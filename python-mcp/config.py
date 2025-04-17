#!/usr/bin/env python3
"""
Configuration module for Outlook MCP server
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Server information
SERVER_NAME = "outlook-mcp"
SERVER_VERSION = "1.0.0"

# Test mode (set via environment variable or default to False)
USE_TEST_MODE = os.getenv('USE_TEST_MODE', 'false').lower() == 'true'

# Microsoft Graph API configuration
GRAPH_API_ENDPOINT = "https://graph.microsoft.com/v1.0/"
MAX_RESULT_COUNT = 50

# Email fields to retrieve
EMAIL_SELECT_FIELDS = "id,subject,from,toRecipients,receivedDateTime,bodyPreview,isRead,importance,hasAttachments"
EMAIL_DETAIL_FIELDS = "id,subject,from,toRecipients,ccRecipients,bccRecipients,receivedDateTime,body,bodyPreview,isRead,importance,hasAttachments"

# Authentication configuration
AUTH_CONFIG = {
    "clientId": os.getenv("MS_CLIENT_ID", ""),
    "authServerUrl": os.getenv("AUTH_SERVER_URL", "http://localhost:3000"),
    "tokenStorePath": os.path.expanduser(
        os.getenv("TOKEN_STORE_PATH", "~/.outlook-mcp/tokens.json")
    )
}

# Ensure token directory exists
token_dir = Path(AUTH_CONFIG["tokenStorePath"]).parent
token_dir.mkdir(parents=True, exist_ok=True)