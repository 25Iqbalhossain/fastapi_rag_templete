import hashlib
from collections import Counter

from app.providers.llm.base import BaseLLMProvider
from app.providers.vectorstores.base import BaseVectorStore, VectorDocument
from app.schemas.rag import QueryResponse, RetrievedChunk
from app.services.chunking import chunk_document
from app.services.embeddings import EmbeddingService


class RAGPipeline:
    def __init__(
        self,
        embeddings: EmbeddingService,
        vectorstore: BaseVectorStore,
        llm: BaseLLMProvider,
    ) -> None:
        self.embeddings = embeddings
        self.vectorstore = vectorstore
        self.llm = llm

    async def ingest_document(self, user_id: int, document_id: str, text: str) -> list[str]:
        chunks = chunk_document(text)
        await self.vectorstore.delete_by_filters(
            {"user_id": str(user_id), "document_id": document_id}
        )
        documents: list[VectorDocument] = []
        for index, chunk in enumerate(chunks):
            chunk_key = f"{user_id}:{document_id}:{index}:{chunk}".encode("utf-8")
            vector_id = hashlib.sha256(chunk_key).hexdigest()
            documents.append(
                VectorDocument(
                    id=vector_id,
                    text=chunk,
                    embedding=await self.embeddings.embed_text(chunk),
                    metadata={
                        "user_id": str(user_id),
                        "document_id": document_id,
                        "chunk_index": index,
                        "chunk_id": f"{document_id}-{index}",
                    },
                )
            )
        return await self.vectorstore.insert_documents(documents)

    async def run(
        self,
        *,
        user_id: int,
        query: str,
        limit: int,
        document_id: str | None = None,
        include_debug: bool = False,
    ) -> QueryResponse:
        filters: dict[str, str] = {"user_id": str(user_id)}
        if document_id is not None:
            filters["document_id"] = document_id
        initial_matches = await self.vectorstore.similarity_search(query, max(limit * 2, limit), filters)
        matches = self.rerank(query, initial_matches)[:limit]
        context = "\n\n".join(match.text for match in matches)
        prompt = self.build_prompt(query, context)
        answer = await self.llm.generate(prompt)
        return QueryResponse(
            answer=answer,
            matches=[
                RetrievedChunk(
                    chunk_id=str(match.metadata.get("chunk_id", match.id)),
                    score=match.score,
                    text=match.text,
                )
                for match in matches
            ],
            debug={
                "prompt": prompt,
                "retrieved_count": len(initial_matches),
                "reranked_count": len(matches),
                "filters": filters,
            }
            if include_debug
            else None,
        )

    def build_prompt(self, query: str, context: str) -> str:
        return (
            "You are an enterprise AI backend assistant. "
            "Answer using the provided context when relevant.\n\n"
            f"Context:\n{context or 'No context found.'}\n\n"
            f"Question:\n{query}"
        )

    def rerank(self, query: str, matches: list) -> list:
        query_terms = Counter(self._normalize_terms(query))
        scored_matches = []
        for match in matches:
            lexical_score = self._lexical_overlap_score(query_terms, match.text)
            combined_score = (float(match.score) * 0.7) + (lexical_score * 0.3)
            scored_matches.append((combined_score, match))
        scored_matches.sort(key=lambda item: item[0], reverse=True)
        return [match for _, match in scored_matches]

    def _lexical_overlap_score(self, query_terms: Counter[str], text: str) -> float:
        text_terms = Counter(self._normalize_terms(text))
        if not query_terms:
            return 0.0
        overlap = sum(min(count, text_terms.get(term, 0)) for term, count in query_terms.items())
        return overlap / max(sum(query_terms.values()), 1)

    def _normalize_terms(self, text: str) -> list[str]:
        return [token.strip(".,!?;:\"'()[]{}").lower() for token in text.split() if token.strip()]