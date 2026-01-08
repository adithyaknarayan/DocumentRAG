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
        
        Inputs:
            texts: List of texts to embed
            
        Returns:
            2D numpy array of embeddings (one per text).
        """
        pass

class VectorStore(ABC):
    """Abstract interface for vector storage and similarity search.
    The original idea was that I leave the doors open for me to test other
    vectir databases.
    """
    
    @abstractmethod
    def add_vectors(
        self,
        vectors: np.ndarray,
        metadata: List[Dict[str, Any]],
        ids: Optional[List[str]] = None
    ) -> None:
        """
        Add vectors to the store with associated metadata.
        
        Inputs:
            vectors: 2D array of vectors to add
            metadata: List of metadata dicts (one per vector)
            ids: Optional list of unique IDs for vectors
        """
        pass
    
    @abstractmethod
    def save(self, path: str) -> None:
        """Save things to disk."""
        pass
    
    @abstractmethod
    def load(self, path:str) -> None:
        """Load vector store from disk."""
        pass

    @abstractmethod
    def search(self, query:np.ndarray, k:int):
        """
        Search for vecros in the index and return the relevant metadata
        Inputs:
            query: the query embedding that we want to search against
            k: the top k that similar entries in the db that we want

        Returns:
            List of metadata entries returned from the indices with min
            distance to the query.
        """
