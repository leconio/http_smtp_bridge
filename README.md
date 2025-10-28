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

## API Usage

### Health Check

```bash
curl http://localhost:8000/api/v1/health
```

### Send Email

```bash
curl -X POST http://localhost:8000/api/v1/send \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your_api_key" \
  -d '{
    "from": "sender@example.com",
    "from_name": "Sender Name",
    "to": ["recipient@example.com"],
    "subject": "Test Email",
    "text": "Plain text content",
    "html": "<p>HTML content</p>"
  }'
```

### API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

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
