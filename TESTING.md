# 🧪 MenuMate Testing Guide

## ✅ Step 1: Verify API Connections

Already done! Your APIs are working:
```bash
source venv/bin/activate
python test_api.py
```

## 🚀 Step 2: Start the Server

In your terminal, run:
```bash
source venv/bin/activate
uvicorn main:app --reload --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

## 🧪 Step 3: Test Basic Endpoints

### Test Health Check
```bash
curl http://localhost:8000/health
```
Expected: `{"status":"ok"}`

### Test Root Endpoint
```bash
curl http://localhost:8000/
```
Expected: JSON with service information

## 📱 Step 4: Test Webhook Endpoint

### Option A: Manual Test (without image)
```bash
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "From=whatsapp:+1234567890" \
  -d "Body=What should I order?" \
  -d "NumMedia=0"
```

This will return an error message asking for an image (which is expected).

### Option B: Test with Sample Image URL
You need a publicly accessible image URL. Here's an example:

```bash
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "From=whatsapp:+1234567890" \
  -d "Body=What should I order?" \
  -d "NumMedia=1" \
  -d "MediaUrl0=https://example.com/menu.jpg"
```

## 🔗 Step 5: Test with WhatsApp (Local)

### Using ngrok

1. **Install ngrok** (if not already):
   ```bash
   # macOS
   brew install ngrok
   ```

2. **Start your server** (in one terminal):
   ```bash
   source venv/bin/activate
   uvicorn main:app --reload
   ```

3. **Start ngrok** (in another terminal):
   ```bash
   ngrok http 8000
   ```

4. **Copy the HTTPS URL** (e.g., `https://abc123.ngrok.io`)

5. **Configure Twilio Webhook**:
   - Go to [Twilio Console](https://console.twilio.com/)
   - Navigate to: **Messaging** → **Settings** → **WhatsApp Sandbox Settings**
   - Set **When a message comes in**: `https://your-ngrok-url.ngrok.io/webhook`
   - Method: `POST`
   - Save!

6. **Join WhatsApp Sandbox** (if not already):
   - Send the join code word to `+1 415 523 8886` (or your sandbox number)
   - Code word is shown in Twilio Console

7. **Test via WhatsApp**:
   - Send a photo of a menu to the sandbox number
   - Add text: "What should I order?"
   - Wait for the AI response!

## 🚢 Step 6: Test in Production (Render)

1. **Deploy to Render** (see README.md)
2. **Update Twilio webhook** to point to your Render URL
3. **Test via WhatsApp** as above

## 🐛 Troubleshooting

### Port 8000 already in use
```bash
# Find what's using port 8000
lsof -ti:8000

# Kill it
kill -9 $(lsof -ti:8000)

# Or use a different port
uvicorn main:app --reload --port 8001
```

### OpenAI API errors
- Check your API key in `.env`
- Verify you have credits/quota
- Check API status: https://status.openai.com/

### Serper.dev errors
- Verify API key is correct
- Check quota: https://serper.dev/dashboard

### Twilio errors
- Verify Account SID and Auth Token
- Check WhatsApp sandbox is activated
- Ensure webhook URL is publicly accessible (HTTPS)

### Image analysis fails
- Ensure image URL is publicly accessible
- Image must be in supported format (JPG, PNG, etc.)
- Check image size isn't too large

## 📝 Test Checklist

- [ ] API connections verified (`python test_api.py`)
- [ ] Server starts without errors
- [ ] Health endpoint returns `{"status":"ok"}`
- [ ] Webhook endpoint accepts POST requests
- [ ] ngrok tunnel established (for local testing)
- [ ] Twilio webhook configured
- [ ] WhatsApp sandbox joined
- [ ] Test message with menu image sent
- [ ] AI response received

## 🎉 Success!

If you receive an AI-generated recommendation via WhatsApp, everything is working! 🎊

