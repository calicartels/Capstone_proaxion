"""
Document retrieval system for the RAG chatbot.
"""
from typing import Dict, List, Any
import vertexai
from vertexai.generative_models import GenerativeModel

from config.settings import TEXT_MODEL, SIMILARITY_THRESHOLD, MAX_CONTEXT_LENGTH
from rag.document_store import DocumentStore

class Retriever:
    """Retrieve relevant document chunks for a query."""
    
    def __init__(self, document_store: DocumentStore = None):
        """
        Initialize the retriever.
        
        Args:
            document_store (DocumentStore, optional): Document store to use.
        """
        self.document_store = document_store or DocumentStore()
        self.model = GenerativeModel(TEXT_MODEL)
    
    def retrieve_for_query(self, query: str, doc_ids: List[str] = None, max_chunks: int = 5) -> List[Dict]:
        """
        Retrieve relevant chunks for a query.
        
        Args:
            query (str): User query
            doc_ids (List[str], optional): Document IDs to search. 
                                          If None, search all known documents.
            max_chunks (int): Maximum number of chunks to return
            
        Returns:
            List[Dict]: Relevant document chunks
        """
        relevant_chunks = []
        
        # If no doc_ids provided, we could implement a way to search all documents
        # For now, we'll just require document IDs
        if not doc_ids:
            print("⚠️ No document IDs provided for retrieval")
            return []
        
        # Process each document
        for doc_id in doc_ids:
            # Get all chunks for this document
            chunks = self.document_store.get_chunks(doc_id)
            
            if not chunks:
                print(f"⚠️ No chunks found for document {doc_id}")
                continue
            
            # Score each chunk for relevance to the query
            scored_chunks = self._score_chunks(query, chunks)
            
            # Add relevant chunks to the results
            relevant_chunks.extend(scored_chunks)
        
        # Sort by relevance score
        relevant_chunks.sort(key=lambda c: c["relevance_score"], reverse=True)
        
        # Return the top chunks
        return relevant_chunks[:max_chunks]
    
    def _score_chunks(self, query: str, chunks: List[Dict]) -> List[Dict]:
        """
        Score chunks for relevance to the query using the LLM.
        
        Args:
            query (str): User query
            chunks (List[Dict]): Document chunks
            
        Returns:
            List[Dict]: Scored chunks with relevance scores
        """
        scored_chunks = []
        
        for chunk in chunks:
            # Use the LLM to determine relevance
            chunk_text = chunk.get("text", "")
            relevance = self._get_relevance_score(query, chunk_text)
            
            # Only include chunks above the threshold
            if relevance >= SIMILARITY_THRESHOLD:
                scored_chunks.append({
                    **chunk,
                    "relevance_score": relevance
                })
        
        return scored_chunks
    
    def _get_relevance_score(self, query: str, text: str) -> float:
        """
        Use the LLM to determine the relevance of text to a query.
        
        Args:
            query (str): User query
            text (str): Text to evaluate
            
        Returns:
            float: Relevance score between 0 and 1
        """
        prompt = f"""
        Query: {query}
        
        Text: {text}
        
        On a scale from 0 to 1, how relevant is the Text to the Query?
        Provide only a single floating-point number as your answer, where:
        - 0 means completely irrelevant
        - 1 means perfectly relevant
        
        Score:
        """
        
        try:
            response = self.model.generate_content(prompt)
            
            # Extract the relevance score from the response
            score_text = response.text.strip()
            
            # Try to convert to a float
            try:
                score = float(score_text)
                return max(0.0, min(1.0, score))  # Ensure between 0 and 1
            except ValueError:
                print(f"⚠️ Could not parse relevance score: {score_text}")
                return 0.5  # Default to medium relevance
                
        except Exception as e:
            print(f"⚠️ Error getting relevance score: {e}")
            return 0.5  # Default to medium relevance