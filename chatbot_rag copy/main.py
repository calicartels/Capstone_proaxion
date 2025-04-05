"""
Entry point for the RAG chatbot system.

This script serves as the main entry point for the ProAxion RAG chatbot system.
It offers two main functionalities:
1. Indexing documents from Google Docs for the RAG system
2. Running the API server for the chatbot

Run with --help for usage information.
"""
import argparse
import os
from pathlib import Path
import uvicorn

from config.settings import API_HOST, API_PORT, KNOWLEDGE_DOCUMENT_IDS
from utils.auth import setup_vertex_ai
from utils.docs_service import DocsProcessor
from rag.document_store import DocumentStore


def ensure_credentials_dir():
    """
    Ensure the credentials directory exists.
    
    Returns:
        Path: Path to the credentials directory
    """
    creds_dir = Path(__file__).parent / "credentials"
    creds_dir.mkdir(exist_ok=True)
    return creds_dir


def index_documents(doc_ids=None):
    """
    Index documents for RAG.
    
    Process documents from Google Docs, extract their content,
    and store them in the document store for retrieval.
    
    Args:
        doc_ids (List[str], optional): Document IDs to index. 
                                    If None, index all configured documents.
    """
    # Initialize components
    setup_vertex_ai()
    docs_processor = DocsProcessor()
    document_store = DocumentStore()
    
    # Use provided doc_ids or default to all knowledge documents
    doc_ids = doc_ids or KNOWLEDGE_DOCUMENT_IDS
    
    # Process each document
    for doc_id in doc_ids:
        print(f"Indexing document: {doc_id}")
        
        # Retrieve document content
        document = docs_processor.get_document_content(doc_id)
        
        if "error" in document:
            print(f"⚠️ Error retrieving document {doc_id}: {document['error']}")
            continue
        
        # Store document
        document_store.store_document(doc_id, document)
        
        # Create and store chunks
        chunks = docs_processor.extract_chunks(document)
        document_store.store_chunks(doc_id, chunks)
        
        print(f"✓ Indexed document {doc_id} with {len(chunks)} chunks")


def run_api():
    """
    Run the API server.
    
    Starts the FastAPI server with Uvicorn on the configured host and port.
    """
    # Import here to avoid circular imports
    from api.app import app
    
    print(f"Starting API server at http://{API_HOST}:{API_PORT}")
    # Start the server
    uvicorn.run(app, host=API_HOST, port=API_PORT)


if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="ProAxion RAG Chatbot")
    parser.add_argument("--index", action="store_true", help="Index documents")
    parser.add_argument("--documents", nargs="+", help="Document IDs to index")
    parser.add_argument("--run-api", action="store_true", help="Run the API server")
    
    args = parser.parse_args()
    
    # Ensure credentials directory exists
    ensure_credentials_dir()
    
    # Initialize Vertex AI
    setup_vertex_ai()
    
    # Run requested operation
    if args.index:
        index_documents(args.documents)
    
    if args.run_api:
        run_api()
    
    # If no operation specified, show help
    if not (args.index or args.run_api):
        parser.print_help()