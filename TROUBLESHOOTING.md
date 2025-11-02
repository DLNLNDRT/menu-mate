# 🔧 Troubleshooting: No WhatsApp Replies

## Common Issues & Solutions

### Issue 1: Render Not Deployed Yet
**Symptoms:** No response when sending WhatsApp message

**Solution:**
1. Go to https://dashboard.render.com/
2. Check if you have a web service deployed
3. If not, follow deployment steps below

### Issue 2: Webhook URL Incorrect
**Symptoms:** Twilio shows webhook errors

**Solution:**
1. Get your Render URL (e.g., `https://menu-mate.onrender.com`)
2. Update Twilio webhook to: `https://your-app.onrender.com/webhook`
3. Must end with `/webhook`

### Issue 3: Environment Variables Missing
**Symptoms:** Errors in Render logs about missing API keys

**Solution:**
1. Render Dashboard → Your Service → Environment
2. Add all 5 variables from your `.env` file
3. Redeploy

### Issue 4: Service Not Running
**Symptoms:** Render shows "Service Unavailable"

**Solution:**
1. Check Render logs for errors
2. Verify build succeeded
3. Check if service is "Live"

---

## Quick Checklist

- [ ] Render service deployed and running
- [ ] Render URL is accessible (try visiting it)
- [ ] Twilio webhook URL matches Render URL + `/webhook`
- [ ] All 5 environment variables set in Render
- [ ] Service status is "Live" in Render
- [ ] You joined WhatsApp sandbox successfully

