"""
Authentication utilities for Google Cloud services.
"""
import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2.service_account import Credentials as ServiceAccountCredentials
from google_auth_oauthlib.flow import InstalledAppFlow
import vertexai
from google.cloud import storage
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from config.settings import PROJECT_ID, LOCATION, SERVICE_ACCOUNT_KEY, OAUTH_CREDENTIALS_FILE, CREDENTIALS_DIR

# Define scopes needed for Google Docs and Drive
SCOPES = ['https://www.googleapis.com/auth/documents.readonly',
          'https://www.googleapis.com/auth/drive.readonly']

def setup_vertex_ai():
    """
    Set up Google Cloud authentication and initialize Vertex AI using service account.
    
    Returns:
        Credentials: The service account credentials
    """
    if os.path.exists(SERVICE_ACCOUNT_KEY):
        credentials = ServiceAccountCredentials.from_service_account_file(
            SERVICE_ACCOUNT_KEY,
            scopes=['https://www.googleapis.com/auth/cloud-platform']
        )
        
        # Initialize Vertex AI with credentials
        vertexai.init(project=PROJECT_ID, location=LOCATION, credentials=credentials)
        print(f"✓ Initialized Vertex AI with service account from {SERVICE_ACCOUNT_KEY}")
        return credentials
    else:
        # Use application default credentials as fallback
        vertexai.init(project=PROJECT_ID, location=LOCATION)
        print("⚠️ Using application default credentials for Vertex AI")
        return None

def get_docs_drive_credentials():
    """
    Get user credentials for Google Docs and Drive APIs using OAuth.
    
    Returns:
        Credentials: User's OAuth credentials
    """
    creds = None
    # Token file stores the user's access and refresh tokens
    token_file = os.path.join(CREDENTIALS_DIR, 'token.json')
    
    # Check if we have saved token
    if os.path.exists(token_file):
        try:
            creds = Credentials.from_authorized_user_info(
                json.load(open(token_file)), SCOPES)
            print("✓ Loaded saved Google Docs/Drive credentials")
        except Exception as e:
            print(f"⚠️ Error loading saved credentials: {e}")
    
    # If credentials don't exist or are invalid, let user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                print("✓ Refreshed Google Docs/Drive credentials")
            except Exception as e:
                print(f"⚠️ Error refreshing credentials: {e}")
                creds = None
        
        if not creds:
            # Check if credentials file exists
            if not os.path.exists(OAUTH_CREDENTIALS_FILE):
                raise FileNotFoundError(
                    f"OAuth credentials file not found at {OAUTH_CREDENTIALS_FILE}. "
                    "Please download OAuth 2.0 Client ID credentials from Google Cloud Console."
                )
            
            print(f"🔑 Using OAuth client credentials from {OAUTH_CREDENTIALS_FILE}")
            flow = InstalledAppFlow.from_client_secrets_file(OAUTH_CREDENTIALS_FILE, SCOPES)
            print("🌐 Opening browser for Google authentication. Please log in and grant permissions...")
            creds = flow.run_local_server(port=0)
            print("✓ Authentication successful!")
        
        # Save the credentials for the next run
        with open(token_file, 'w') as token:
            token.write(creds.to_json())
            print(f"💾 Saved authentication token to {token_file}")
    
    return creds

def get_docs_service():
    """
    Create and return a Google Docs API service using OAuth authentication.
    
    Returns:
        Resource: Google Docs API service resource.
    """
    try:
        creds = get_docs_drive_credentials()
        service = build('docs', 'v1', credentials=creds)
        print("✓ Successfully created Google Docs service")
        return service
    except HttpError as error:
        print(f"❌ Error with Google Docs API: {error}")
        return None