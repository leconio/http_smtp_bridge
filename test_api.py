#!/usr/bin/env python3
"""
Test script for SMTP Bridge API
"""
import asyncio
import json
from typing import Optional

try:
    import httpx
except ImportError:
    print("Installing httpx...")
    import subprocess
    subprocess.check_call(["uv", "add", "httpx"])
    import httpx


async def test_smtp_bridge(
    base_url: str = "http://localhost:8081",
    api_key: Optional[str] = None
):
    """Test SMTP Bridge API endpoints"""

    headers = {}
    if api_key:
        headers["X-API-Key"] = api_key

    async with httpx.AsyncClient(timeout=30.0) as client:
        # Test 1: Health check
        print("\n" + "=" * 50)
        print("Test 1: Health Check")
        print("=" * 50)
        try:
            response = await client.get(f"{base_url}/api/v1/health")
            print(f"Status: {response.status_code}")
            print(f"Response: {response.json()}")
        except Exception as e:
            print(f"Error: {e}")

        # Test 2: Root endpoint
        print("\n" + "=" * 50)
        print("Test 2: Root Endpoint")
        print("=" * 50)
        try:
            response = await client.get(f"{base_url}/")
            print(f"Status: {response.status_code}")
            print(f"Response: {response.json()}")
        except Exception as e:
            print(f"Error: {e}")

        # Test 3: Send email (will fail without valid SMTP config)
        print("\n" + "=" * 50)
        print("Test 3: Send Email")
        print("=" * 50)
        email_data = {
            "from": "test@mail.aside0.com",
            "from_name": "Test Sender",
            "to": ["spawnlau@gmail.com", "leconio@outlook.com"],
            "subject": "Test Email from SMTP Bridge",
            "text": "This is a test email sent via SMTP Bridge",
            "html": "<p>This is a <strong>test email</strong> sent via SMTP Bridge</p>"
        }
        try:
            response = await client.post(
                f"{base_url}/api/v1/send",
                json=email_data,
                headers=headers
            )
            print(f"Status: {response.status_code}")
            print(f"Response: {response.json()}")
        except Exception as e:
            print(f"Error: {e}")

        # Test 4: API Documentation
        print("\n" + "=" * 50)
        print("Test 4: API Documentation")
        print("=" * 50)
        print(f"OpenAPI docs: {base_url}/docs")
        print(f"ReDoc: {base_url}/redoc")


if __name__ == "__main__":
    import sys

    # Parse command line arguments
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8081"
    api_key = sys.argv[2] if len(sys.argv) > 2 else None

    print(f"\nTesting SMTP Bridge at: {base_url}")
    if api_key:
        print(f"Using API Key: {api_key[:10]}...")

    asyncio.run(test_smtp_bridge(base_url, api_key))
