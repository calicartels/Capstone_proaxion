# ProAxion RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot system for ProAxion, designed to answer questions about sensor installation and maintenance using knowledge from Google Docs.

## Overview

This chatbot uses a RAG architecture to provide accurate, knowledge-grounded responses about sensor installation procedures. The system:

1. Retrieves documents from Google Docs
2. Chunks and indexes them for efficient retrieval
3. Retrieves relevant context based on user queries
4. Generates helpful responses using Google's Vertex AI Gemini models

## System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│                 │    │                 │    │                 │
│  React Frontend │───▶│  FastAPI Server │───▶│  Google Vertex  │
│                 │◀───│                 │◀───│        AI       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │   ▲
                              │   │
                              ▼   │
                        ┌─────────────────┐
                        │                 │
                        │  Google Docs &  │
                        │      Drive      │
                        │                 │
                        └─────────────────┘
```

## Directory Structure

- `api/` - FastAPI server implementation
- `config/` - Configuration settings
- `credentials/` - OAuth and service account credentials
- `rag/` - Core RAG components (retrieval, generation)
- `utils/` - Helper utilities for authentication and document processing

## Installation

### Prerequisites

- Python 3.9+
- Google Cloud account with Vertex AI API enabled
- Google OAuth credentials for Docs/Drive access
- Google service account credentials for Vertex AI

### Setup

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up credentials:
   - Place Google service account key in `credentials/` directory
   - Place OAuth client credentials in `credentials/` directory
   - Update filenames in `config/settings.py` if needed

## Configuration

All configuration is managed in `config/settings.py`:

- `PROJECT_ID` - Google Cloud project ID
- `KNOWLEDGE_DOCUMENT_IDS` - List of Google Doc IDs to use as knowledge sources
- `API_HOST/PORT` - API server settings
- `CORS_ORIGINS` - Allowed origins for CORS
- Model configuration and RAG parameters

## Usage

### Indexing Documents

Before using the chatbot, index your knowledge documents:

```bash
python main.py --index
```

Or index specific documents:

```bash
python main.py --index --documents "doc_id_1" "doc_id_2"
```

### Running the API Server

Start the API server:

```bash
python main.py --run-api
```

The server will be available at http://localhost:8000 by default.

## API Endpoints

- `POST /api/chat` - Send a chat message and get a response
- `POST /api/index-document` - Index a new document
- `GET /health` - Check API health

## Authentication

The system uses two types of authentication:

1. **OAuth 2.0** for Google Docs/Drive API access (interactive login flow)
2. **Service Account** for Vertex AI access

When first running the system, you'll be prompted to authenticate with Google to access Docs/Drive.

## Development

### Adding New Knowledge Sources

1. Add new Google Doc IDs to `KNOWLEDGE_DOCUMENT_IDS` in `config/settings.py`
2. Run indexing with `python main.py --index`

### Modifying the Response Generation

To customize how responses are generated, modify the `Generator` class in `rag/generator.py`.

## Troubleshooting

- **Authentication errors**: Ensure credentials files exist and have correct permissions
- **Document retrieval errors**: Verify document IDs and that your account has access
- **Vertex AI errors**: Check that your service account has the Vertex AI User role

## License

Proprietary - For ProAxion use only 