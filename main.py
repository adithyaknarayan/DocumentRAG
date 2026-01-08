import argparse
import os

from src.domain.embed import SentenceTransformerEmbedder
from src.domain.faiss_vdb import FAISSVectorStore
from src.domain.generate import HFGenerator
from src.domain.chunk import SentenceChunker
from src.applications.retreival import EmbeddingRetriever
from src.applications.generation import GenerationService
from src.applications.ingestion import IngestionSevice


def ingest_documents(base_path: str, vector_db_path: str, sens_per_chunk: int = 1):
    """
    Ingest documents and save to vector database. This is the same implementation as
    in test_rag.py
    """
    chunker = SentenceChunker(sens_per_chunk=sens_per_chunk)
    embedder = SentenceTransformerEmbedder(model_name='all-MiniLM-L6-v2')
    vdb = FAISSVectorStore(dimension=embedder.embed_dim)
    ingestor = IngestionSevice(chunker=chunker, embeder=embedder, vector_db=vdb)
    ingestor.process_dir(base_path)
    print(f"Done. Saved to {vector_db_path}")

def interactive_mode(retriever, generator, top_k, max_tokens, temperature):
    """Interactive question-answering mode."""
    print("\nInteractive mode. Type 'quit' or 'q' to exit.\n")
    
    while True:
        try:
            query = input("Question: ").strip()
            
            if query.lower() in ['quit', 'exit', 'q', '']:
                break
            
            retrieved_chunks = retriever.retrieve(query, top_k=top_k)
            response = generator.generate_response(
                query=query,
                retrieved_chunks=retrieved_chunks,
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            print(f"\nAnswer: {response}\n")
            
        except KeyboardInterrupt:
            print("\n")
            break
        except Exception as e:
            print(f"Error: {str(e)}\n")


def main():
    parser = argparse.ArgumentParser(description="Minimal RAG System")
    parser.add_argument("--ingest_first", action="store_true", help="Ingest documents first")
    parser.add_argument("--sens_per_chunk", type=int, default = 1, help="How many sentences to include per chunk")
    parser.add_argument("--data_path", type=str, default="dataset/Farmers_Bulletin")
    parser.add_argument("--vector_db_path", type=str, default="dataset/vectordb")
    parser.add_argument("--query", type=str, default=None, help="Single query (omit for interactive)")
    parser.add_argument("--model_name", type=str, default="TinyLlama/TinyLlama-1.1B-Chat-v1.0")
    parser.add_argument("--embedder_name", type=str, default="all-MiniLM-L6-v2")
    parser.add_argument("--top_k", type=int, default=3)
    parser.add_argument("--max_tokens", type=int, default=256)
    parser.add_argument("--temperature", type=float, default=0.7)
    args = parser.parse_args()
    
    if args.ingest_first:
        ingest_documents(args.data_path, args.vector_db_path, args.sens_per_chunk)
    embedder = SentenceTransformerEmbedder(model_name=args.embedder_name)
    vector_store = FAISSVectorStore(dimension=embedder.embed_dim)
    
    if not os.path.exists(f"{args.vector_db_path}.index"):
        print(f"Error: Vector database not found at {args.vector_db_path}. Use the --ingest_first flag")
        return
    
    vector_store.load(args.vector_db_path)
    llm = HFGenerator(model_name=args.model_name)
    
    retriever = EmbeddingRetriever(embedder=embedder, vector_store=vector_store)
    generator = GenerationService(llm_generator=llm)
    
    interactive_mode(retriever, generator, args.top_k, args.max_tokens, args.temperature)


if __name__ == "__main__":
    main()
