#!/usr/bin/env python3
"""Simple webhook test to see if it responds quickly"""
import requests
import time

url = "http://localhost:8000/webhook"

print("Testing webhook response time...")
print("-" * 60)

start = time.time()

try:
    response = requests.post(
        url,
        data={
            "From": "whatsapp:+1234567890",
            "Body": "Test message",
            "NumMedia": "0"
        },
        timeout=10
    )
    
    elapsed = time.time() - start
    
    print(f"✅ Status Code: {response.status_code}")
    print(f"✅ Response Time: {elapsed:.2f} seconds")
    print(f"✅ Response Body: {response.text[:100]}")
    
    if elapsed > 5:
        print(f"\n⚠️  WARNING: Response took {elapsed:.2f}s (should be < 1s)")
    else:
        print(f"\n✅ SUCCESS: Response is fast enough for Twilio!")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

