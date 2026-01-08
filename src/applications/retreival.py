from typing import List, Dict, Any, Optional

from ..interfaces.abstractions import Embedder, VectorStore


class EmbeddingRetriever:
    """
    Application layer to orchestrate relevant chunk retrieval. Basically does
    Query -> embed -> similarity search -> top_k segments
    """
    def __init__(
        self,
        embedder: Embedder,
        vector_store: VectorStore
    ) -> None:
        pass

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        thresh: Optional[int] = None
    ):
        pass