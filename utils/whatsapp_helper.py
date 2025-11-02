"""
Twilio WhatsApp API helper for sending messages.
"""
import os
from twilio.rest import Client
from typing import Optional


def get_twilio_client() -> Optional[Client]:
    """
    Initialize and return Twilio client.
    
    Returns:
        Twilio Client instance or None if credentials are missing
    """
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    
    if not account_sid or not auth_token:
        return None
    
    return Client(account_sid, auth_token)


async def send_whatsapp_message(
    to_number: str,
    message: str,
    media_url: Optional[str] = None
) -> bool:
    """
    Send a WhatsApp message via Twilio.
    
    Args:
        to_number: Recipient's WhatsApp number (e.g., "+1234567890" or "whatsapp:+1234567890")
        message: Message text to send
        media_url: Optional URL of image to include
        
    Returns:
        True if message sent successfully, False otherwise
    """
    client = get_twilio_client()
    if not client:
        print("Twilio client not initialized - check credentials")
        return False
    
    whatsapp_number = os.getenv("TWILIO_WHATSAPP_NUMBER", "whatsapp:+14155238886")
    
    # Ensure to_number has whatsapp: prefix to match the channel
    if not to_number.startswith("whatsapp:"):
        to_number = f"whatsapp:{to_number}"
    
    try:
        message_params = {
            "from_": whatsapp_number,  # Use from_ because 'from' is a Python keyword
            "to": to_number,
            "body": message
        }
        
        if media_url:
            message_params["media_url"] = [media_url]
        
        message = client.messages.create(**message_params)
        print(f"Message sent: {message.sid}")
        return True
        
    except Exception as e:
        print(f"Error sending WhatsApp message: {e}")
        return False


def format_recommendation_message(
    restaurant_name: str,
    best_dish: str,
    reasoning: str,
    review_highlights: str
) -> str:
    """
    Format a recommendation message for WhatsApp.
    
    Args:
        restaurant_name: Name of the restaurant
        best_dish: Recommended dish name
        reasoning: Brief explanation
        review_highlights: Key highlights from reviews
        
    Returns:
        Formatted message string
    """
    # Use emojis to make it visually appealing
    message = f"""🍽 *Restaurant:* {restaurant_name or 'Unknown'}

✅ *Best Dish:* {best_dish}

💬 *Why this dish?*
{reasoning}

⭐ *Review Highlights:*
{review_highlights}

Bon appétit! 🍴"""
    
    return message
