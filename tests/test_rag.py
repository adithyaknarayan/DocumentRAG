from src.domain.embed import SentenceTransformerEmbedder
from src.domain.faiss_vdb import FAISSVectorStore
from src.domain.generate import HFGenerator
from src.applications.retreival import EmbeddingRetriever
from src.applications.generation import GenerationService

print("Loading embedder...")
embedder = SentenceTransformerEmbedder(model_name='all-MiniLM-L6-v2')

print("Loading vector store...")
vector_store = FAISSVectorStore(dimension=embedder.embed_dim)
vector_store.load("dataset/vectordb")  # Load your pre-built index
model_name = 'TinyLlama/TinyLlama-1.1B-Chat-v1.0'
print(f"Loading {model_name}...")
llm = HFGenerator(model_name=model_name)

retriever = EmbeddingRetriever(embedder=embedder, vector_store=vector_store)
generator = GenerationService(llm_generator=llm)

query = "Why is it easier to build wide gates?"

print(f"\nQuery: {query}")
print("\n1. Retrieving relevant context...")
retrieved_chunks = retriever.retrieve(query, top_k=3)

print(f"   Found {len(retrieved_chunks)} relevant chunks")
for i, chunk in enumerate(retrieved_chunks, 1):
    print(f"   [{i}] Score: {chunk['score']:.3f}")

print("\n2. Generating response...")
response = generator.generate_response(
    query=query,
    retrieved_chunks=retrieved_chunks,
    max_tokens=256,
    temperature=0.7
)

print("\n" + "="*50)
print("ANSWER:")
print("="*50)
print(response)
print("="*50)

