# 🚀 Render Setup - Step by Step Guide

Follow these exact steps to get MenuMate running on Render.

---

## STEP 1: Sign Up for Render (if not done)

1. Go to: https://dashboard.render.com/
2. Click **"Get Started for Free"** or **"Sign Up"**
3. Sign up with:
   - **GitHub** (recommended - connects automatically)
   - OR Email
4. Verify your email if required

---

## STEP 2: Create New Web Service

1. In Render Dashboard, click **"New +"** button (top right)
2. Select **"Web Service"**
3. You'll see: **"Connect a repository"**
4. Click **"Connect GitHub"** (or GitLab if you prefer)

---

## STEP 3: Connect Your Repository

1. **Authorize Render** to access your GitHub (if first time)
2. **Search for**: `menu-mate`
3. **Select**: `DLNLNDRT/menu-mate`
4. Click **"Connect"**

---

## STEP 4: Configure Service

Render will auto-detect from `render.yaml`, but verify:

### Basic Settings:
- **Name**: `menu-mate` (or your choice)
- **Region**: Choose closest to you (e.g., `Oregon` for US)
- **Branch**: `main` (should be default)
- **Root Directory**: Leave blank (or `.`)

### Build & Deploy:
- **Environment**: `Python 3` (auto-detected)
- **Build Command**: `pip install -r requirements.txt` (auto-detected)
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port 10000` (auto-detected)

### Plan:
- **Free**: Free tier (good for testing)
  - Note: Free tier spins down after 15 min inactivity, but wakes up on request

---

## STEP 5: Add Environment Variables (CRITICAL!)

**This is the most important step!**

1. Scroll down to **"Environment Variables"** section
2. Click **"Add Environment Variable"** for each:

### Variable 1: OPENAI_API_KEY
- **Key**: `OPENAI_API_KEY`
- **Value**: Copy from your `.env` file (starts with `sk-`)
- Click **"Add"**

### Variable 2: SERPER_API_KEY
- **Key**: `SERPER_API_KEY`
- **Value**: Copy from your `.env` file
- Click **"Add"**

### Variable 3: TWILIO_ACCOUNT_SID
- **Key**: `TWILIO_ACCOUNT_SID`
- **Value**: Copy from your `.env` file (starts with `AC`)
- Click **"Add"**

### Variable 4: TWILIO_AUTH_TOKEN
- **Key**: `TWILIO_AUTH_TOKEN`
- **Value**: Copy from your `.env` file
- Click **"Add"**

### Variable 5: TWILIO_WHATSAPP_NUMBER
- **Key**: `TWILIO_WHATSAPP_NUMBER`
- **Value**: Copy from your `.env` file (format: `whatsapp:+14155238886`)
- Click **"Add"**

**⚠️ Important:** 
- Copy values EXACTLY from your `.env` file
- No extra spaces
- Include `whatsapp:` prefix for the phone number

---

## STEP 6: Create & Deploy

1. Scroll to bottom
2. Click **"Create Web Service"**
3. Render will start:
   - Cloning your repo
   - Installing dependencies
   - Building the service
   - Starting the server

4. **Wait 5-10 minutes** for first deployment
   - You'll see build logs
   - Status will change from "Building" → "Deploying" → "Live"

---

## STEP 7: Get Your Render URL

1. Once status shows **"Live"** (green indicator)
2. Your URL is shown at the top: `https://menu-mate.onrender.com` (or similar)
3. **Copy this URL** - you'll need it for Twilio

4. **Test it:**
   - Visit: `https://your-app.onrender.com/health`
   - Should show: `{"status":"ok"}`

---

## STEP 8: Configure Twilio Webhook

### 8A. Get Your Render Webhook URL

Your webhook URL is: `https://your-render-url.onrender.com/webhook`

Example: `https://menu-mate.onrender.com/webhook`

### 8B. Update Twilio Webhook

1. Go to: https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn
2. Scroll to **"Sandbox Configuration"** section
3. Find **"When a message comes in"** field
4. **Paste your webhook URL:**
   ```
   https://your-render-url.onrender.com/webhook
   ```
5. **HTTP Method**: Select `POST`
6. Click **"Save"**

### 8C. Verify Webhook

1. In Twilio Console, go to: **Monitor → Logs → Requests**
2. Send a test WhatsApp message
3. You should see a request to your webhook URL
4. Check status code (should be 200)

---

## STEP 9: Test End-to-End

1. **Send WhatsApp message:**
   - Open WhatsApp
   - Send to sandbox number: `+1 415 523 8886` (or your sandbox number)
   - Send a menu photo
   - Add text: "What should I order?"

2. **Check Render Logs:**
   - Render Dashboard → Your Service → **Logs**
   - You should see:
     - Incoming webhook request
     - Processing messages
     - Any errors (if occur)

3. **Wait 30-60 seconds** for AI processing

4. **Receive response** via WhatsApp!

---

## 🐛 Troubleshooting

### Problem: Service Won't Deploy

**Check:**
- Build logs in Render Dashboard
- Ensure `requirements.txt` is correct
- Verify Python version compatibility

**Common errors:**
- Missing dependencies → Check `requirements.txt`
- Syntax errors → Check Render logs
- Port conflicts → Already handled (port 10000)

### Problem: Service Deployed But Not Responding

**Check:**
1. Visit: `https://your-app.onrender.com/health`
   - Should return: `{"status":"ok"}`
   
2. If not accessible:
   - Check service status in Render Dashboard
   - Free tier may be "asleep" (wakes up on first request)

3. Check Render logs for errors

### Problem: Webhook Not Receiving Messages

**Check:**
1. Twilio Console → Monitor → Logs → Requests
   - See if webhook is being called
   - Check status code (200 = success)

2. Render Dashboard → Logs
   - See if requests are arriving
   - Check for errors

3. Verify webhook URL in Twilio:
   - Must be: `https://your-app.onrender.com/webhook`
   - Must be HTTPS
   - Must end with `/webhook`

### Problem: Getting Responses But They're Empty/Wrong

**Check:**
1. Render Dashboard → Logs
   - Look for error messages
   - Check environment variables are set

2. Verify API keys:
   - OpenAI API key valid
   - Serper.dev API key valid
   - Twilio credentials valid

---

## ✅ Success Checklist

- [ ] Render service deployed and "Live"
- [ ] Health endpoint works: `https://your-app.onrender.com/health`
- [ ] All 5 environment variables added to Render
- [ ] Twilio webhook URL configured correctly
- [ ] Joined WhatsApp sandbox successfully
- [ ] Test message sent
- [ ] Render logs show incoming requests
- [ ] Receive AI response via WhatsApp

---

## 📞 Need Help?

**Check these places:**
1. Render Dashboard → Your Service → Logs
2. Twilio Console → Monitor → Logs → Errors
3. Twilio Console → Monitor → Logs → Requests

**Common solutions:**
- Re-deploy if service is down
- Double-check environment variables
- Verify webhook URL is correct
- Wait a bit longer (AI processing takes time)

---

Once all steps are complete, your MenuMate bot should be working! 🎉

