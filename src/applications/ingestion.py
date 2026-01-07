from typing import List, Optional
from pathlib import Path
import hashlib
import glob

from ..interfaces.abstractions import Embedder, DocumentChunker

class IngestionSevice:
    """
    This orchestrates the embedding and chunking interfaces.
    """
    def __init__(
        self,
        embeder: Embedder,
        chunker: DocumentChunker
    ) -> None:
        """
        Ingest documents and generate embeddings.
        """
        self.embedder = embeder
        self.chunker = chunker
    
    def process_document(self, document:str):

        # chunk text
        chunks = self.chunker.chunk_text(document, None)
        
        # split into text and metadata
        texts = [chunk['text'] for chunk in chunks]
        metadatas = [chunk['metadata'] for chunk in chunks]

        embeds = self.embedder.embed_batch(texts)

        return embeds

    def process_dir(self, base_path:str) -> None:
        """
        Glob all txt files and extract the txt data from it
        """
        file_paths = glob.glob(f"{base_path}/*.txt")
        embeds = []

        for file_path in file_paths:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    document = f.read()
                    embeds.append(self.process_document(document))
            except Exception as e:
                print(f"[error_log]: could not process {file_path}")

        # temp return to test
        return embeds