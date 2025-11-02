# 🚀 MenuMate Setup Guide

## Step 1: Get Your API Keys

You'll need API keys from three services:

### 1. OpenAI API Key
1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Navigate to **API Keys** in the left sidebar
4. Click **Create new secret key**
5. Copy the key (starts with `sk-...`)
   - ⚠️ **Important**: You'll only see it once! Save it immediately.

### 2. Serper.dev API Key (for Google Reviews)
1. Go to [Serper.dev](https://serper.dev/)
2. Sign up for a free account
3. You'll get 2,500 free searches per month
4. Copy your API key from the dashboard

### 3. Twilio Account (for WhatsApp)
1. Go to [Twilio Console](https://console.twilio.com/)
2. Sign up for a free account
3. You'll get:
   - **Account SID**: Found in your Twilio dashboard (starts with `AC...`)
   - **Auth Token**: Found in your Twilio dashboard (click "Show" to reveal)
   - **WhatsApp Sandbox Number**: 
     - Go to **Messaging** → **Try it out** → **Send a WhatsApp message**
     - Your sandbox number will be something like `+14155238886`
     - To join the sandbox, send the code word to the number (shown in Twilio console)

## Step 2: Create Your .env File

Create a file named `.env` in the project root with this content:

```bash
OPENAI_API_KEY=sk-your-openai-key-here
SERPER_API_KEY=your-serper-api-key-here
TWILIO_ACCOUNT_SID=ACyour-twilio-account-sid-here
TWILIO_AUTH_TOKEN=your-twilio-auth-token-here
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
```

**Replace the placeholder values with your actual keys!**

## Step 3: Activate Virtual Environment

```bash
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

## Step 4: Test the Server

```bash
uvicorn main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

Visit `http://localhost:8000` in your browser to see the health check!

## Step 5: Test Locally with ngrok (Optional)

For local WhatsApp testing, you'll need to expose your local server:

1. Install [ngrok](https://ngrok.com/download)
2. Run: `ngrok http 8000`
3. Copy the HTTPS URL (e.g., `https://abc123.ngrok.io`)
4. In Twilio Console → WhatsApp Sandbox Settings → Webhook URL: `https://abc123.ngrok.io/webhook`

## Step 6: Deploy to Render (When Ready)

1. Push your code to GitHub
2. Go to [Render Dashboard](https://dashboard.render.com/)
3. Click **New** → **Blueprint**
4. Connect your GitHub repo
5. Render will auto-detect `render.yaml`
6. Add your environment variables in Render dashboard:
   - `OPENAI_API_KEY`
   - `SERPER_API_KEY`
   - `TWILIO_ACCOUNT_SID`
   - `TWILIO_AUTH_TOKEN`
   - `TWILIO_WHATSAPP_NUMBER`
7. Deploy!
8. Update Twilio webhook to point to your Render URL: `https://your-app.onrender.com/webhook`

## 🎉 You're Ready!

Send a WhatsApp message to your Twilio sandbox number with:
- A photo of a restaurant menu
- A question like "What should I order?"

The bot will analyze and respond!

