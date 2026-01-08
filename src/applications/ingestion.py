from typing import List, Optional
from pathlib import Path
import hashlib
import glob

from ..interfaces.abstractions import Embedder, DocumentChunker, VectorStore

class IngestionSevice:
    """
    This orchestrates the embedding and chunking interfaces.
    """
    def __init__(
        self,
        embeder: Embedder,
        chunker: DocumentChunker,
        vector_db: VectorStore
    ) -> None:
        """
        Ingest documents and generate embeddings.
        """
        self.embedder = embeder
        self.chunker = chunker
        self.vector_db = vector_db
    
    def process_document(self, document:str):
        # Chunk text
        chunks = self.chunker.chunk_text(document)
        
        # Split into text and metadata
        texts = [chunk['text'] for chunk in chunks]
        metadatas = [chunk['metadata'] for chunk in chunks]
        print(metadatas)
        embeds = self.embedder.embed_batch(texts)
        
        # Generate chunk_ids
        chunk_ids = [i for i in range(len(chunks))]

        # Now add the embedding to the vectordb
        self.vector_db.add_vectors(embeds, metadatas, chunk_ids)

    def process_dir(self, base_path:str, proc_len: Optional[int] = None) -> None:
        """
        Glob all txt files and extract the txt data from it
        """
        file_paths = glob.glob(f"{base_path}/*.txt")
        if proc_len:
            file_paths = file_paths[:proc_len]

        for file_path in file_paths:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    document = f.read()
                    self.process_document(document)
            except Exception as e:
                print(e)
                print(f"[error_log]: could not process {file_path}")

        self.vector_db.save(f"{base_path}/vectordb/db")