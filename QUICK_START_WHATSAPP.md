# 🚀 Quick Start: WhatsApp Integration

## ✅ Current Status
- Server running on port 8000
- All API keys configured
- Webhook endpoint ready at `/webhook`

## 📋 Setup Steps (5 minutes)

### 1. Install ngrok (if not already installed)

```bash
brew install ngrok
```

**OR** download from: https://ngrok.com/download

---

### 2. Start ngrok Tunnel

**In a NEW terminal window** (keep server running):

```bash
cd /Users/dylanlindert/Desktop/Tutai/Assignment5
./setup_whatsapp.sh
```

**OR manually:**
```bash
ngrok http 8000
```

You'll see:
```
Forwarding    https://abc123xyz.ngrok.io -> http://localhost:8000
```

**📋 COPY THE HTTPS URL** (e.g., `https://abc123xyz.ngrok.io`)

---

### 3. Configure Twilio Webhook

1. **Open:** https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn
2. **Or navigate:** Messaging → Settings → WhatsApp Sandbox Settings

3. **Set webhook:**
   - **When a message comes in**: `https://YOUR-NGROK-URL.ngrok.io/webhook`
     - Replace `YOUR-NGROK-URL` with your actual ngrok URL
   - **HTTP Method**: `POST`
   - Click **Save**

4. **Note your sandbox info:**
   - Sandbox number: `+1 415 523 8886` (or shown in console)
   - Join code word: (shown on the same page)

---

### 4. Join WhatsApp Sandbox

1. **Open WhatsApp** on your phone
2. **Send a message** to the sandbox number
3. **Send the join code word** (e.g., `join example-code`)
4. You'll receive: "You're all set! You've joined the sandbox."

---

### 5. Test It!

1. **Send a menu photo** to the sandbox number via WhatsApp
2. **Add text**: "What should I order?"
3. **Wait for AI response!** 🎉

---

## 🎯 Quick Commands Reference

```bash
# Start server
source venv/bin/activate
uvicorn main:app --reload

# Start ngrok (in another terminal)
ngrok http 8000

# Test webhook locally
curl -X POST http://localhost:8000/webhook \
  -d "From=whatsapp:+1234567890" \
  -d "Body=test" \
  -d "NumMedia=0"
```

---

## 🐛 Troubleshooting

**ngrok not found:**
```bash
brew install ngrok
```

**Port 8000 in use:**
```bash
lsof -ti:8000 | xargs kill -9
```

**Webhook not receiving:**
- Check ngrok URL matches exactly in Twilio
- Verify server is running
- Check ngrok is running (keep terminal open!)
- Verify you joined sandbox successfully

**Check server logs** for errors!

---

## 📚 More Details

- Full guide: `WHATSAPP_SETUP.md`
- Testing guide: `TESTING.md`
- General docs: `README.md`

---

**Need help?** Check server terminal for error messages!

