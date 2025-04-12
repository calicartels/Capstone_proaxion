"""
Configuration settings for the chatbot RAG system.
"""
import os

# Google Cloud Project configuration
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "capstone-449418")
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

# Directory paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CREDENTIALS_DIR = os.path.join(BASE_DIR, "credentials")

# Edit chatbot_rag/config/settings.py to match your filenames
SERVICE_ACCOUNT_KEY = os.environ.get(
    "GOOGLE_APPLICATION_CREDENTIALS", 
    os.path.join(CREDENTIALS_DIR, "capstone-449418-38bd0569f608.json")  # Updated filename
)

# OAuth client credentials (for Google Docs & Drive)
OAUTH_CREDENTIALS_FILE = os.environ.get(
    "OAUTH_CREDENTIALS_FILE",
    os.path.join(CREDENTIALS_DIR, "client_secret_695116221974-hqg9ap5bh4ok0nc23bbbkh8h30nhqa8d.apps.googleusercontent.com.json")  # Updated filename
)

# Vertex AI model settings
# Update Vertex AI model settings
TEXT_MODEL = os.environ.get("TEXT_MODEL", "gemini-1.0-pro") 
MULTIMODAL_MODEL = os.environ.get("MULTIMODAL_MODEL", "gemini-2.0-flash-001")

# Google Document IDs (list of document IDs to use as knowledge sources)
KNOWLEDGE_DOCUMENT_IDS = [
    "1k1I7_tVuTaRePPTirBd8qybUFxQlemVqsr0SFlXo4RU",  # Sensor Placement Guide
    # Add more document IDs as needed
]

GCS_BUCKET_NAME = "proaxionsample"
GCS_PREFIX = "sample/Videos"

# API Settings
API_HOST = os.environ.get("API_HOST", "0.0.0.0")
API_PORT = int(os.environ.get("API_PORT", 8000))
CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173,http://localhost:5174").split(",")

# RAG settings
MAX_CONTEXT_LENGTH = 4000  # Maximum number of tokens for context
SIMILARITY_THRESHOLD = 0.75  # Minimum similarity score for retrieval
MODEL_TEMPERATURE = 1.0 