from src.applications.ingestion import IngestionSevice
from src.domain.chunk import SentenceChunker
from src.domain.embed import SentenceTransformerEmbedder


base_path = '/home/adithya/LongHori/document_rag/dataset/Farmers_Bulletin'

chunker = SentenceChunker(1)
embedder = SentenceTransformerEmbedder()
ingestor = IngestionSevice(chunker=chunker, embeder=embedder)

# run
ingestor.process_dir(base_path)