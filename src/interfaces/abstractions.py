"""Abstract base classes defining core interfaces for the RAG system.
Doing this so that later down the line if I wasnt to ablate implementations
it's a bit easier.
"""

from abc import ABC, abstractmethod
from typing import List, Tuple, Optional, Dict, Any
import numpy as np

class DocumentChunker(ABC):
    """
    Abstraction for all the document chunking strategies.
    """
    
    @abstractmethod
    def chunk_text(
        self,
        text: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Split text into chunks. Also return with metadata
        
        Input:
            text: The full test that we feed into the chunker
            metadata: Chunk metadata. Currently we broadcast this to all chunk extracted from text.
            
        Returns:
            The chunks as a list of dicts.
        """
        pass

class Embedder(ABC):
    """Abstract interface for text embedding models."""
    
    @abstractmethod
    def embed_batch(self, texts: List[str]) -> np.ndarray:
        """
        Generate embeddings for multiple texts by running over eaach text.
        
        Args:
            texts: List of texts to embed
            
        Returns:
            2D numpy array of embeddings (one per text).
        """
        pass