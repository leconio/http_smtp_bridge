# SMTP Bridge

HTTP to SMTP proxy service built with FastAPI, providing a RESTful API for sending emails.

**Current Version**: v1.0.7
**Docker Image**: `ghcr.io/leconio/http_smtp_bridge:latest`
**Image Size**: ~85MB (Alpine-based)

## Features

- 🚀 RESTful API for sending emails via SMTP
- 📧 Support for HTML and plain text emails
- 📎 File attachments support (base64 encoded)
- 🔐 API key authentication
- 🛡️ Rate limiting protection
- 🌐 CORS support
- ⚡ Production-ready with Gunicorn + Uvicorn workers
- 🐳 Docker support with Alpine Linux
- 📊 Comprehensive logging
- 🏥 Health check endpoint

## Requirements

- **Docker** (recommended) - for containerized deployment
- **Python 3.11+** - for local development
- **uv** - Python package manager (for development)

## Quick Start

### Using Docker (Recommended)

1. **Pull the image**:
```bash
docker pull ghcr.io/leconio/http_smtp_bridge:latest
```

2. **Run with Docker Compose** (easiest):
```bash
# Copy and edit .env file
cp .env.example .env
nano .env

# Start the service
docker-compose up -d
```

3. **Or run with docker command**:
```bash
docker run -d \
  --name smtp_bridge \
  --network host \
  -e SMTP_HOST=localhost \
  -e SMTP_PORT=25 \
  -e SMTP_USE_TLS=false \
  -e API_KEY=your_secret_key \
  -e LOG_FILE= \
  --restart unless-stopped \
  ghcr.io/leconio/http_smtp_bridge:latest
```

## Docker Deployment Options

### Option 1: Host Network Mode (Recommended for Local SMTP)

Use this when your SMTP server is running on the host machine (localhost):

```bash
docker run -d \
  --name smtp_bridge \
  --network host \
  -e SMTP_HOST=localhost \
  -e SMTP_PORT=25 \
  -e SMTP_USE_TLS=false \
  -e API_KEY=your_api_key \
  -e LOG_FILE= \
  --restart unless-stopped \
  ghcr.io/leconio/http_smtp_bridge:latest
```

**Note**: With `--network host`, the container uses the host's network. No need to map ports.

### Option 2: Bridge Network with host.docker.internal

Use this for external SMTP servers or when you need port isolation:

```bash
docker run -d \
  --name smtp_bridge \
  -p 8000:8000 \
  --add-host=host.docker.internal:host-gateway \
  -e SMTP_HOST=host.docker.internal \
  -e SMTP_PORT=25 \
  -e SMTP_USE_TLS=false \
  -e API_KEY=your_api_key \
  -e LOG_FILE= \
  --restart unless-stopped \
  ghcr.io/leconio/http_smtp_bridge:latest
```

### Option 3: External SMTP Server

For Gmail, Outlook, or other external SMTP services:

```bash
docker run -d \
  --name smtp_bridge \
  -p 8000:8000 \
  -e SMTP_HOST=smtp.gmail.com \
  -e SMTP_PORT=587 \
  -e SMTP_USERNAME=your_email@gmail.com \
  -e SMTP_PASSWORD=your_app_password \
  -e SMTP_USE_TLS=true \
  -e API_KEY=your_api_key \
  --restart unless-stopped \
  ghcr.io/leconio/http_smtp_bridge:latest
```

## Local Development

1. **Install dependencies**:
```bash
uv sync
```

2. **Configure environment**:
```bash
cp .env.example .env
# Edit .env with your SMTP settings
nano .env
```

3. **Run development server**:
```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Building from Source

```bash
# Build the Docker image
docker build -t smtp_bridge .

# Run it
docker run -d \
  --name smtp_bridge \
  --network host \
  --env-file .env \
  smtp_bridge
```

## API Documentation

### Interactive Documentation

- **Swagger UI**: http://localhost:8000/docs (interactive testing)
- **ReDoc**: http://localhost:8000/redoc (readable documentation)
- **OpenAPI JSON**: http://localhost:8000/openapi.json

### API Endpoints

#### 1. Root Endpoint

**GET** `/`

Returns basic service information.

```bash
curl http://localhost:8000/
```

**Response**:
```json
{
  "service": "SMTP Bridge",
  "version": "1.0.0",
  "status": "running"
}
```

#### 2. Health Check

**GET** `/api/v1/health`

Check if the service is healthy. No authentication required.

```bash
curl http://localhost:8000/api/v1/health
```

**Response**:
```json
{
  "status": "healthy",
  "service": "smtp-bridge"
}
```

#### 3. Send Email

**POST** `/api/v1/send`

Send an email via SMTP. Requires API key authentication.

**Headers**:
- `Content-Type: application/json`
- `X-API-Key: your_api_key` (if API_KEY is configured)

**Request Body**:
```json
{
  "from": "sender@example.com",
  "from_name": "Sender Name (optional)",
  "to": ["recipient1@example.com", "recipient2@example.com"],
  "cc": ["cc@example.com"],  // optional
  "bcc": ["bcc@example.com"],  // optional
  "subject": "Email Subject",
  "text": "Plain text content",  // at least one of text or html required
  "html": "<p>HTML content</p>",  // at least one of text or html required
  "reply_to": "reply@example.com",  // optional
  "headers": {  // optional custom headers
    "X-Custom-Header": "value"
  },
  "attachments": [  // optional
    {
      "filename": "document.pdf",
      "content": "base64_encoded_content",
      "content_type": "application/pdf"
    }
  ]
}
```

**Response (Success)**:
```json
{
  "success": true,
  "message": "Email sent successfully",
  "message_id": "<unique-message-id@hostname>"
}
```

**Response (Error)**:
```json
{
  "detail": "Error message describing what went wrong"
}
```

## Testing with curl

### Basic Test Examples

#### 1. Simple Text Email

```bash
curl -X POST http://localhost:8000/api/v1/send \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your_api_key" \
  -d '{
    "from": "sender@example.com",
    "to": ["recipient@example.com"],
    "subject": "Simple Test",
    "text": "This is a plain text email."
  }'
```

#### 2. HTML Email

```bash
curl -X POST http://localhost:8000/api/v1/send \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your_api_key" \
  -d '{
    "from": "sender@example.com",
    "from_name": "John Doe",
    "to": ["recipient@example.com"],
    "subject": "HTML Email Test",
    "html": "<html><body><h1>Hello!</h1><p>This is an <strong>HTML</strong> email.</p></body></html>"
  }'
```

#### 3. Email with Text and HTML (Multipart)

```bash
curl -X POST http://localhost:8000/api/v1/send \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your_api_key" \
  -d '{
    "from": "sender@example.com",
    "to": ["recipient@example.com"],
    "subject": "Multipart Email",
    "text": "This is the plain text version.",
    "html": "<p>This is the <strong>HTML</strong> version.</p>"
  }'
```

#### 4. Email with CC and BCC

```bash
curl -X POST http://localhost:8000/api/v1/send \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your_api_key" \
  -d '{
    "from": "sender@example.com",
    "to": ["primary@example.com"],
    "cc": ["cc1@example.com", "cc2@example.com"],
    "bcc": ["bcc@example.com"],
    "subject": "Email with CC and BCC",
    "text": "This email has CC and BCC recipients."
  }'
```

#### 5. Email with Reply-To

```bash
curl -X POST http://localhost:8000/api/v1/send \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your_api_key" \
  -d '{
    "from": "noreply@example.com",
    "reply_to": "support@example.com",
    "to": ["customer@example.com"],
    "subject": "Support Response",
    "text": "Please reply to support@example.com for assistance."
  }'
```

#### 6. Email with Base64 Attachment

```bash
# First, encode a file to base64
BASE64_CONTENT=$(base64 -w 0 document.pdf)

curl -X POST http://localhost:8000/api/v1/send \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your_api_key" \
  -d '{
    "from": "sender@example.com",
    "to": ["recipient@example.com"],
    "subject": "Email with Attachment",
    "text": "Please find the attached document.",
    "attachments": [
      {
        "filename": "document.pdf",
        "content": "'"$BASE64_CONTENT"'",
        "content_type": "application/pdf"
      }
    ]
  }'
```

### Complete Test Script

Save this as `test_smtp_bridge.sh`:

```bash
#!/bin/bash

# Configuration
API_KEY="your_api_key"
BASE_URL="http://localhost:8000"
FROM_EMAIL="sender@example.com"
TO_EMAIL="recipient@example.com"

echo "=========================================="
echo "SMTP Bridge API Test Suite"
echo "=========================================="

# Test 1: Health Check
echo -e "\n[1/5] Testing Health Check..."
RESPONSE=$(curl -s "$BASE_URL/api/v1/health")
echo "Response: $RESPONSE"
if echo "$RESPONSE" | grep -q "healthy"; then
    echo "✅ Health check passed"
else
    echo "❌ Health check failed"
fi

# Test 2: Root Endpoint
echo -e "\n[2/5] Testing Root Endpoint..."
RESPONSE=$(curl -s "$BASE_URL/")
echo "Response: $RESPONSE"
if echo "$RESPONSE" | grep -q "SMTP Bridge"; then
    echo "✅ Root endpoint passed"
else
    echo "❌ Root endpoint failed"
fi

# Test 3: Send Plain Text Email
echo -e "\n[3/5] Testing Plain Text Email..."
RESPONSE=$(curl -s -X POST "$BASE_URL/api/v1/send" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{
    "from": "'"$FROM_EMAIL"'",
    "to": ["'"$TO_EMAIL"'"],
    "subject": "Plain Text Test",
    "text": "This is a plain text test email."
  }')
echo "Response: $RESPONSE"
if echo "$RESPONSE" | grep -q "success"; then
    echo "✅ Plain text email sent"
else
    echo "❌ Plain text email failed"
fi

# Test 4: Send HTML Email
echo -e "\n[4/5] Testing HTML Email..."
RESPONSE=$(curl -s -X POST "$BASE_URL/api/v1/send" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{
    "from": "'"$FROM_EMAIL"'",
    "from_name": "Test Sender",
    "to": ["'"$TO_EMAIL"'"],
    "subject": "HTML Test Email",
    "html": "<h1>Test</h1><p>This is an <strong>HTML</strong> email.</p>"
  }')
echo "Response: $RESPONSE"
if echo "$RESPONSE" | grep -q "success"; then
    echo "✅ HTML email sent"
else
    echo "❌ HTML email failed"
fi

# Test 5: Test Without API Key (should fail)
echo -e "\n[5/5] Testing Authentication (no API key)..."
RESPONSE=$(curl -s -X POST "$BASE_URL/api/v1/send" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "'"$FROM_EMAIL"'",
    "to": ["'"$TO_EMAIL"'"],
    "subject": "Test",
    "text": "This should fail."
  }')
echo "Response: $RESPONSE"
if echo "$RESPONSE" | grep -q "detail"; then
    echo "✅ Authentication check passed (correctly rejected)"
else
    echo "⚠️  Authentication check unexpected result"
fi

echo -e "\n=========================================="
echo "Test Suite Complete"
echo "=========================================="
```

**Usage**:
```bash
# Make it executable
chmod +x test_smtp_bridge.sh

# Edit the configuration
nano test_smtp_bridge.sh

# Run the tests
./test_smtp_bridge.sh
```

### Python Test Script

Save this as `test_smtp_bridge.py`:

```python
#!/usr/bin/env python3
"""
Test script for SMTP Bridge API
"""
import requests
import sys

BASE_URL = "http://localhost:8000"
API_KEY = "your_api_key"

def test_health():
    """Test health check endpoint"""
    print("\n[1/3] Testing health check...")
    response = requests.get(f"{BASE_URL}/api/v1/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    print("✅ Health check passed")

def test_send_email():
    """Test send email endpoint"""
    print("\n[2/3] Testing send email...")

    data = {
        "from": "test@example.com",
        "from_name": "Test User",
        "to": ["recipient@example.com"],
        "subject": "Test Email from Python",
        "text": "This is a test email sent via Python script.",
        "html": "<p>This is a <strong>test email</strong> sent via Python script.</p>"
    }

    headers = {
        "Content-Type": "application/json",
        "X-API-Key": API_KEY
    }

    response = requests.post(f"{BASE_URL}/api/v1/send", json=data, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

    if response.status_code == 200:
        print("✅ Email sent successfully")
    else:
        print("❌ Email sending failed")

def test_no_auth():
    """Test authentication requirement"""
    print("\n[3/3] Testing authentication...")

    data = {
        "from": "test@example.com",
        "to": ["recipient@example.com"],
        "subject": "Test",
        "text": "Test"
    }

    response = requests.post(f"{BASE_URL}/api/v1/send", json=data)
    print(f"Status: {response.status_code}")

    if response.status_code == 403 or response.status_code == 401:
        print("✅ Authentication check passed")
    else:
        print(f"⚠️  Unexpected status: {response.status_code}")

if __name__ == "__main__":
    print("=" * 50)
    print("SMTP Bridge API Test Suite (Python)")
    print("=" * 50)

    try:
        test_health()
        test_send_email()
        test_no_auth()

        print("\n" + "=" * 50)
        print("All tests completed")
        print("=" * 50)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
```

**Usage**:
```bash
# Install requests if needed
pip install requests

# Edit configuration
nano test_smtp_bridge.py

# Run tests
python3 test_smtp_bridge.py
```

## Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `SMTP_HOST` | SMTP server hostname | `localhost` | Yes |
| `SMTP_PORT` | SMTP server port | `25` | Yes |
| `SMTP_USERNAME` | SMTP username | - | No |
| `SMTP_PASSWORD` | SMTP password | - | No |
| `SMTP_USE_TLS` | Enable TLS/STARTTLS | `false` | No |
| `SMTP_TIMEOUT` | Connection timeout (seconds) | `30` | No |
| `API_KEY` | API authentication key | - | No |
| `ALLOWED_ORIGINS` | CORS allowed origins | `["*"]` | No |
| `RATE_LIMIT_ENABLED` | Enable rate limiting | `true` | No |
| `RATE_LIMIT_REQUESTS` | Max requests per period | `100` | No |
| `RATE_LIMIT_PERIOD` | Rate limit period (seconds) | `60` | No |
| `LOG_LEVEL` | Logging level (INFO/DEBUG/WARNING) | `INFO` | No |
| `LOG_FILE` | Log file path (empty for stdout) | - | No |

### Common SMTP Configurations

#### Gmail
```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USE_TLS=true
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
```

#### Outlook/Office 365
```env
SMTP_HOST=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_USE_TLS=true
```

#### Local Postfix/Sendmail
```env
SMTP_HOST=localhost
SMTP_PORT=25
SMTP_USE_TLS=false
```

## Troubleshooting

### SSL/TLS Errors

**Error**: `[SSL: WRONG_VERSION_NUMBER] wrong version number`

**Solution**: Your SMTP server doesn't support TLS on this port. Set `SMTP_USE_TLS=false`:
```bash
-e SMTP_USE_TLS=false
```

### Connection Refused

**Error**: `Connection refused to 127.0.0.1:25`

**Solutions**:
1. Use `--network host` mode
2. Check if SMTP server is running: `telnet localhost 25`
3. Use correct SMTP port (25, 587, or 465)

### Permission Denied

**Error**: `Permission denied to /var/log/smtp_bridge/app.log`

**Solution**: Set `LOG_FILE` to empty for Docker:
```bash
-e LOG_FILE=
```

## CI/CD

This project uses GitHub Actions for automated builds:

- **Trigger**: Push tags matching `v*` (e.g., v1.0.7)
- **Registry**: GitHub Container Registry (ghcr.io)
- **Architecture**: linux/amd64 only
- **Image Tags**:
  - `v1.0.7` - Specific version
  - `v1.0` - Minor version
  - `v1` - Major version
  - `latest` - Latest release

## License

MIT

## Links

- **Repository**: https://github.com/leconio/http_smtp_bridge
- **Container Registry**: https://github.com/leconio/http_smtp_bridge/pkgs/container/http_smtp_bridge
- **Issues**: https://github.com/leconio/http_smtp_bridge/issues
