from typing import List, Dict, Any, Optional

from ..interfaces.abstractions import LLMGenerator


class GenerationService:
    """Combines retrieved chunks with LLM to generate responses."""
    
    def __init__(self, llm_generator: LLMGenerator):
        self.llm = llm_generator
    
    def generate_response(
        self,
        query: str,
        retrieved_chunks: List[Dict[str, Any]],
        max_tokens: Optional[int] = 512,
        temperature: float = 0.7
    ) -> str:
        """Generate response from query and retrieved chunks."""
        prompt = self._build_prompt(query, retrieved_chunks)
        return self.llm.generate(prompt, max_tokens=max_tokens, temperature=temperature)
    
    def _build_prompt(self, query: str, retrieved_chunks: List[Dict[str, Any]]) -> str:
        """Build instruction-style prompt for MPT-7B-Chat."""
        contexts = [f"[{i}] {chunk.get('text', '').strip()}" 
                   for i, chunk in enumerate(retrieved_chunks, 1) if chunk.get('text')]
        context_str = "\n\n".join(contexts)
        
        return f"""
### Instruction:
Answer the following question based on the provided context. Be concise and accurate.

### Context:
{context_str}

### Question:
{query}

### Response:"""
