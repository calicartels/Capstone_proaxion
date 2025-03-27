# debug_index.py
from rag.document_store import DocumentStore
from utils.docs_service import DocsProcessor
from utils.auth import setup_vertex_ai
import os

# Initialize components
credentials = setup_vertex_ai()
docs_processor = DocsProcessor()
document_store = DocumentStore()

# Document ID to index
doc_id = "1k1I7_tVuTaRePPTirBd8qybUFxQlemVqsr0SFlXo4RU"

# Retrieve and process the document
print(f"Retrieving document: {doc_id}")
document = docs_processor.get_document_content(doc_id)

if "error" in document:
    print(f"Error retrieving document: {document['error']}")
    exit(1)

# Store the document
print("Storing document...")
document_store.store_document(doc_id, document)

# Create and store chunks
print("Creating chunks...")
chunks = docs_processor.extract_chunks(document)
print(f"Generated {len(chunks)} chunks")

# Store chunks
print("Storing chunks...")
document_store.store_chunks(doc_id, chunks)

print("Indexing complete!")