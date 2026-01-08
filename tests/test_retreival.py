from src.applications.ingestion import IngestionSevice
from src.domain.chunk import SentenceChunker
from src.domain.embed import SentenceTransformerEmbedder
from src.domain.faiss_vdb import FAISSVectorStore
from src.applications.retreival import EmbeddingRetriever

base_path = '/home/adithya/LongHori/document_rag/dataset/Farmers_Bulletin'

chunker = SentenceChunker(5)
embedder = SentenceTransformerEmbedder()
vdb = FAISSVectorStore(384)
ingestor = IngestionSevice(chunker=chunker, embeder=embedder, vector_db=vdb)

# run
ingestor.process_dir(base_path, 1)

query = "Why is it easier to build wide gates?"
retr = EmbeddingRetriever(embedder, vdb)
retr.retrieve(query, 5, None)
breakpoint()