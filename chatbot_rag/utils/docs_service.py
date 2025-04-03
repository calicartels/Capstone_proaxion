"""
Google Docs utilities for retrieving and processing document content.
"""
from typing import Dict, List, Optional, Union
import re
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from utils.auth import get_docs_service

class DocsProcessor:
    """Process Google Docs content for RAG system."""
    
    def __init__(self):
        """Initialize the DocsProcessor."""
        self.docs_service = get_docs_service()
        
    def get_document_content(self, doc_id: str) -> Dict:
        """
        Get the content of a Google Doc by its ID.
        
        Args:
            doc_id (str): Google Docs document ID
            
        Returns:
            Dict: Document content with text and structure
        """
        try:
            # Get document content
            document = self.docs_service.documents().get(documentId=doc_id).execute()
            
            # Process the document
            content = self._process_document(document)
            return content
        except HttpError as error:
            print(f"Error retrieving document {doc_id}: {error}")
            return {"error": str(error)}
    
    def _process_document(self, document: Dict) -> Dict:
        """
        Process a Google Doc document into a structured format.
        
        Args:
            document (Dict): Google Doc API response
            
        Returns:
            Dict: Processed document content
        """
        result = {
            "title": document.get("title", "Untitled"),
            "doc_id": document.get("documentId", ""),
            "sections": [],
            "text": ""
        }
        
        # Process document content
        if "body" in document and "content" in document["body"]:
            content = document["body"]["content"]
            current_section = None
            current_text = ""
            
            for item in content:
                if "paragraph" in item:
                    paragraph = item["paragraph"]
                    
                    # Extract text from paragraph
                    para_text = ""
                    if "elements" in paragraph:
                        for element in paragraph["elements"]:
                            if "textRun" in element:
                                para_text += element["textRun"].get("content", "")
                    
                    # Check if this is a heading
                    if "paragraphStyle" in paragraph and "namedStyleType" in paragraph["paragraphStyle"]:
                        style = paragraph["paragraphStyle"]["namedStyleType"]
                        if style.startswith("HEADING_"):
                            # If we've been collecting text, add it to the current section
                            if current_section and current_text:
                                current_section["content"] = current_text
                                result["sections"].append(current_section)
                            
                            # Start a new section
                            heading_level = int(style.split("_")[1])
                            current_section = {
                                "title": para_text.strip(),
                                "level": heading_level,
                                "content": ""
                            }
                            current_text = ""
                            continue
                    
                    # Add to current text
                    current_text += para_text
                    result["text"] += para_text
            
            # Add the final section
            if current_section and current_text:
                current_section["content"] = current_text
                result["sections"].append(current_section)
        
        return result
    
    def extract_chunks(self, document: Dict, chunk_size: int = 1000, overlap: int = 200) -> List[Dict]:
        """
        Extract overlapping chunks from a document for embedding.
        
        Args:
            document (Dict): Processed document
            chunk_size (int): Target size of each chunk in characters
            overlap (int): Overlap between chunks in characters
            
        Returns:
            List[Dict]: List of document chunks with metadata
        """
        chunks = []
        
        # Process each section
        for section in document.get("sections", []):
            section_title = section.get("title", "")
            section_level = section.get("level", 1)
            section_content = section.get("content", "")
            
            # Skip empty sections
            if not section_content.strip():
                continue
            
            # Create chunks from this section
            section_chunks = self._create_chunks(
                text=section_content,
                chunk_size=chunk_size,
                overlap=overlap,
                metadata={
                    "doc_id": document.get("doc_id", ""),
                    "doc_title": document.get("title", ""),
                    "section_title": section_title,
                    "section_level": section_level
                }
            )
            chunks.extend(section_chunks)
        
        return chunks
    
    def _create_chunks(self, text: str, chunk_size: int, overlap: int, metadata: Dict) -> List[Dict]:
        """
        Create overlapping chunks from text.
        
        Args:
            text (str): Text to chunk
            chunk_size (int): Target size of each chunk
            overlap (int): Overlap between chunks
            metadata (Dict): Metadata to include with each chunk
            
        Returns:
            List[Dict]: List of chunks with metadata
        """
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # If text is shorter than chunk_size, return it as a single chunk
        if len(text) <= chunk_size:
            return [{
                "text": text,
                "metadata": metadata
            }]
        
        chunks = []
        start = 0
        
        while start < len(text):
            # Find a good breakpoint near the chunk_size
            end = min(start + chunk_size, len(text))
            
            # If we're not at the end, try to break at a sentence boundary
            if end < len(text):
                # Try to find the last sentence boundary within the chunk
                last_period = text.rfind('.', start, end)
                if last_period > start + chunk_size // 2:  # Only break at sentence if it's not too short
                    end = last_period + 1
            
            # Create the chunk
            chunk_text = text[start:end].strip()
            chunks.append({
                "text": chunk_text,
                "metadata": {
                    **metadata,
                    "chunk_index": len(chunks)
                }
            })
            
            # Move to next chunk with overlap
            start = end - overlap if end < len(text) else len(text)
        
        return chunks