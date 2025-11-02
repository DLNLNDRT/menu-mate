# 📱 Twilio WhatsApp Sandbox Setup Guide

Complete step-by-step guide to set up Twilio WhatsApp Sandbox and connect it to MenuMate.

---

## 📋 Prerequisites

- ✅ Twilio account created (free tier available)
- ✅ Render service deployed (for webhook URL)
- ✅ WhatsApp installed on your phone

---

## STEP 1: Access Twilio Console

1. **Go to:** https://console.twilio.com/
2. **Sign up** (if you don't have an account):
   - Free account includes WhatsApp sandbox
   - No credit card required for sandbox testing

3. **Log in** to your Twilio account

---

## STEP 2: Navigate to WhatsApp Sandbox

### Option A: Direct Link
- Go to: https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn

### Option B: Through Console
1. In Twilio Dashboard, click **"Messaging"** (left sidebar)
2. Click **"Try it out"** 
3. Click **"Send a WhatsApp message"**
4. You'll see the **WhatsApp Sandbox** page

---

## STEP 3: Join the WhatsApp Sandbox

### 3A. Find Your Sandbox Information

On the WhatsApp Sandbox page, you'll see:

- **Sandbox number:** Usually `+1 415 523 8886` (or shown on page)
- **Join code word:** Something like `join example-code` (shown on page)

**Example:**
```
Send a WhatsApp message to +1 415 523 8886
with the join code word: join example-abc123
```

### 3B. Join from Your Phone

1. **Open WhatsApp** on your phone
2. **Send a message** to the sandbox number:
   - Number: `+1 415 523 8886` (or the number shown)
3. **Send the join code word:**
   - Example: `join example-abc123`
   - Use the EXACT code word shown on Twilio page

4. **Wait for confirmation:**
   - You'll receive: **"You're all set! You've joined the sandbox."**
   - If you see this, you're connected! ✅

---

## STEP 4: Configure the Webhook

This tells Twilio where to send incoming messages (your Render server).

### 4A. Get Your Render URL

1. Go to: https://dashboard.render.com/
2. Find your deployed service
3. Copy your Render URL (e.g., `https://menu-mate.onrender.com`)

### 4B. Set Webhook URL in Twilio

1. **On WhatsApp Sandbox page**, scroll to **"Sandbox Configuration"** section
2. Find **"When a message comes in"** field
3. **Enter your webhook URL:**
   ```
   https://your-render-url.onrender.com/webhook
   ```
   - Replace `your-render-url` with your actual Render URL
   - Example: `https://menu-mate.onrender.com/webhook`
   - **Must end with `/webhook`**

4. **HTTP Method:** Select `POST` (should be default)

5. **Click "Save"** (bottom of the form)

---

## STEP 5: Verify Webhook Configuration

### 5A. Check Webhook Settings

After saving, verify:
- ✅ Webhook URL is correct (HTTPS, ends with `/webhook`)
- ✅ HTTP Method is `POST`
- ✅ No error messages shown

### 5B. Test Webhook Connection

1. **In Twilio Console:**
   - Go to: **Monitor → Logs → Requests**
   
2. **Send a test WhatsApp message:**
   - Open WhatsApp
   - Send a message to sandbox number
   - Any message will do

3. **Check Twilio Logs:**
   - You should see a request appear
   - Status code should be `200` (success)
   - URL should match your webhook

---

## STEP 6: Test End-to-End

### 6A. Send a Menu Photo

1. **Open WhatsApp**
2. **Send to sandbox number:** `+1 415 523 8886`
3. **Attach a menu photo** (or any restaurant menu image)
4. **Add text:** "What should I order?" (optional)

### 6B. Check the Flow

1. **Check Twilio Logs:**
   - Monitor → Logs → Requests
   - Should show webhook called
   - Status should be `200`

2. **Check Render Logs:**
   - Render Dashboard → Your Service → Logs
   - Should show incoming request
   - Should show processing messages

3. **Wait 30-60 seconds:**
   - AI needs time to process the image

4. **Check WhatsApp:**
   - You should receive AI recommendation!

---

## 🔍 Troubleshooting

### Problem: "You're all set" message not received

**Solutions:**
- ✅ Verify sandbox number is correct
- ✅ Use EXACT join code word (case-sensitive)
- ✅ Make sure you're sending from WhatsApp (not SMS)
- ✅ Try sending join code again
- ✅ Check you're using the correct phone number

### Problem: Webhook returns errors

**Check:**
1. **Render service is running:**
   - Visit: `https://your-url.onrender.com/health`
   - Should return: `{"status":"ok"}`

2. **Webhook URL is correct:**
   - Must be HTTPS
   - Must end with `/webhook`
   - No typos in URL

3. **Environment variables set in Render:**
   - All 5 API keys must be configured
   - Check Render Dashboard → Environment

4. **Check Render logs:**
   - Look for error messages
   - Verify requests are arriving

### Problem: Messages received but no reply

**Check:**
1. **Render logs:**
   - Are requests arriving?
   - Any error messages?
   - Is processing happening?

2. **Environment variables:**
   - All set correctly in Render?
   - API keys are valid?

3. **Wait longer:**
   - First request may take 60+ seconds
   - Free tier may be slow to start

### Problem: "11200 Error" in Twilio

**This is fixed in the code:**
- Webhook responds immediately
- Processing happens in background
- If still seeing this, check Render service is running

---

## 📱 Sandbox Limitations

**Free Sandbox:**
- ✅ Only works with numbers you've joined
- ✅ Limited to testing (not production)
- ✅ No monthly limits on messages during testing

**For Production:**
- Need to request WhatsApp Business API access
- Apply through Twilio
- Approval process required

---

## ✅ Success Checklist

- [ ] Twilio account created
- [ ] WhatsApp Sandbox page accessed
- [ ] Joined sandbox successfully (received confirmation)
- [ ] Render service deployed and running
- [ ] Render URL obtained
- [ ] Webhook URL configured in Twilio
- [ ] Webhook URL ends with `/webhook`
- [ ] HTTP Method set to `POST`
- [ ] Webhook saved successfully
- [ ] Test message sent
- [ ] Twilio logs show webhook called (status 200)
- [ ] Render logs show incoming requests
- [ ] Received AI response via WhatsApp!

---

## 🎯 Quick Reference

**Sandbox Number:** Usually `+1 415 523 8886`  
**Join Code:** Check Twilio Console (changes per account)  
**Webhook Format:** `https://your-app.onrender.com/webhook`  
**Method:** `POST`

**Links:**
- Twilio Sandbox: https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn
- Twilio Dashboard: https://console.twilio.com/
- Render Dashboard: https://dashboard.render.com/

---

## 📞 Need More Help?

**Check these:**
- Render Dashboard → Your Service → Logs
- Twilio Console → Monitor → Logs → Requests
- Twilio Console → Monitor → Logs → Errors

**Common fixes:**
- Re-save webhook URL in Twilio
- Restart Render service
- Verify all environment variables in Render
- Try joining sandbox again

Once setup is complete, MenuMate will receive WhatsApp messages and send AI-powered recommendations! 🎉

