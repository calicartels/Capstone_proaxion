"""
Document store for RAG system using Google Cloud Storage.
"""
import json
import os
import hashlib
from typing import Dict, List, Any

from google.cloud import storage
from config.settings import PROJECT_ID
from utils.auth import setup_vertex_ai

class DocumentStore:
    """Store and retrieve documents for RAG system."""
    
    def __init__(self, bucket_name: str = None):
        """
        Initialize the document store.
        
        Args:
            bucket_name (str, optional): GCS bucket name. Defaults to PROJECT_ID + "-rag-store".
        """
        # Initialize GCS client
        credentials = setup_vertex_ai()
        self.client = storage.Client(credentials=credentials, project=PROJECT_ID)
        
        # Use default bucket name if not provided
        self.bucket_name = bucket_name or f"{PROJECT_ID}-rag-store"
        
        # Ensure bucket exists
        self._ensure_bucket_exists()
    
    def _ensure_bucket_exists(self):
        """Create the bucket if it doesn't exist."""
        try:
            self.bucket = self.client.get_bucket(self.bucket_name)
            print(f"✓ Using existing bucket: {self.bucket_name}")
        except:
            print(f"Creating new bucket: {self.bucket_name}")
            self.bucket = self.client.create_bucket(self.bucket_name)
    
    def store_document(self, doc_id: str, content: Dict) -> str:
        """
        Store a document in GCS.
        
        Args:
            doc_id (str): Document ID
            content (Dict): Document content
            
        Returns:
            str: Blob name where document is stored
        """
        # Create a unique filename based on doc_id
        blob_name = f"docs/{doc_id}.json"
        
        # Create GCS blob
        blob = self.bucket.blob(blob_name)
        
        # Upload content as JSON
        blob.upload_from_string(
            json.dumps(content, ensure_ascii=False, indent=2),
            content_type="application/json"
        )
        
        print(f"✓ Stored document {doc_id} in {blob_name}")
        return blob_name
    
    def store_chunks(self, doc_id: str, chunks: List[Dict]) -> List[str]:
        """
        Store document chunks in GCS.
        
        Args:
            doc_id (str): Document ID
            chunks (List[Dict]): Document chunks
            
        Returns:
            List[str]: Blob names where chunks are stored
        """
        blob_names = []
        
        for i, chunk in enumerate(chunks):
            # Create chunk metadata
            chunk_id = f"{doc_id}_chunk_{i}"
            
            # Store the chunk
            blob_name = f"chunks/{chunk_id}.json"
            blob = self.bucket.blob(blob_name)
            
            # Upload content as JSON
            blob.upload_from_string(
                json.dumps(chunk, ensure_ascii=False, indent=2),
                content_type="application/json"
            )
            
            blob_names.append(blob_name)
        
        print(f"✓ Stored {len(chunks)} chunks for document {doc_id}")
        return blob_names
    
    def get_document(self, doc_id: str) -> Dict:
        """
        Retrieve a document from GCS.
        
        Args:
            doc_id (str): Document ID
            
        Returns:
            Dict: Document content
        """
        blob_name = f"docs/{doc_id}.json"
        blob = self.bucket.blob(blob_name)
        
        try:
            # Download content
            content = blob.download_as_string()
            return json.loads(content)
        except:
            print(f"⚠️ Document {doc_id} not found in {blob_name}")
            return None
    
    def get_chunks(self, doc_id: str) -> List[Dict]:
        """
        Retrieve all chunks for a document.
        
        Args:
            doc_id (str): Document ID
            
        Returns:
            List[Dict]: Document chunks
        """
        chunks = []
        prefix = f"chunks/{doc_id}_chunk_"
        
        # List all blobs with the prefix
        blobs = self.client.list_blobs(self.bucket_name, prefix=prefix)
        
        for blob in blobs:
            # Download content
            content = blob.download_as_string()
            chunks.append(json.loads(content))
        
        # Sort chunks by index
        chunks.sort(key=lambda c: c.get("metadata", {}).get("chunk_index", 0))
        
        return chunks