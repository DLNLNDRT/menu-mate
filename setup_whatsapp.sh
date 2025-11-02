#!/bin/bash
# WhatsApp Integration Setup Helper

echo "╔══════════════════════════════════════════════════════════╗"
echo "║      📱 MenuMate WhatsApp Integration Setup            ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Step 1: Check if ngrok is installed
echo "Step 1: Checking ngrok installation..."
if command -v ngrok &> /dev/null; then
    echo "✅ ngrok is installed: $(ngrok version | head -1)"
else
    echo "❌ ngrok is not installed"
    echo ""
    echo "Installing ngrok..."
    if command -v brew &> /dev/null; then
        brew install ngrok
    else
        echo "⚠️  Homebrew not found. Please install ngrok manually:"
        echo "   https://ngrok.com/download"
        exit 1
    fi
fi

echo ""
echo "Step 2: Checking if server is running..."
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ Server is running on port 8000"
else
    echo "❌ Server is not running!"
    echo "   Start it with: uvicorn main:app --reload"
    exit 1
fi

echo ""
echo "Step 3: Starting ngrok tunnel..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "⚠️  IMPORTANT: Keep this terminal open!"
echo "📋 Copy the HTTPS URL that appears below"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Start ngrok
ngrok http 8000

