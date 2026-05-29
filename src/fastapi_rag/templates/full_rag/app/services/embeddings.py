import hashlib
import math


class EmbeddingService:
    def __init__(self, dimensions: int) -> None:
        self.dimensions = dimensions

    async def embed_text(self, text: str) -> list[float]:
        buckets = [0.0] * self.dimensions
        for token in text.lower().split():
            digest = hashlib.sha256(token.encode("utf-8")).digest()
            index = digest[0] % self.dimensions
            magnitude = (digest[1] / 255) + 0.01
            buckets[index] += magnitude
        norm = math.sqrt(sum(value * value for value in buckets)) or 1.0
        return [value / norm for value in buckets]
