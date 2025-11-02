"""
Twilio WhatsApp API helper for sending messages and downloading media.
"""
import os
import asyncio
import requests
import base64
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
    
    # Ensure whatsapp_number has whatsapp: prefix
    if whatsapp_number and not whatsapp_number.startswith("whatsapp:"):
        whatsapp_number = f"whatsapp:{whatsapp_number}"
    
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


async def download_twilio_media(media_url: str) -> Optional[str]:
    """
    Download media from Twilio Media URL and convert to base64 data URL.
    
    Twilio Media URLs require authentication, so we download using Twilio credentials
    and convert to base64 format that OpenAI can use.
    
    Args:
        media_url: Twilio Media URL (e.g., https://api.twilio.com/.../Media/...)
        
    Returns:
        Base64 data URL string (e.g., "data:image/jpeg;base64,...") or None if fails
    """
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    
    if not account_sid or not auth_token:
        print("Twilio credentials not available for media download")
        return None
    
    try:
        # Download image with Basic Auth using Twilio credentials
        response = await asyncio.to_thread(
            requests.get,
            media_url,
            auth=(account_sid, auth_token),
            timeout=30
        )
        response.raise_for_status()
        
        # Get content type
        content_type = response.headers.get('Content-Type', 'image/jpeg')
        
        # Convert to base64
        image_base64 = base64.b64encode(response.content).decode('utf-8')
        
        # Create data URL format that OpenAI accepts
        data_url = f"data:{content_type};base64,{image_base64}"
        
        return data_url
        
    except Exception as e:
        print(f"Error downloading Twilio media: {e}")
        return None
