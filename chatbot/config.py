import os
import glob

# Project settings
PROJECT_ID = "capstone-449418"  # Your GCP project ID
LOCATION = "us-central1"        # Update if using a different region

# Base directory is relative to the application
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Storage directories
DATA_DIR = os.path.join(BASE_DIR, "data")
DOCS_DIR = os.path.join(DATA_DIR, "docs")
IMAGES_DIR = os.path.join(DATA_DIR, "images")
STRUCTURED_DIR = os.path.join(DATA_DIR, "structured")
CREDENTIALS_DIR = os.path.join(BASE_DIR, "credentials")

# Find credentials files
# Service account key (for Vertex AI, Storage, Firestore)
SERVICE_ACCOUNT_KEY = os.environ.get(
    "GOOGLE_APPLICATION_CREDENTIALS", 
    os.path.join(CREDENTIALS_DIR, "capstone-449418-6577c3f0fefc.json")
)

# Find OAuth client credentials (for Google Docs & Drive)
client_secret_pattern = os.path.join(CREDENTIALS_DIR, "client_secret_*.json")
client_secret_files = glob.glob(client_secret_pattern)
OAUTH_CREDENTIALS_FILE = client_secret_files[0] if client_secret_files else None

# Vertex AI model settings - UPDATED TO USE AVAILABLE MODELS
LLM_MODEL = "gemini-pro"           # Standard text model
TEXT_MODEL = "gemini-pro"          # Standard text model
MULTIMODAL_MODEL = "gemini-pro-vision"  # For image captioning

# Flag to enable/disable multimodal processing
ENABLE_MULTIMODAL = True   # Set to False to skip image captioning if models unavailable

# Document processing settings
MAX_TOKENS_PER_CHUNK = 8000    # Maximum context size for LLM processing
IMAGE_QUALITY = 70             # JPEG quality for extracted images (0-100)

# Ensure all necessary directories exist
for dir_path in [DOCS_DIR, IMAGES_DIR, STRUCTURED_DIR, CREDENTIALS_DIR]:
    os.makedirs(dir_path, exist_ok=True)

print(f"Service Account Key: {SERVICE_ACCOUNT_KEY}")
print(f"OAuth Credentials: {OAUTH_CREDENTIALS_FILE}")