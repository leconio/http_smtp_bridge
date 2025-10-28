#!/bin/bash
# Quick start script for development

export PATH="$HOME/.local/bin:$PATH"

# Check if .env exists
if [ ! -f .env ]; then
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo "Please edit .env with your SMTP configuration"
    exit 1
fi

# Run with uvicorn (development)
echo "Starting SMTP Bridge (Development Mode)..."
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8081
