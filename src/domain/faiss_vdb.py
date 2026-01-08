from typing import List, Tuple, Optional, Dict, Any
import numpy as np
import faiss
import pickle
import os

from ..interfaces.abstractions import VectorStore


class FAISSVectorStore(VectorStore):
    """
    Vector store using FAISS.
    """
    
    def __init__(self, dimension: int, index_type: str = 'flat'):
        """
        Initialize FAISS vector store. From a brief look online Flat 
        works well for small datasets. 
        """
        self.dimension = dimension # TODO: This is hardcoded on call should ideally depend on embedding model
        self.index_type = index_type
        self.metadata_store: List[Dict[str, Any]] = []
        self.id_store: List[str] = []
        
        if index_type == 'flat':
            # Mainly stuck with this since a quick google search revealed that this work better
            self.index = faiss.IndexFlatL2(dimension)
        else:
            raise NotImplementedError(f"The DB only supports flat at the moment: {index_type}")
    
    def add_vectors(
        self,
        vectors: np.ndarray,
        metadata: List[Dict[str, Any]],
        ids: Optional[List[str]] = None
    ) -> None:
        """
        Add vectors to the store with associated metadata.
        
        Args:
            vectors: 2D array of vectors to add
            metadata: List of metadata dicts (one per vector)
            ids: Optional list of unique IDs for vectors
        """
        
        # We neec continuous id so add to existing ids
        numeric_ids = np.arange(len(self.id_store), len(self.id_store) + len(vectors))
        
        # Add to FAISS index
        self.index.add(vectors)
        
        # Store metadata and IDs
        self.metadata_store.extend(metadata)
        self.id_store.extend(numeric_ids)
    
    def save(self, path: str) -> None:
        """Save the vectordb."""
        os.makedirs(os.path.dirname(path) if os.path.dirname(path) else '.', exist_ok=True)
        
        # Save FAISS index
        faiss.write_index(self.index, f"{path}.index")
        
        # Save metadata and IDs
        with open(f"{path}.metadata", 'wb') as f:
            pickle.dump({
                'metadata_store': self.metadata_store,
                'id_store': self.id_store,
                'dimension': self.dimension,
                'index_type': self.index_type
            }, f)

    def load(self, path: str) -> None:
        """Load vector store from disk."""
        # Load FAISS index
        self.index = faiss.read_index(f"{path}.index")


        # Load metadata so that we can map it back to sentences
        # for testing if the retrieval is working.
        with open(f"{path}.metadata", 'rb') as f:
            data = pickle.load(f)
            self.metadata_store = data['metadata_store']
            self.id_store = data['id_store']
            self.dimension = data['dimension']
            self.index_type = data['index_type']

    def search(self, query:np.ndarray, k:int = 5):
        """
        Use Faiss search to look for most similar indices in index
        """
        distances, indices = self.index.search(query, k)

        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx >= 0:  # Valid index
                results.append((
                    self.id_store[idx],
                    float(dist),
                    self.metadata_store[idx]
                ))
        
        return results


