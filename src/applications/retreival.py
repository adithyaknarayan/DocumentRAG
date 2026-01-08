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
        self.embedder = embedder
        self.vector_store = vector_store

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        thresh: Optional[int] = None
    ) -> List[dict]:
        # search for the query embedding
        query_embedding = self.embedder.embed_text(query)
        raw_results = self.vector_store.search(query_embedding, k=top_k)

        # for the results, get the relevant chunks
        final_results = []
        for chunk_id, score, metadata in raw_results:
            # threshold
            if thresh is not None and score > thresh:
                continue
            
            # get text from metadata
            text = metadata.get('text', '')
            
            result = {
                'chunk_id': chunk_id,
                'text': text,
                'score': score,
                'metadata': metadata
            }
            final_results.append(result)
        return final_results