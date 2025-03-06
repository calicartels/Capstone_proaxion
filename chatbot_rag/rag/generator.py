"""
Response generation using Vertex AI.
"""
from typing import Dict, List, Any
import vertexai
from vertexai.generative_models import GenerativeModel

from config import settings
from config.settings import TEXT_MODEL, MAX_CONTEXT_LENGTH, MODEL_TEMPERATURE
from rag.retriever import Retriever

class Generator:
    """Generate responses using RAG and Vertex AI."""
    
    def __init__(self, retriever: Retriever = None):
        """
        Initialize the generator.
        
        Args:
            retriever (Retriever, optional): Retriever to use.
        """
        self.retriever = retriever or Retriever()
        self.model = GenerativeModel("gemini-2.0-flash-001")    

    # In chatbot_rag/rag/generator.py
    def generate_response(self, context: str, doc_ids: List[str] = None, history: List[Dict] = None) -> Dict:
        """Generate a response using RAG."""
        # Retrieve relevant chunks
        chunks = self.retriever.retrieve_for_query(context, doc_ids)
        
        if not chunks:
            # No relevant chunks found
            return {
                "text": "I don't have specific information about this. Please provide more details or try asking about sensor installation, machine configurations, or troubleshooting.",
                "has_context": False
            }
        
        # Prepare context from chunks
        context_text = self._prepare_context(chunks)
        
        # Generate response with history if provided
        response = self._generate_with_context(context, context_text, history)
        
        # Extract sources for attribution
        sources = self._extract_sources(chunks)
        
        return {
            "text": response,
            "has_context": True,
            "sources": sources
        }

    
    def _prepare_context(self, chunks: List[Dict]) -> str:
        """
        Prepare context from chunks, respecting token limits.
        
        Args:
            chunks (List[Dict]): Relevant document chunks
            
        Returns:
            str: Prepared context text
        """
        context_text = "Information from knowledge base:\n\n"
        
        # Add chunk text to context, with metadata
        for chunk in chunks:
            # Get metadata
            metadata = chunk.get("metadata", {})
            doc_title = metadata.get("doc_title", "Unknown Document")
            section_title = metadata.get("section_title", "")
            
            # Add chunk with source info
            chunk_context = f"Source: {doc_title}"
            if section_title:
                chunk_context += f" - {section_title}"
            chunk_context += f"\n{chunk.get('text', '')}\n\n"
            
            # Add to context if we have space
            if len(context_text + chunk_context) < MAX_CONTEXT_LENGTH:
                context_text += chunk_context
            else:
                # We're out of space
                break
        
        return context_text
    
    def _generate_with_context(self, query: str, context_text: str, history=None) -> str:
        """Generate a response using the LLM with context and history."""
        history_text = ""
        if history and len(history) > 0:
            history_text = "Previous conversation:\n"
            for item in history:
                role = item.get("role", "")
                content = item.get("content", "")
                if role == "user":
                    history_text += f"User: {content}\n"
                elif role == "assistant":
                    history_text += f"Assistant: {content}\n"
            history_text += "\n"
        
        prompt = f"""
        You are ProAxion Assistant, a helpful and knowledgeable expert on sensor installation and machine monitoring.
        You communicate in a clear, professional manner with concise, well-structured responses.
        
        {history_text}
        
        CONTEXT INFORMATION:
        {context_text}
        
        USER QUERY: {query}
        
        Based on the context information provided, create a helpful, focused response that directly addresses the user's query.
        
        Your response should:
        1. Be clear, concise and well-structured using markdown formatting
        2. Focus specifically on answering the user's query rather than providing general information 
        3. Use bullet points and headings to organize information
        4. Provide practical, actionable guidance when appropriate
        5. Be friendly but professional in tone
        
        DO NOT include references to the "context information" or say phrases like "based on the provided context".
        Simply answer directly as if you know this information naturally.
        """
        
        try:
            generation_config = {
                "temperature": 0.2,
                "max_output_tokens": 800,
            }
            
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )
            return response.text.strip()
        except Exception as e:
            print(f"⚠️ Error generating response: {e}")
            return "I'm sorry, I encountered an error while generating a response. Please try again."
    
    def _extract_sources(self, chunks: List[Dict]) -> List[Dict]:
        """
        Extract sources from chunks for attribution.
        
        Args:
            chunks (List[Dict]): Retrieved chunks
            
        Returns:
            List[Dict]: Source information
        """
        sources = []
        seen_docs = set()
        
        for chunk in chunks:
            metadata = chunk.get("metadata", {})
            doc_id = metadata.get("doc_id", "")
            doc_title = metadata.get("doc_title", "Unknown Document")
            
            # Only include each document once
            if doc_id and doc_id not in seen_docs:
                seen_docs.add(doc_id)
                sources.append({
                    "id": doc_id,
                    "title": doc_title
                })
        
        return sources