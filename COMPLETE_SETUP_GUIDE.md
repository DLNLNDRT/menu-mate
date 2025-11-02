# 🚀 Complete Setup Guide: MenuMate

Follow these steps **in order** to get your MenuMate project running from scratch.

---

## 📋 Pre-Flight Checklist

Before starting, make sure you have:
- ✅ Python 3.9+ installed
- ✅ Terminal/Command line access
- ✅ Accounts for: OpenAI, Serper.dev, Twilio
- ✅ WhatsApp on your phone (for testing)

---

## STEP 1: Verify Project Files ✅

Your project should already have these files. Let's verify:

```bash
cd /Users/dylanlindert/Desktop/Tutai/Assignment5
ls -la
```

You should see:
- `main.py` - FastAPI application
- `requirements.txt` - Python dependencies
- `utils/` - Helper modules
- `.env_template` - Template for environment variables
- `.env` - Your actual API keys (should already exist)

**✅ If all files are present, continue to Step 2**

---

## STEP 2: Verify Environment Variables 🔑

Check that your `.env` file has all API keys:

```bash
source venv/bin/activate
python test_api.py
```

**Expected output:** All 5 APIs should show ✅ PASS

**If any fail:**
1. Open `.env` file
2. Add missing API keys (see Step 2B below for where to get them)

### STEP 2B: Getting API Keys (if needed)

#### A. OpenAI API Key
1. Go to: https://platform.openai.com/api-keys
2. Click **"Create new secret key"**
3. Copy the key (starts with `sk-`)
4. Add to `.env`: `OPENAI_API_KEY=sk-your-key-here`

#### B. Serper.dev API Key
1. Go to: https://serper.dev
2. Sign up (free tier: 2,500 searches/month)
3. Copy API key from dashboard
4. Add to `.env`: `SERPER_API_KEY=your-key-here`

#### C. Twilio Credentials
1. Go to: https://console.twilio.com
2. Find **Account SID** (starts with `AC...`)
3. Find **Auth Token** (click "Show" to reveal)
4. Add to `.env`:
   ```
   TWILIO_ACCOUNT_SID=ACyour-sid-here
   TWILIO_AUTH_TOKEN=your-token-here
   TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
   ```

---

## STEP 3: Start the Server 🖥️

**In your terminal:**

```bash
cd /Users/dylanlindert/Desktop/Tutai/Assignment5
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**You should see:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Application startup complete.
```

**✅ Server is running!** (Keep this terminal open)

---

## STEP 4: Test the Server 🧪

**Open a NEW terminal window** (keep server running):

```bash
# Test health endpoint
curl http://localhost:8000/health

# Should return: {"status":"ok"}

# Test root endpoint
curl http://localhost:8000/

# Should return JSON with service info
```

**✅ If both work, continue to Step 5**

---

## STEP 5: Set Up WhatsApp Integration 📱

### 5A. Install ngrok

```bash
brew install ngrok
```

**If brew fails:** Download from https://ngrok.com/download

Verify installation:
```bash
ngrok version
```

### 5B. Start ngrok Tunnel

**In a NEW terminal window** (keep server running):

```bash
cd /Users/dylanlindert/Desktop/Tutai/Assignment5
ngrok http 8000
```

**You'll see:**
```
Forwarding    https://abc123xyz.ngrok.io -> http://localhost:8000
```

**📋 COPY THE HTTPS URL** (the one starting with `https://`)

**⚠️ Keep this terminal open!** ngrok must stay running.

### 5C. Configure Twilio Webhook

1. **Go to Twilio Console:**
   - Visit: https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn
   - Or: Messaging → Settings → WhatsApp Sandbox Settings

2. **Find Sandbox Configuration section**

3. **Set webhook:**
   - **When a message comes in**: Paste your ngrok URL + `/webhook`
     - Example: `https://abc123xyz.ngrok.io/webhook`
   - **HTTP Method**: `POST`
   - Click **Save**

4. **Note your sandbox info:**
   - Sandbox number: Usually `+1 415 523 8886`
   - Join code word: Shown on the same page (e.g., `join example-code`)

### 5D. Join WhatsApp Sandbox

1. **Open WhatsApp** on your phone
2. **Send a message** to the sandbox number (from Step 5C)
3. **Send the join code word** (from Step 5C)
   - Example: `join example-code`
4. **Wait for confirmation:** "You're all set! You've joined the sandbox."

**✅ You're now connected to the sandbox!**

---

## STEP 6: Test It! 🎉

1. **Find a menu photo** (or take one with your phone)
2. **Open WhatsApp**
3. **Send to sandbox number:**
   - Attach the menu photo
   - Add text: "What should I order?"
4. **Wait for response!** 

You should receive:
- 🍽 Restaurant name
- ✅ Best dish recommendation
- 💬 Reasoning
- ⭐ Review highlights
- 📸 Optional: Generated dish image

---

## 🎯 Quick Command Reference

```bash
# Terminal 1: Start server
cd /Users/dylanlindert/Desktop/Tutai/Assignment5
source venv/bin/activate
uvicorn main:app --reload

# Terminal 2: Start ngrok
cd /Users/dylanlindert/Desktop/Tutai/Assignment5
ngrok http 8000

# Terminal 3: Test endpoints
curl http://localhost:8000/health
curl http://localhost:8000/
```

---

## 🐛 Troubleshooting

### Server won't start
```bash
# Check if port 8000 is in use
lsof -ti:8000

# Kill process if needed
lsof -ti:8000 | xargs kill -9

# Try different port
uvicorn main:app --reload --port 8001
```

### API connection errors
```bash
# Test all APIs
python test_api.py

# Check .env file has all keys
cat .env
```

### ngrok not found
```bash
# Install via brew
brew install ngrok

# Or download manually
# https://ngrok.com/download
```

### Webhook not receiving messages
- ✅ Verify ngrok is running (keep terminal open)
- ✅ Check webhook URL in Twilio matches ngrok URL exactly
- ✅ Ensure you joined sandbox successfully
- ✅ Check server logs for incoming requests
- ✅ Verify server is running on port 8000

### Image analysis fails
- Use a clear, well-lit menu photo
- Ensure image is publicly accessible (Twilio provides this)
- Check OpenAI API has credits/quota
- See server logs for specific error

---

## ✅ Success Checklist

- [ ] All environment variables set and verified (`python test_api.py`)
- [ ] Server running without errors
- [ ] Health endpoint returns `{"status":"ok"}`
- [ ] ngrok tunnel active and URL copied
- [ ] Twilio webhook configured with ngrok URL
- [ ] Joined WhatsApp sandbox successfully
- [ ] Sent test menu photo via WhatsApp
- [ ] Received AI recommendation response

---

## 🚀 Next Steps (After Testing)

1. **Deploy to Render:**
   - Push code to GitHub
   - Connect to Render
   - Add environment variables
   - Update Twilio webhook to Render URL

2. **Production Setup:**
   - Request production WhatsApp number from Twilio
   - Set up custom domain (optional)
   - Monitor usage and costs

---

## 📚 Additional Resources

- `QUICK_START_WHATSAPP.md` - Quick WhatsApp reference
- `WHATSAPP_SETUP.md` - Detailed WhatsApp setup
- `TESTING.md` - Comprehensive testing guide
- `README.md` - Full project documentation

---

**Need help?** Check the server terminal logs for detailed error messages!

