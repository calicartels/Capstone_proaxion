"""
Response generation using Vertex AI.
"""
from typing import Dict, List, Any
import vertexai
from vertexai.generative_models import GenerativeModel

from config.settings import TEXT_MODEL, MAX_CONTEXT_LENGTH
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
        self.model = GenerativeModel(TEXT_MODEL)
    
    def generate_response(self, context: str, doc_ids: List[str] = None) -> Dict:
        """
        Generate a response using RAG.
        
        Args:
            context (str): Current frontend context or query
            doc_ids (List[str], optional): Document IDs to search
            
        Returns:
            Dict: Generated response with metadata
        """
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
        
        # Generate response
        response = self._generate_with_context(context, context_text)
        
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
    
    def _generate_with_context(self, query: str, context_text: str) -> str:
        """
        Generate a response using the LLM with context.
        
        Args:
            query (str): User query
            context_text (str): Context from retrieved documents
            
        Returns:
            str: Generated response
        """
        prompt = f"""
        You are a helpful assistant for ProAxion sensor installation and machine monitoring. 
        You provide specific, accurate information based on the provided context.
        If you don't know the answer or if it's not covered in the context, say so clearly.
        
        Context:
        {context_text}
        
        Current user situation: {query}
        
        Based on the context, provide a helpful and accurate response about sensor installation, 
        configuration, or troubleshooting. Be specific and provide details from the context.
        """
        
        try:
            response = self.model.generate_content(prompt)
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