from src.applications.ingestion import IngestionSevice
from src.domain.chunk import SentenceChunker
from src.domain.embed import SentenceTransformerEmbedder
from src.domain.faiss_vdb import FAISSVectorStore


base_path = '/home/adithya/LongHori/document_rag/dataset/Farmers_Bulletin'

chunker = SentenceChunker(1)
embedder = SentenceTransformerEmbedder()
vdb = FAISSVectorStore(384)
ingestor = IngestionSevice(chunker=chunker, embeder=embedder, vector_db=vdb)

# run
ingestor.process_dir(base_path, 1)

query = "Why is it easier to build wide gates?"
query_embedding = embedder.embed_text(query)

vdb.load('/home/adithya/LongHori/document_rag/dataset/vectordb')
print(vdb.metadata_store)
vdb.search(query_embedding)
breakpoint()