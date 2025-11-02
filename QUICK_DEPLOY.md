# ⚡ Quick Deploy: GitHub + Render

## ✅ Step-by-Step (5 minutes)

### 1. Commit Code Locally

```bash
cd /Users/dylanlindert/Desktop/Tutai/Assignment5

# Already initialized git, now commit:
git add .
git commit -m "Initial commit: MenuMate WhatsApp bot"
```

### 2. Create GitHub Repo

**Option A: GitHub Website**
1. Go to: https://github.com/new
2. Name: `menumate` (or any name)
3. **Don't** initialize with README
4. Click **Create repository**

**Option B: GitHub CLI** (if you have it)
```bash
gh repo create menumate --public --source=. --remote=origin --push
```

### 3. Push to GitHub

```bash
# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/menumate.git

# Push
git branch -M main
git push -u origin main
```

### 4. Deploy to Render

1. **Sign up:** https://dashboard.render.com/
2. **New** → **Web Service**
3. **Connect GitHub** → Select `menumate` repo
4. **Settings:**
   - Name: `menumate`
   - Build: `pip install -r requirements.txt`
   - Start: `uvicorn main:app --host 0.0.0.0 --port 10000`
5. **Environment Variables:**
   - Add all 5 from your `.env` file:
     - `OPENAI_API_KEY`
     - `SERPER_API_KEY`
     - `TWILIO_ACCOUNT_SID`
     - `TWILIO_AUTH_TOKEN`
     - `TWILIO_WHATSAPP_NUMBER`
6. **Create Web Service**
7. **Wait 5-10 minutes** for deployment
8. **Copy your Render URL** (e.g., `https://menumate.onrender.com`)

### 5. Update Twilio Webhook

1. Go to: https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn
2. **Sandbox Configuration** → **When a message comes in**
3. Paste: `https://YOUR-RENDER-URL.onrender.com/webhook`
4. Method: `POST`
5. **Save**

### 6. Test!

Send WhatsApp message → Get AI response! 🎉

---

**Full details:** See `DEPLOYMENT.md`

