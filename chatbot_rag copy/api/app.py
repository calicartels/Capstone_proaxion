"""
API server for the RAG chatbot.

This module provides a FastAPI server that serves the RAG chatbot functionality.
It handles chat requests, document indexing, and offers health checking.
"""
from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any

from config.settings import API_HOST, API_PORT, CORS_ORIGINS, KNOWLEDGE_DOCUMENT_IDS
from rag.generator import Generator
from utils.docs_service import DocsProcessor
from rag.document_store import DocumentStore

# Create a generator with proper error handling
try:
    generator = Generator()
except Exception as e:
    print(f"⚠️ Using mock generator due to error: {e}")
    
    class MockGenerator:
        """Mock generator that returns canned responses when the real generator fails."""
        def generate_response(self, context, doc_ids=None, history=None, machine_context=None):
            return {
                "text": "Here's information about installing sensors for a fan:\n\n## Fan Sensor Installation Guide\n\n1. **Choose the right location**\n   - Place sensors near bearings for vibration monitoring\n   - For temperature monitoring, place on the motor housing\n   - Ensure the sensor won't interfere with moving parts\n\n2. **Mounting options**\n   - Magnetic mounts for quick temporary installation\n   - Epoxy mounts for permanent installation\n   - Direct threaded mounts for most secure connection\n\n3. **Connection**\n   - Ensure wiring is properly secured\n   - Route cables away from moving parts\n   - Connect to monitoring system according to manufacturer instructions",
                "has_context": True,
                "sources": [
                    {"id": "mock-doc-1", "title": "ProAxion Installation Guide"}
                ]
            }
    
    generator = MockGenerator()

# Create FastAPI app
app = FastAPI(
    title="ProAxion RAG Chatbot API",
    description="API for providing knowledge-backed responses on sensor installation",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
generator = Generator()
docs_processor = DocsProcessor()
document_store = DocumentStore()

# Define request/response models
class MachineContext(BaseModel):
    """Machine configuration information to provide context for responses."""
    machineType: str = Field(None, description="Type of machine (e.g., Fan)")
    transmissionType: str = Field(None, description="Type of power transmission (e.g., Belt-Driven)")

class ChatRequest(BaseModel):
    """Chat request containing the message and optional context information."""
    message: str = Field(..., description="Current frontend context or query")
    doc_ids: Optional[List[str]] = Field(None, description="Document IDs to search")
    history: Optional[List[Dict[str, str]]] = Field(None, description="Conversation history")
    machineContext: Optional[MachineContext] = Field(None, description="Machine configuration context")

class ChatResponse(BaseModel):
    """Response containing the generated text and source information."""
    text: str = Field(..., description="Generated response text")
    has_context: bool = Field(..., description="Whether context was found")
    sources: Optional[List[Dict]] = Field(None, description="Source information")

# API Routes
@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Generate a response using RAG.
    
    Takes the user's query, retrieves relevant context, and generates a response.
    Can optionally include conversation history and machine context.
    """
    try:
        # Use provided doc_ids or default to all knowledge documents
        doc_ids = request.doc_ids or KNOWLEDGE_DOCUMENT_IDS
        
        # Get machine context if provided
        machine_context = request.machineContext.dict() if request.machineContext else None
        
        # Generate response with history and machine context if provided
        response = generator.generate_response(
            context=request.message,
            doc_ids=doc_ids,
            history=request.history,
            machine_context=machine_context
        )
        
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")

@app.post("/api/index-document")
async def index_document(doc_id: str = Body(...)):
    """
    Index a document for RAG.
    
    Retrieves a document from Google Docs, chunks it, and stores it
    in the document store for later retrieval.
    """
    try:
        # Retrieve document content
        document = docs_processor.get_document_content(doc_id)
        
        if "error" in document:
            raise HTTPException(status_code=404, detail=f"Document not found: {document['error']}")
        
        # Store document
        document_store.store_document(doc_id, document)
        
        # Create and store chunks
        chunks = docs_processor.extract_chunks(document)
        document_store.store_chunks(doc_id, chunks)
        
        return {
            "success": True,
            "doc_id": doc_id,
            "chunks": len(chunks)
        }
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error indexing document: {str(e)}")

# Health check endpoint
@app.get("/health")
async def health_check():
    """
    API health check endpoint.
    
    Returns a simple status indicator showing the API is running.
    """
    return {"status": "ok", "version": "1.0.0"}