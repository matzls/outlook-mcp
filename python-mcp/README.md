# Python MCP Server for Outlook

This is a Model Context Protocol (MCP) server implementation that provides access to Microsoft Outlook through the Microsoft Graph API. This server allows AI assistants to interact with Outlook email, folders, and rules.

## Features

- **Authentication**: Authenticate with Microsoft Graph API
- **Email Operations**: List, search, read, and send emails
- **Folder Management**: List folders, create folders, and move emails between folders
- **Rules Management**: List, create, and modify inbox rules

## Installation

1. Clone the repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up environment variables (create a `.env` file):

```
MS_CLIENT_ID=your_microsoft_client_id
AUTH_SERVER_URL=http://localhost:3000
TOKEN_STORE_PATH=~/.outlook-mcp/tokens.json
USE_TEST_MODE=false
```

## Usage

Run the server:

```bash
python server.py
```

For test mode, set the environment variable:

```bash
USE_TEST_MODE=true python server.py
```

## Available Tools

### Authentication Tools
- `about`: Get information about the server
- `authenticate`: Authenticate with Microsoft Graph API
- `check-auth-status`: Check current authentication status

### Email Tools
- `list-emails`: List emails from any folder
- `search-emails`: Search for emails with various criteria
- `read-email`: Read the full content of an email
- `send-email`: Compose and send a new email

### Folder Tools
- `list-folders`: List mail folders in your account
- `create-folder`: Create a new mail folder
- `move-emails`: Move emails between folders

### Rules Tools
- `list-rules`: List inbox rules
- `create-rule`: Create a new inbox rule
- `edit-rule-sequence`: Change the execution order of a rule

## Development

This is a Python port of a JavaScript MCP server. The code is organized into modules:

- `auth/`: Authentication and token management
- `email/`: Email operations
- `folder/`: Folder management
- `rules/`: Rules management
- `utils/`: Utility functions for API calls and data formatting

## Testing

For testing without connecting to actual Microsoft services, use test mode:

```bash
USE_TEST_MODE=true python server.py
```

This will simulate API responses with mock data.

## License

MIT