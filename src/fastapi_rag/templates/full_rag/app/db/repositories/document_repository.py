from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.document import Document, DocumentStatus


class DocumentRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, doc_id: int) -> Document | None:
        result = await self.session.execute(select(Document).where(Document.id == doc_id))
        return result.scalar_one_or_none()

    async def list_by_user(self, user_id: int) -> list[Document]:
        result = await self.session.execute(
            select(Document).where(Document.user_id == user_id).order_by(Document.created_at.desc())
        )
        return list(result.scalars().all())

    async def create(
        self,
        *,
        user_id: int,
        filename: str,
        content_type: str,
        storage_path: str,
    ) -> Document:
        doc = Document(
            user_id=user_id,
            filename=filename,
            content_type=content_type,
            storage_path=storage_path,
        )
        self.session.add(doc)
        await self.session.commit()
        await self.session.refresh(doc)
        return doc

    async def update_status(
        self, doc_id: int, status: DocumentStatus, error_message: str | None = None
    ) -> Document | None:
        doc = await self.get_by_id(doc_id)
        if doc:
            doc.status = status
            doc.error_message = error_message
            await self.session.commit()
            await self.session.refresh(doc)
        return doc
