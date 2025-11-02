#!/bin/bash
# Test script for the webhook endpoint
# This simulates a Twilio WhatsApp webhook POST request

echo "🧪 Testing MenuMate Webhook Endpoint"
echo "=================================="
echo ""

# Make sure server is running first
echo "📡 Make sure the server is running:"
echo "   uvicorn main:app --reload"
echo ""
read -p "Press Enter when server is running..."

# Test health endpoint first
echo "1️⃣ Testing health endpoint..."
curl -s http://localhost:8000/health | python3 -m json.tool
echo ""
echo ""

# Test root endpoint
echo "2️⃣ Testing root endpoint..."
curl -s http://localhost:8000/ | python3 -m json.tool
echo ""
echo ""

# Test webhook with sample data (simulating Twilio)
echo "3️⃣ Testing webhook endpoint with sample data..."
echo "   (This simulates a WhatsApp message with an image)"
echo ""

# Note: For full testing, you need an actual image URL that's publicly accessible
# Twilio provides MediaUrl0 in the webhook payload
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "From=whatsapp:+1234567890" \
  -d "Body=What should I order?" \
  -d "NumMedia=1" \
  -d "MediaUrl0=https://example.com/menu.jpg"

echo ""
echo ""
echo "⚠️  Note: Full testing requires:"
echo "   1. A publicly accessible image URL"
echo "   2. Or use ngrok to expose localhost"
echo "   3. Configure Twilio webhook to point to your server"

