#!/usr/bin/env python3
"""
Debug script to test webhook endpoint and see what errors occur.
"""
import requests
import sys

def test_webhook():
    """Test the webhook endpoint with sample data."""
    url = "http://localhost:8000/webhook"
    
    # Test 1: Without image (should return 200 with message)
    print("Test 1: Webhook without image...")
    try:
        response = requests.post(
            url,
            data={
                "From": "whatsapp:+1234567890",
                "Body": "What should I order?",
                "NumMedia": "0"
            },
            timeout=30
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:200]}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "-" * 60 + "\n")
    
    # Test 2: With image URL (will try to process)
    print("Test 2: Webhook with image URL...")
    try:
        response = requests.post(
            url,
            data={
                "From": "whatsapp:+1234567890",
                "Body": "What should I order?",
                "NumMedia": "1",
                "MediaUrl0": "https://example.com/menu.jpg"  # This will fail but shows the error
            },
            timeout=30
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:500]}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("Webhook Debug Test")
    print("=" * 60)
    print("\nMake sure server is running: uvicorn main:app --reload\n")
    test_webhook()

