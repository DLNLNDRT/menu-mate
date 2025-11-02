#!/usr/bin/env python3
"""
Test script to verify API connections for MenuMate.
This will test your OpenAI, Serper.dev, and Twilio credentials.
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_env_variables():
    """Test that all required environment variables are set."""
    print("🔍 Checking environment variables...")
    required_vars = [
        "OPENAI_API_KEY",
        "SERPER_API_KEY",
        "TWILIO_ACCOUNT_SID",
        "TWILIO_AUTH_TOKEN",
        "TWILIO_WHATSAPP_NUMBER"
    ]
    
    missing = []
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            missing.append(var)
            print(f"  ❌ {var}: Not set")
        else:
            # Show first few characters for verification
            masked = value[:10] + "..." if len(value) > 10 else value
            print(f"  ✅ {var}: {masked}")
    
    if missing:
        print(f"\n⚠️  Missing {len(missing)} environment variable(s). Please check your .env file.")
        return False
    else:
        print("\n✅ All environment variables are set!")
        return True

def test_openai():
    """Test OpenAI API connection."""
    print("\n🤖 Testing OpenAI API...")
    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Simple test call
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Say 'Hello' if you can read this."}],
            max_tokens=10
        )
        message = response.choices[0].message.content
        print(f"  ✅ OpenAI API working! Response: {message.strip()}")
        return True
    except Exception as e:
        print(f"  ❌ OpenAI API error: {str(e)}")
        return False

def test_serper():
    """Test Serper.dev API connection."""
    print("\n🔍 Testing Serper.dev API...")
    try:
        import requests
        api_key = os.getenv("SERPER_API_KEY")
        
        url = "https://google.serper.dev/search"
        headers = {
            "X-API-KEY": api_key,
            "Content-Type": "application/json"
        }
        payload = {
            "q": "best restaurant",
            "num": 1
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if "organic" in data or "answerBox" in data:
            print("  ✅ Serper.dev API working!")
            return True
        else:
            print("  ⚠️  Serper.dev API responded but no results found")
            return True  # Still counts as working
    except Exception as e:
        print(f"  ❌ Serper.dev API error: {str(e)}")
        return False

def test_twilio():
    """Test Twilio credentials (without sending a message)."""
    print("\n📱 Testing Twilio credentials...")
    try:
        from twilio.rest import Client
        
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        
        client = Client(account_sid, auth_token)
        
        # Try to fetch account info (this validates credentials)
        account = client.api.accounts(account_sid).fetch()
        print(f"  ✅ Twilio credentials valid! Account: {account.friendly_name}")
        return True
    except Exception as e:
        print(f"  ❌ Twilio API error: {str(e)}")
        return False

def main():
    print("=" * 60)
    print("🧪 MenuMate API Connection Test")
    print("=" * 60)
    
    # Test environment variables
    if not test_env_variables():
        print("\n❌ Please fix your .env file and try again.")
        sys.exit(1)
    
    # Test each API
    results = {
        "OpenAI": test_openai(),
        "Serper.dev": test_serper(),
        "Twilio": test_twilio()
    }
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    for service, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"  {service}: {status}")
    
    all_passed = all(results.values())
    if all_passed:
        print("\n🎉 All tests passed! Your API connections are working.")
        print("\n💡 Next steps:")
        print("   1. Start the server: uvicorn main:app --reload")
        print("   2. Test the webhook endpoint (see README.md)")
        print("   3. Set up WhatsApp webhook in Twilio")
    else:
        print("\n⚠️  Some tests failed. Please check your API keys and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main()

