from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer

from ..interfaces.abstractions import Embedder


class SentenceTransformerEmbedder(Embedder):
    """
    Embedder implementation using sentence-transformers. I'll likely try something better
    """
    
    def __init__(
        self,
        model_name: str = 'all-MiniLM-L6-v2',
        device: str = 'cpu'
    ):
        """
        Initialize embedder with a specific model.
        
        Args:
            model_name: Hugging Face model identifier
            device: gpu_id to run on
        """
        self.model_name = model_name
        self.device = device
        self.model = SentenceTransformer(model_name, device=device)
        self.embed_dim= self.model.get_sentence_embedding_dimension()
    
    def embed_text(self, text: str) -> np.ndarray:
        """
        Generate embedding for a single text. This is
        mainly for the query processing. Use embed_batch
        for data ingestion.
        
        Args:
            text: Input text to embed
            
        Returns:
            Embedding vector as numpy array
        """
        
        embedding = self.model.encode(
            text,
            convert_to_numpy=True,
            normalize_embeddings=True
        )
        embedding = np.expand_dims(embedding, axis=0)
        return embedding

    def embed_batch(self, texts: List[str]) -> np.ndarray:
        """
        Generate embeddings for multiple texts efficiently.
        
        Args:
            texts: List of texts to embed
            
        Returns:
            2D numpy array of embeddings (one per text)
        """
        if not texts:
            return np.array([])
        
        # Filter out empty texts and track indices
        valid_texts = []
        valid_indices = []
        for i, text in enumerate(texts):
            if text and text.strip():
                valid_texts.append(text)
                valid_indices.append(i)
        
        # Create result array
        result = np.zeros((len(texts), self.embed_dim), dtype=np.float32)
        
        if valid_texts:
            # Embed valid texts
            embeddings = self.model.encode(
                valid_texts,
                convert_to_numpy=True,
                normalize_embeddings=True,
                show_progress_bar=len(valid_texts) > 10
            )
            
            # Place embeddings at correct indices
            for i, idx in enumerate(valid_indices):
                result[idx] = embeddings[i]
        
        return result
