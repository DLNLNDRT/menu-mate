# ✅ Quick Fix Checklist - No WhatsApp Replies

## 🔍 Diagnose First

### Check 1: Render Deployment
```
☐ Go to: https://dashboard.render.com/
☐ Do you see a service?
☐ Is it "Live" (green)?
☐ What's the URL? (e.g., https://menu-mate.onrender.com)
```

**If NO service:**
→ Follow "STEP 1-6: Deploy to Render" below

**If service exists but not Live:**
→ Check logs for errors
→ Verify environment variables are set

### Check 2: Render URL Works
```
☐ Visit: https://your-app.onrender.com/health
☐ Does it show: {"status":"ok"}?
```

**If NO:**
→ Service might be down or sleeping (free tier)
→ Check Render dashboard for errors

### Check 3: Twilio Webhook
```
☐ Go to: https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn
☐ Scroll to "Sandbox Configuration"
☐ Check "When a message comes in" URL
☐ Is it: https://your-render-url.onrender.com/webhook ?
☐ Method is POST?
```

**If NO or wrong:**
→ Update webhook URL (see Step 7 below)

### Check 4: Environment Variables
```
☐ Render Dashboard → Your Service → Environment
☐ Do you have all 5 variables?
  • OPENAI_API_KEY
  • SERPER_API_KEY
  • TWILIO_ACCOUNT_SID
  • TWILIO_AUTH_TOKEN
  • TWILIO_WHATSAPP_NUMBER
```

**If NO:**
→ Add missing variables (see Step 5 below)

---

## 🚀 Step-by-Step Setup

### STEP 1: Deploy to Render (if not done)

1. **Go to:** https://dashboard.render.com/
2. **Sign up/Login** (free account)
3. **Click:** "New +" → "Web Service"
4. **Connect GitHub:**
   - Authorize Render
   - Select: `DLNLNDRT/menu-mate`
5. **Settings (auto-filled from render.yaml):**
   - Name: `menu-mate`
   - Environment: `Python 3`
   - Build: `pip install -r requirements.txt`
   - Start: `uvicorn main:app --host 0.0.0.0 --port 10000`
6. **Click:** "Create Web Service"
7. **Wait 5-10 minutes** for deployment

---

### STEP 2: Get Your Render URL

Once deployed:
- Status shows **"Live"** (green)
- Your URL is at the top
- Example: `https://menu-mate.onrender.com`
- **Copy this URL!**

---

### STEP 3: Test Render URL

Visit: `https://your-app.onrender.com/health`

Should show: `{"status":"ok"}`

**If it works:** ✅ Render is working!
**If not:** Check Render logs for errors

---

### STEP 4: Add Environment Variables

**In Render Dashboard → Your Service:**

1. Click **"Environment"** tab
2. Click **"Add Environment Variable"**
3. Add each one (copy from your `.env` file):

```
Key: OPENAI_API_KEY
Value: sk-your-actual-key-from-env-file

Key: SERPER_API_KEY  
Value: your-actual-key-from-env-file

Key: TWILIO_ACCOUNT_SID
Value: ACyour-actual-sid-from-env-file

Key: TWILIO_AUTH_TOKEN
Value: your-actual-token-from-env-file

Key: TWILIO_WHATSAPP_NUMBER
Value: whatsapp:+14155238886
```

4. After adding all 5, Render will **auto-redeploy**
5. Wait for redeployment to complete

---

### STEP 5: Configure Twilio Webhook

1. **Go to:** https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn
2. **Scroll to:** "Sandbox Configuration"
3. **Find:** "When a message comes in"
4. **Enter:** `https://your-render-url.onrender.com/webhook`
   - Replace `your-render-url` with your actual Render URL
   - Example: `https://menu-mate.onrender.com/webhook`
5. **HTTP Method:** Select `POST`
6. **Click:** "Save"

---

### STEP 6: Verify Webhook in Twilio

1. **Go to:** Twilio Console → Monitor → Logs → Requests
2. **Send a test WhatsApp message**
3. **Check if:**
   - Request appears in logs
   - Status code is 200 (success)
   - URL matches your Render webhook

---

### STEP 7: Test End-to-End

1. **Send WhatsApp:**
   - Open WhatsApp
   - Send to sandbox number
   - Attach menu photo
   - Add text: "What should I order?"

2. **Check Render Logs:**
   - Render Dashboard → Your Service → Logs
   - Should see incoming request
   - Should see processing messages

3. **Wait 30-60 seconds**
   - AI needs time to process

4. **Check WhatsApp:**
   - Should receive AI recommendation!

---

## 🐛 Common Issues & Fixes

### Issue: "Service unavailable"
**Fix:** 
- Free tier may be sleeping
- Send message - it will wake up
- First request takes longer

### Issue: "Webhook timeout"
**Fix:**
- Code already handles this (responds immediately)
- Check if service is running
- Check Render logs

### Issue: "No requests in Twilio logs"
**Fix:**
- Verify webhook URL in Twilio is correct
- Must be HTTPS
- Must end with `/webhook`
- Try saving webhook again

### Issue: "Errors in Render logs"
**Fix:**
- Check environment variables are set
- Verify API keys are correct
- Check error message for details

---

## ✅ Success Indicators

You know it's working when:
- ✅ Render service shows "Live"
- ✅ Health endpoint returns `{"status":"ok"}`
- ✅ Twilio logs show 200 status code
- ✅ Render logs show incoming requests
- ✅ You receive WhatsApp response within 30-60 seconds

---

**Still having issues?** Share:
1. Render service status
2. Any errors in Render logs
3. What you see in Twilio logs
4. Your Render URL

