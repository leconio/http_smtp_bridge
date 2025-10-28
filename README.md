# SMTP Bridge

HTTP to SMTP proxy service built with FastAPI and uvicorn.

## Features

- RESTful API for sending emails via SMTP
- Support for HTML and plain text emails
- File attachments support (base64 encoded)
- API key authentication
- Rate limiting
- CORS support
- Production-ready with Gunicorn + Uvicorn workers
- Systemd service configuration
- Nginx reverse proxy configuration
- Comprehensive logging

## Requirements

- Python 3.11+
- uv (Python package manager)
- Nginx (for production)
- Systemd (for service management)
- Docker (for containerized deployment)

## Installation

### Development

1. Install dependencies:
```bash
uv sync
```

2. Configure environment:
```bash
cp .env.example .env
# Edit .env with your SMTP settings
```

3. Run development server:
```bash
uv run uvicorn app.main:app --reload
```

### Docker Deployment

#### Using Pre-built Image from GitHub Container Registry

1. Pull the latest image:
```bash
docker pull ghcr.io/YOUR_USERNAME/smtp_bridge:latest
```

2. Run the container:
```bash
docker run -d \
  --name smtp_bridge \
  -p 8000:8000 \
  -e SMTP_HOST=smtp.example.com \
  -e SMTP_PORT=587 \
  -e SMTP_USERNAME=your_username \
  -e SMTP_PASSWORD=your_password \
  -e API_KEY=your_api_key \
  ghcr.io/YOUR_USERNAME/smtp_bridge:latest
```

Or use docker-compose:
```yaml
version: '3.8'
services:
  smtp_bridge:
    image: ghcr.io/YOUR_USERNAME/smtp_bridge:latest
    ports:
      - "8000:8000"
    environment:
      - SMTP_HOST=smtp.example.com
      - SMTP_PORT=587
      - SMTP_USERNAME=your_username
      - SMTP_PASSWORD=your_password
      - API_KEY=your_api_key
    restart: unless-stopped
```

#### Building Locally

1. Build the image:
```bash
docker build -t smtp_bridge .
```

2. Run the container:
```bash
docker run -d \
  --name smtp_bridge \
  -p 8000:8000 \
  --env-file .env \
  smtp_bridge
```

### Production Deployment (Systemd)

1. Run deployment script:
```bash
sudo bash deploy.sh
```

2. Configure settings:
```bash
sudo nano /opt/smtp_bridge/.env
```

3. Start service:
```bash
sudo systemctl start smtp_bridge
```

## CI/CD

This project uses GitHub Actions to automatically build and push Docker images to GitHub Container Registry (ghcr.io):

- **On push to main/master**: Builds and pushes with `latest` tag
- **On tag (v*)**: Builds and pushes with version tags
- **Multi-architecture**: Supports both amd64 and arm64

To use the automated builds:
1. Enable GitHub Actions in your repository
2. Ensure package permissions are set to allow workflows to write packages
3. Push to main branch or create a version tag

## API Documentation

Visit http://localhost:8000/docs for interactive API documentation.

## License

MIT
