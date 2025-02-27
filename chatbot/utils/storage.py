# GCS utilities
"""
Utilities for storing and retrieving structured data and media.
"""
import os
import json
import uuid
import datetime

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import STRUCTURED_DIR, IMAGES_DIR

class StorageManager:
    """Manage storage of structured data and media files."""
    
    def __init__(self, storage_client=None, firestore_client=None):
        """
        Initialize the storage manager.
        
        Args:
            storage_client: Google Cloud Storage client (optional)
            firestore_client: Google Cloud Firestore client (optional)
        """
        self.storage_client = storage_client
        self.firestore_client = firestore_client
        self.use_cloud = storage_client is not None and firestore_client is not None
    
    def save_structured_data(self, data, doc_id=None):
        """
        Save structured data to storage.
        
        Args:
            data (dict): Structured data to save
            doc_id (str, optional): Document ID to use as reference
            
        Returns:
            str: ID of the saved data
        """
        # Generate a unique ID if none provided
        if not doc_id:
            doc_id = f"doc_{uuid.uuid4().hex[:8]}_{datetime.datetime.now().strftime('%Y%m%d')}"
        
        # Add metadata
        data['_metadata'] = {
            'id': doc_id,
            'created_at': datetime.datetime.now().isoformat(),
            'version': '1.0'
        }
        
        if self.use_cloud:
            # Save to Firestore
            doc_ref = self.firestore_client.collection('structured_data').document(doc_id)
            doc_ref.set(data)
            print(f"Saved structured data to Firestore with ID: {doc_id}")
        else:
            # Save to local file
            file_path = os.path.join(STRUCTURED_DIR, f"{doc_id}.json")
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"Saved structured data to: {file_path}")
        
        return doc_id
    
    def load_structured_data(self, doc_id):
        """
        Load structured data from storage.
        
        Args:
            doc_id (str): ID of the data to load
            
        Returns:
            dict: The loaded structured data
        """
        if self.use_cloud:
            # Load from Firestore
            doc_ref = self.firestore_client.collection('structured_data').document(doc_id)
            doc = doc_ref.get()
            if doc.exists:
                return doc.to_dict()
            else:
                print(f"No data found with ID: {doc_id}")
                return None
        else:
            # Load from local file
            file_path = os.path.join(STRUCTURED_DIR, f"{doc_id}.json")
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    return json.load(f)
            else:
                print(f"No data found at: {file_path}")
                return None
    
    def upload_image_to_cloud(self, local_path, remote_path=None):
        """
        Upload an image to cloud storage.
        
        Args:
            local_path (str): Local path to the image
            remote_path (str, optional): Remote path in cloud storage
            
        Returns:
            str: Public URL of the uploaded image
        """
        if not self.use_cloud:
            print("Cloud storage client not initialized")
            return local_path
        
        try:
            bucket_name = f"{self.storage_client.project}-tactix-media"
            bucket = self.storage_client.bucket(bucket_name)
            
            # Create bucket if it doesn't exist
            if not bucket.exists():
                bucket = self.storage_client.create_bucket(bucket_name)
                print(f"Created bucket: {bucket_name}")
            
            # Use filename as remote path if not specified
            if not remote_path:
                remote_path = os.path.basename(local_path)
            
            # Add images/ prefix to keep files organized
            if not remote_path.startswith('images/'):
                remote_path = f"images/{remote_path}"
            
            # Upload the file
            blob = bucket.blob(remote_path)
            blob.upload_from_filename(local_path)
            
            # Make the blob publicly readable
            blob.make_public()
            
            print(f"Uploaded {local_path} to {remote_path}")
            return blob.public_url
        
        except Exception as e:
            print(f"Error uploading image to cloud: {e}")
            return local_path
    
    def list_all_documents(self):
        """
        List all available structured documents.
        
        Returns:
            list: List of document IDs and metadata
        """
        if self.use_cloud:
            # List from Firestore
            docs = []
            query = self.firestore_client.collection('structured_data').stream()
            
            for doc in query:
                data = doc.to_dict()
                metadata = data.get('_metadata', {})
                docs.append({
                    'id': doc.id,
                    'created_at': metadata.get('created_at', 'Unknown'),
                    'title': data.get('title', 'Untitled Document')
                })
            
            return docs
        else:
            # List from local files
            docs = []
            for filename in os.listdir(STRUCTURED_DIR):
                if filename.endswith('.json'):
                    file_path = os.path.join(STRUCTURED_DIR, filename)
                    with open(file_path, 'r') as f:
                        try:
                            data = json.load(f)
                            metadata = data.get('_metadata', {})
                            docs.append({
                                'id': metadata.get('id', filename.replace('.json', '')),
                                'created_at': metadata.get('created_at', 'Unknown'),
                                'title': data.get('title', 'Untitled Document')
                            })
                        except json.JSONDecodeError:
                            print(f"Error decoding JSON from {filename}")
            
            return docs