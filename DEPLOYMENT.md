# 🚀 Deployment Guide: GitHub + Render

This guide will help you deploy MenuMate to Render so it runs 24/7 without needing ngrok!

---

## 📋 Prerequisites

- ✅ GitHub account (free)
- ✅ Render account (free tier available)
- ✅ All API keys in `.env` file
- ✅ Project code ready

---

## STEP 1: Prepare for GitHub

### 1A. Verify .gitignore

Make sure `.env` is in `.gitignore` (already done):
```bash
cat .gitignore | grep .env
```

### 1B. Check what will be committed

```bash
git status
```

You should see:
- ✅ `main.py`, `requirements.txt`, etc.
- ✅ `utils/` folder
- ✅ `render.yaml`
- ❌ `.env` should NOT appear (it's ignored)

---

## STEP 2: Create GitHub Repository

### Option A: Using GitHub Website

1. Go to: https://github.com/new
2. Repository name: `menumate` (or any name you like)
3. Description: "AI Menu & Restaurant Advisor - WhatsApp Bot"
4. Choose: **Public** (or Private if you prefer)
5. **DO NOT** initialize with README, .gitignore, or license
6. Click **Create repository**

### Option B: Using GitHub CLI

```bash
gh repo create menumate --public --source=. --remote=origin --push
```

---

## STEP 3: Push Code to GitHub

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Check what's being added (verify .env is NOT listed)
git status

# Commit
git commit -m "Initial commit: MenuMate WhatsApp bot"

# Add GitHub remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/menumate.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Important:** Replace `YOUR_USERNAME` with your actual GitHub username!

---

## STEP 4: Deploy to Render

### 4A. Create Render Account

1. Go to: https://dashboard.render.com/
2. Click **Get Started for Free**
3. Sign up with GitHub (recommended) or email

### 4B. Create New Web Service

1. In Render Dashboard, click **New** → **Web Service**
2. Connect your GitHub account (if not already connected)
3. Select your repository: `menumate` (or whatever you named it)

### 4C. Configure Service

Render should auto-detect settings from `render.yaml`, but verify:

- **Name**: `menumate` (or your choice)
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port 10000`
- **Plan**: Free (or paid if you prefer)

### 4D. Add Environment Variables

In Render dashboard, go to your service → **Environment**:

Add these variables (from your `.env` file):

```
OPENAI_API_KEY          = sk-your-actual-key
SERPER_API_KEY          = your-actual-key
TWILIO_ACCOUNT_SID      = ACyour-actual-sid
TWILIO_AUTH_TOKEN       = your-actual-token
TWILIO_WHATSAPP_NUMBER  = whatsapp:+14155238886
```

**How to add:**
1. Click **Environment** tab
2. Click **Add Environment Variable**
3. Add each one individually
4. Click **Save Changes**

### 4E. Deploy

1. Click **Create Web Service**
2. Render will start building
3. Wait 5-10 minutes for deployment
4. You'll get a URL like: `https://menumate.onrender.com`

---

## STEP 5: Update Twilio Webhook

1. **Get your Render URL:**
   - Render Dashboard → Your Service → Settings
   - Copy the URL (e.g., `https://menumate.onrender.com`)

2. **Update Twilio:**
   - Go to: https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn
   - Scroll to **Sandbox Configuration**
   - **When a message comes in**: `https://menumate.onrender.com/webhook`
   - **HTTP Method**: `POST`
   - Click **Save**

---

## STEP 6: Test!

1. **Send WhatsApp message** with menu photo
2. **Check Render logs:**
   - Render Dashboard → Your Service → Logs
   - You should see requests coming in

3. **Receive AI response** via WhatsApp!

---

## 🎉 Benefits of Render Deployment

- ✅ No ngrok needed (runs 24/7)
- ✅ Real HTTPS URL (no timeouts)
- ✅ Free tier available
- ✅ Auto-deploys on git push
- ✅ Better for production

---

## 🔄 Updating Code

Whenever you make changes:

```bash
git add .
git commit -m "Description of changes"
git push
```

Render will automatically redeploy!

---

## 🐛 Troubleshooting

### Build Fails
- Check Render logs for errors
- Verify `requirements.txt` is correct
- Check Python version compatibility

### Service Not Starting
- Check logs in Render dashboard
- Verify environment variables are set
- Check start command is correct

### Webhook Not Working
- Verify Render URL is accessible
- Check Twilio webhook URL matches exactly
- Look at Render logs for incoming requests

### API Errors
- Verify all environment variables in Render
- Check API keys are correct
- Review logs for specific errors

---

## 📚 Additional Resources

- Render Docs: https://render.com/docs
- Render Status: https://status.render.com/
- Twilio Webhook Guide: https://www.twilio.com/docs/whatsapp/tutorial/send-and-receive-messages

---

**Need help?** Check Render logs and Twilio error logs for details!

