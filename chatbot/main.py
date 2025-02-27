#!/usr/bin/env python3
"""
ProAxion Tactix - Intelligent Document Processor
Main application for processing Google Docs into structured knowledge.
"""
import os
import argparse
import json
from pprint import pprint

# Import utility modules
from utils.auth import setup_vertex_ai, get_docs_service, get_drive_service, get_storage_client, get_firestore_client
# from utils.auth_switcher import get_docs_service, get_drive_service
from utils.docs_parser import DocParser
from utils.llm_processor import LLMProcessor
from utils.storage import StorageManager
from utils.kb_integration import KnowledgeBaseManager

# Import configuration
from config import PROJECT_ID, STRUCTURED_DIR

def process_document(doc_url, use_cloud=False, build_kb=True):
    """
    Process a Google Doc URL into structured knowledge.
    
    Args:
        doc_url (str): Google Docs URL
        use_cloud (bool): Whether to use cloud storage
        build_kb (bool): Whether to build a comprehensive knowledge base
        
    Returns:
        str: ID of the processed document
    """
    print(f"\n📄 Processing document: {doc_url}")
    
    # Step 1: Setup authentication
    print("\n🔑 Setting up authentication...")
    service_account_credentials = setup_vertex_ai()
    
    # Step 2: Initialize services with fallback methods
    print("\n🔧 Initializing services...")
    docs_service = get_docs_service()
    if not docs_service:
        print("❌ Could not authenticate with Google Docs API")
        return None
        
    drive_service = get_drive_service()
    if not drive_service:
        print("❌ Could not authenticate with Google Drive API")
        return None
    
    storage_client = None
    firestore_client = None
    if use_cloud:
        storage_client = get_storage_client()
        firestore_client = get_firestore_client()
    
    # Step 3: Initialize components
    doc_parser = DocParser(docs_service, drive_service)
    llm_processor = LLMProcessor()
    storage_manager = StorageManager(storage_client, firestore_client)
    kb_manager = KnowledgeBaseManager()
    
    # Step 4: Extract document content
    print("\n📑 Extracting document content...")
    doc_content = doc_parser.extract_doc_from_url(doc_url)
    
    if not doc_content:
        print("❌ Failed to extract document content")
        return None
    
    print(f"✓ Extracted {len(doc_content['elements'])} elements from document: {doc_content['title']}")
    
    # Step 5: Analyze document structure
    print("\n🔍 Analyzing document structure with LLM...")
    document_structure = llm_processor.analyze_document_structure(doc_content['elements'])
    
    # Step 6: Process images with captions
    print("\n🖼️ Generating image captions...")
    image_elements = [el for el in doc_content['elements'] if el['type'] == 'image']
    print(f"Found {len(image_elements)} images in document")
    
    if image_elements:
        enhanced_images = llm_processor.generate_image_captions(image_elements, doc_content['elements'])
        print(f"✓ Generated captions for {len(enhanced_images)} images")
    else:
        enhanced_images = []
        print("No images found to caption")
    
    # Step 7: Create structured knowledge
    print("\n🧠 Creating structured knowledge base...")
    structured_data = llm_processor.structure_document_to_json(document_structure, enhanced_images)
    
    # Validate essential data is present
    if not _check_essential_data(structured_data):
        print("⚠️ Warning: Document processing did not extract all essential data.")
        print("⚠️ The knowledge base builder will attempt to fill in missing information.")
    
    # Add document metadata
    structured_data['title'] = doc_content['title']
    structured_data['source_url'] = doc_url
    structured_data['processed_date'] = doc_content['extracted_on']
    
    # Add document metadata
    structured_data['title'] = doc_content['title']
    structured_data['source_url'] = doc_url
    structured_data['processed_date'] = doc_content['extracted_on']
    
    # Step 8: Save structured data
    print("\n💾 Saving structured data...")
    doc_id = storage_manager.save_structured_data(structured_data)
    
    # Step 9: Upload images to cloud if using cloud storage
    if use_cloud and enhanced_images:
        print("\n☁️ Uploading images to cloud storage...")
        for img in enhanced_images:
            local_path = os.path.join('data/images', img['filename'])
            if os.path.exists(local_path):
                img['cloud_url'] = storage_manager.upload_image_to_cloud(local_path)
        
        # Update structured data with cloud URLs
        structured_data['images'] = enhanced_images
        doc_id = storage_manager.save_structured_data(structured_data, doc_id)
    
    print(f"\n✅ Document processing complete! Document ID: {doc_id}")
    
    # Step 10: Build comprehensive knowledge base (optional)
    if build_kb:
        print("\n💡 Building comprehensive knowledge base...")
        kb_manager = KnowledgeBaseManager()
        try:
            kb_id = kb_manager.process_document_completion(doc_id)
            if kb_id:
                print(f"\n💡 To view the comprehensive knowledge base, run: python main.py view {kb_id}")
        except AttributeError as e:
            print(f"\n⚠️ Warning: {e}")
            print("⚠️ Attempting alternative method...")
            kb_id = kb_manager.build_kb(doc_id)
            if kb_id:
                print(f"\n💡 To view the comprehensive knowledge base, run: python main.py view {kb_id}")
    else:
        print(f"\n💡 To view this document, run: python main.py view {doc_id}")
    
    return doc_id


def list_documents():
    """List all processed documents."""
    # Initialize storage manager
    storage_manager = StorageManager()
    
    # Get list of documents
    docs = storage_manager.list_all_documents()
    
    if not docs:
        print("📂 No processed documents found.")
        print("💡 Process a document first using: python main.py process <google-docs-url>")
        return []
    
    print(f"📂 Found {len(docs)} processed documents:")
    for i, doc in enumerate(docs, 1):
        print(f"{i}. ID: {doc['id']}")
        print(f"   Title: {doc['title']}")
        print(f"   Created: {doc['created_at']}")
        print()
    
    return docs

def view_document(doc_id):
    """
    View a processed document.
    
    Args:
        doc_id (str): Document ID to view
    """
    # Initialize storage manager
    storage_manager = StorageManager()
    
    # Get document data
    doc_data = storage_manager.load_structured_data(doc_id)
    
    if not doc_data:
        print(f"❌ Document with ID {doc_id} not found")
        print("💡 List available documents using: python main.py list")
        return
    
    # Print document metadata
    print(f"📄 Document: {doc_data.get('title', 'Untitled')}")
    print(f"🔗 Source: {doc_data.get('source_url', 'Unknown')}")
    print(f"⏱️ Processed: {doc_data.get('processed_date', 'Unknown')}")
    print("\n📊 Structured Content:")
    
    # Pretty print with better JSON formatting
    content = {k: v for k, v in doc_data.items() if not k.startswith('_') and k not in ['title', 'source_url', 'processed_date']}
    print(json.dumps(content, indent=2))

def build_kb():
    """Build a comprehensive knowledge base from all processed documents."""
    kb_manager = KnowledgeBaseManager()
    kb_id = kb_manager.kb_builder.build_comprehensive_kb()
    
    if kb_id:
        print(f"\n💡 To view the comprehensive knowledge base, run: python main.py view {kb_id}")
    
    return kb_id

def _check_essential_data(data):
    """Check if structured data contains all essential components."""
    # Check for machine types or configurations
    has_machine_types = "machine_types" in data and data["machine_types"]
    has_configurations = "configurations" in data and data["configurations"]
    
    # Check for sensor placement
    has_sensor_placement = "sensor_placement" in data and data["sensor_placement"]
    
    # Check for installation methods
    has_installation = "installation_methods" in data and data["installation_methods"]
    
    return has_machine_types and has_configurations and has_sensor_placement and has_installation

def main():
    """Main function to parse arguments and execute commands."""
    parser = argparse.ArgumentParser(description="ProAxion Tactix Document Processor")
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Process document command
    process_parser = subparsers.add_parser("process", help="Process a Google Doc")
    process_parser.add_argument("url", help="Google Docs URL to process")
    process_parser.add_argument("--cloud", action="store_true", help="Use cloud storage")
    process_parser.add_argument("--no-kb", action="store_true", help="Don't build comprehensive knowledge base")
    
    # List documents command
    subparsers.add_parser("list", help="List processed documents")
    
    # View document command
    view_parser = subparsers.add_parser("view", help="View a processed document")
    view_parser.add_argument("id", help="Document ID to view")
    
    # Build KB command
    subparsers.add_parser("build-kb", help="Build comprehensive knowledge base")
    
    args = parser.parse_args()
    
    if args.command == "process":
        process_document(args.url, args.cloud, not args.no_kb)
    elif args.command == "list":
        list_documents()
    elif args.command == "view":
        view_document(args.id)
    elif args.command == "build-kb":
        build_kb()
    else:
        parser.print_help()
        print("\n💡 To get started, try processing a Google Doc:")
        print("   python main.py process \"https://docs.google.com/document/d/your-doc-id/edit\"")

if __name__ == "__main__":
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'  # For development only
    main()