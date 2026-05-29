def chunk_document(text: str, chunk_size: int = 400, overlap: int = 50) -> list[str]:
    sanitized = " ".join(text.split())
    if len(sanitized) <= chunk_size:
        return [sanitized]

    chunks: list[str] = []
    start = 0
    while start < len(sanitized):
        end = start + chunk_size
        chunks.append(sanitized[start:end])
        if end >= len(sanitized):
            break
        start = end - overlap
    return chunks
