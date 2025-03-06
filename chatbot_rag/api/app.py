"""
API server for the RAG chatbot.
"""
from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
import uvicorn

from config.settings import API_HOST, API_PORT, CORS_ORIGINS, KNOWLEDGE_DOCUMENT_IDS
from rag.generator import Generator
from utils.docs_service import DocsProcessor
from rag.document_store import DocumentStore



try:
    from rag.generator import Generator
    generator = Generator()
except Exception as e:
    print(f"Using mock generator due to error: {e}")
    
    class MockGenerator:
        def generate_response(self, context, doc_ids=None, history=None):
            return {
                "text": "Here's information about installing sensors for a fan:\n\n## Fan Sensor Installation Guide\n\n1. **Choose the right location**\n   - Place sensors near bearings for vibration monitoring\n   - For temperature monitoring, place on the motor housing\n   - Ensure the sensor won't interfere with moving parts\n\n2. **Mounting options**\n   - Magnetic mounts for quick temporary installation\n   - Epoxy mounts for permanent installation\n   - Direct threaded mounts for most secure connection\n\n3. **Connection**\n   - Ensure wiring is properly secured\n   - Route cables away from moving parts\n   - Connect to monitoring system according to manufacturer instructions",
                "has_context": True,
                "sources": [
                    {"id": "mock-doc-1", "title": "ProAxion Installation Guide"}
                ]
            }
    
    generator = MockGenerator()

# Create FastAPI app
app = FastAPI(title="ProAxion RAG Chatbot API")

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
class ChatRequest(BaseModel):
    message: str = Field(..., description="Current frontend context or query")
    doc_ids: Optional[List[str]] = Field(None, description="Document IDs to search")
    history: Optional[List[Dict[str, str]]] = Field(None, description="Conversation history")

class ChatResponse(BaseModel):
    text: str = Field(..., description="Generated response text")
    has_context: bool = Field(..., description="Whether context was found")
    sources: Optional[List[Dict]] = Field(None, description="Source information")

# Routes
@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Generate a response using RAG."""
    # Use provided doc_ids or default to all knowledge documents
    doc_ids = request.doc_ids or KNOWLEDGE_DOCUMENT_IDS
    
    # Generate response with history if provided
    response = generator.generate_response(
        context=request.message,
        doc_ids=doc_ids,
        history=request.history
    )
    
    return response
@app.post("/api/index-document")
async def index_document(doc_id: str = Body(...)):
    """
    Index a document for RAG.
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "ok"}