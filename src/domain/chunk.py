from typing import List, Dict, Any, Optional
import spacy
import re

from ..interfaces.abstractions import DocumentChunker

class SentenceChunker(DocumentChunker):
    def __init__(self, sens_per_chunk:int = 5):
       self.nlp = spacy.load("en_core_web_sm")
       self.sens_per_chunk = sens_per_chunk

    def split_sentences(self, text: str):
        doc = self.nlp(text)
        return [sent.text.strip() for sent in doc.sents]

    def chunk_text(
        self,
        text: str,
        metadata: Optional[Dict[str, Any]] = None
        ) -> List[Dict[str, Any]]:
        sentences = self.split_sentences(text)
        if not metadata:
            metadata = {}
        
        chunks = []
        chunk_idx = 0
        
        for i in range(0, len(sentences), self.sens_per_chunk):
            chunk_sentences = sentences[i:i + self.sens_per_chunk]
            chunk_text = ' '.join(chunk_sentences)
            
            if chunk_text.strip():
                chunk_metadata = {
                    **metadata,
                    'chunk_index': chunk_idx,
                    'sentence_start': i,
                    'sentence_end': i + len(chunk_sentences),
                    'num_sentences': len(chunk_sentences)
                }
                
                chunks.append({
                    'text': chunk_text.strip(),
                    'metadata': chunk_metadata
                })
                
                chunk_idx += 1
        
        return chunks