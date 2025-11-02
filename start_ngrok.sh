#!/bin/bash
# Quick script to start ngrok for WhatsApp testing

echo "🔗 Starting ngrok tunnel on port 8000..."
echo ""
echo "⚠️  Keep this terminal open while testing!"
echo "📋 Copy the HTTPS URL shown below"
echo ""

# Check if ngrok is installed
if ! command -v ngrok &> /dev/null; then
    echo "❌ ngrok is not installed!"
    echo ""
    echo "Install it with:"
    echo "  brew install ngrok"
    echo ""
    echo "Or download from: https://ngrok.com/download"
    exit 1
fi

# Start ngrok
ngrok http 8000

