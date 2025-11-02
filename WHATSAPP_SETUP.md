# 📱 WhatsApp Integration Setup Guide

## Prerequisites
- ✅ Server is running on port 8000
- ✅ Twilio account with WhatsApp access
- ✅ All API keys configured in `.env`

## Step-by-Step Setup

### Step 1: Install ngrok

**macOS:**
```bash
brew install ngrok
```

**Or download from:** https://ngrok.com/download

**Verify installation:**
```bash
ngrok --version
```

### Step 2: Start ngrok Tunnel

In a **new terminal window** (keep your server running in the first one):

```bash
ngrok http 8000
```

You'll see output like:
```
Session Status                online
Forwarding                    https://abc123.ngrok.io -> http://localhost:8000
```

**Copy the HTTPS URL** (the one starting with `https://`)

### Step 3: Configure Twilio Webhook

1. **Go to Twilio Console:**
   - Visit: https://console.twilio.com/
   - Navigate to: **Messaging** → **Settings** → **WhatsApp Sandbox Settings**

2. **Set Webhook URL:**
   - **When a message comes in**: `https://your-ngrok-url.ngrok.io/webhook`
   - Replace `your-ngrok-url` with the HTTPS URL from ngrok
   - **HTTP Method**: `POST`
   - Click **Save**

3. **Note your Sandbox Number:**
   - You'll see something like: `+1 415 523 8886`
   - Note the **join code word** shown on this page

### Step 4: Join WhatsApp Sandbox

1. **Open WhatsApp** on your phone
2. **Send a message** to the sandbox number (e.g., `+1 415 523 8886`)
3. **Send the join code word** (shown in Twilio Console)
   - For example: `join example-code`

You should receive a confirmation message from Twilio.

### Step 5: Test Your Integration

1. **Send a test message:**
   - Send a **photo of a restaurant menu** to the sandbox number
   - Include text like: "What should I order?"
   - Or: "Recommend me something from this menu"

2. **Watch your server logs:**
   - You should see POST requests coming to `/webhook`
   - Check for any errors in the terminal

3. **Receive AI response:**
   - You should get a WhatsApp message with:
     - Restaurant name
     - Best dish recommendation
     - Reasoning
     - Review highlights
     - Optional: Generated dish image

## Troubleshooting

### ngrok Connection Issues
- Make sure ngrok is pointing to port 8000
- Verify your server is still running
- Check ngrok status in their dashboard

### Webhook Not Receiving Messages
- Verify webhook URL in Twilio matches ngrok URL exactly
- Make sure you're using HTTPS (not HTTP)
- Check that you joined the sandbox successfully
- Verify server logs for incoming requests

### Server Errors
- Check `.env` file has all API keys
- Verify OpenAI, Serper.dev, and Twilio APIs are working
- Check server logs for error messages
- Test API connections: `python test_api.py`

### Image Not Processing
- Ensure image URL is publicly accessible
- Check image format (JPG, PNG supported)
- Verify OpenAI API has credits/quota

## Testing Without WhatsApp (Alternative)

You can test the webhook directly with curl:

```bash
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "From=whatsapp:+1234567890" \
  -d "Body=What should I order?" \
  -d "NumMedia=1" \
  -d "MediaUrl0=https://example.com/menu.jpg"
```

## Next Steps After Testing

Once everything works locally:

1. **Deploy to Render** (see README.md)
2. **Update Twilio webhook** to point to your Render URL
3. **Test in production**
4. **Request production WhatsApp access** from Twilio (if needed)

---

Need help? Check the server logs for detailed error messages!

