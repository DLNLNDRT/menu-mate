# 🍽️ MenuMate — AI Menu & Restaurant Advisor

An AI-powered WhatsApp bot that analyzes restaurant menus from photos, searches Google reviews, and recommends the best dishes to order.

## 🎯 Features

- **Image Analysis**: Uses OpenAI GPT-4o to extract restaurant names, menu items, and cuisine type from photos
- **Review Search**: Integrates with Serper.dev to find and analyze Google Reviews
- **AI Recommendations**: GPT-4o summarizes reviews and recommends the best dish with reasoning
- **Image Generation**: Optional DALL-E 3 generated images of recommended dishes
- **WhatsApp Integration**: Seamless communication via Twilio WhatsApp API

## 🏗️ Architecture

```
WhatsApp → Twilio Webhook → FastAPI (/webhook) → OpenAI GPT-4o → Serper.dev → Twilio API → WhatsApp
```

## 📋 Prerequisites

- Python 3.9+
- OpenAI API key (for GPT-4o and DALL-E 3)
- Serper.dev API key (for Google Reviews search)
- Twilio account with WhatsApp API access
- Render account (for deployment)

## 🚀 Setup

### 1. Clone and Install Dependencies

```bash
cd menu-mate
pip install -r requirements.txt
```

### 2. Environment Variables

Create a `.env` file in the root directory:

```bash
OPENAI_API_KEY=sk-your-openai-key
SERPER_API_KEY=your-serper-api-key
TWILIO_ACCOUNT_SID=your-twilio-account-sid
TWILIO_AUTH_TOKEN=your-twilio-auth-token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
```

### 3. Local Development

Run the FastAPI server:

```bash
uvicorn main:app --reload --port 8000
```

The server will start at `http://localhost:8000`

### 4. Testing Webhook Locally

Use a tool like [ngrok](https://ngrok.com/) to expose your local server:

```bash
ngrok http 8000
```

Use the ngrok URL in your Twilio webhook configuration: `https://your-ngrok-url.ngrok.io/webhook`

## 📱 Twilio WhatsApp Setup

1. **Get Twilio WhatsApp Sandbox**:
   - Go to [Twilio Console](https://console.twilio.com/)
   - Navigate to Messaging → Try it out → Send a WhatsApp message
   - Follow instructions to join the sandbox

2. **Configure Webhook**:
   - In Twilio Console → Messaging → Settings → WhatsApp Sandbox Settings
   - Set webhook URL to: `https://your-render-app.onrender.com/webhook`
   - Set HTTP method to: `POST`

3. **Send a Test Message**:
   - Send a photo of a menu with a question like "What should I order?"
   - The bot will analyze and respond with recommendations

## 🚢 Deployment to Render

### Method 1: Using render.yaml

1. Push your code to GitHub
2. In Render Dashboard, click "New" → "Blueprint"
3. Connect your GitHub repository
4. Render will automatically detect `render.yaml` and deploy

### Method 2: Manual Deployment

1. In Render Dashboard, click "New" → "Web Service"
2. Connect your GitHub repository
3. Configure:
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port 10000`
4. Add environment variables from your `.env` file
5. Deploy!

### Environment Variables in Render

Add these in Render Dashboard → Your Service → Environment:

- `OPENAI_API_KEY`
- `SERPER_API_KEY`
- `TWILIO_ACCOUNT_SID`
- `TWILIO_AUTH_TOKEN`
- `TWILIO_WHATSAPP_NUMBER`

## 📖 API Endpoints

### `GET /`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "MenuMate - AI Menu & Restaurant Advisor",
  "version": "1.0.0"
}
```

### `POST /webhook`
Webhook endpoint for Twilio WhatsApp messages.

**Expected Form Data (from Twilio):**
- `From`: WhatsApp number of sender
- `Body`: Text message from user
- `MediaUrl0`: URL of first image attachment
- `NumMedia`: Number of media attachments

## 🧪 Example Usage Flow

1. User sends WhatsApp message:
   - **Image**: Photo of restaurant menu
   - **Text**: "What should I order?"

2. Bot processes:
   - Analyzes image with GPT-4o
   - Extracts restaurant name: "Chez Janou"
   - Extracts menu items: ["Magret de Canard", "Coq au Vin", ...]
   - Searches Google Reviews via Serper.dev
   - GPT-4o analyzes reviews and recommends best dish

3. Bot responds:
   ```
   🍽 Restaurant: Chez Janou, Paris
   
   ✅ Best Dish: Magret de Canard au Romarin
   
   💬 Why this dish?
   Succulent duck with perfect cooking and rich rosemary aroma.
   
   ⭐ Review Highlights:
   "Amazing duck dish! Perfectly cooked and flavorful."
   ```

## 📁 Project Structure

```
menu-mate/
├── main.py                 # FastAPI application entrypoint
├── requirements.txt        # Python dependencies
├── render.yaml            # Render deployment configuration
├── .env                   # Environment variables (not in git)
├── README.md              # This file
└── utils/
    ├── __init__.py
    ├── openai_helper.py   # OpenAI API functions
    ├── search_helper.py   # Serper.dev search functions
    └── whatsapp_helper.py # Twilio WhatsApp functions
```

## 🔧 Configuration

### OpenAI Models Used

- **GPT-4o**: For image analysis and review summarization
- **DALL-E 3**: For generating dish images (optional)

### API Limits

- OpenAI GPT-4o: Pay-per-use (check your plan limits)
- Serper.dev: Free tier includes 2,500 searches/month
- Twilio: WhatsApp Sandbox is free for testing

## 🐛 Troubleshooting

### Image Analysis Fails
- Ensure the image URL is publicly accessible
- Check OpenAI API key and quota
- Verify image format is supported (JPG, PNG, etc.)

### Reviews Not Found
- Restaurant name might not be clearly visible in image
- Try a clearer photo or specify restaurant in text message
- Check Serper.dev API key and quota

### WhatsApp Messages Not Sending
- Verify Twilio credentials in `.env`
- Check webhook URL is correctly configured in Twilio
- Ensure Render app is running and accessible

## 🚀 Future Improvements

- [ ] Cache restaurant data in SQLite for faster responses
- [ ] Auto-translate non-English menu items
- [ ] Recommend both "Best" and "Most Overrated" dishes
- [ ] Confidence score for restaurant identification
- [ ] Visual dish recognition for "rate my dish" photos

## 📝 License

This project is open source and available for personal and commercial use.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues and questions, please open an issue on GitHub.

---

Built with ❤️ using OpenAI, Twilio, and FastAPI
