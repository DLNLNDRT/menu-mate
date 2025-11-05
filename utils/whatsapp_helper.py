"""
Twilio WhatsApp API helper for sending messages and downloading media.
"""
import os
import asyncio
import requests
import base64
from twilio.rest import Client
from typing import Optional, Dict


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
        import traceback
        print(f"Error sending WhatsApp message: {e}")
        print(f"Full error details: {traceback.format_exc()}")
        if media_url:
            print(f"Failed to send media URL: {media_url[:100]}")
        return False


def truncate_text(text: str, max_length: int) -> str:
    """
    Truncate text to a maximum length, ensuring it ends at a word boundary.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        
    Returns:
        Truncated text with "..." if needed
    """
    if len(text) <= max_length:
        return text
    
    # Truncate and find last space before max_length
    truncated = text[:max_length - 3]
    last_space = truncated.rfind(' ')
    if last_space > max_length * 0.8:  # Only use word boundary if it's not too short
        truncated = truncated[:last_space]
    
    return truncated + "..."


def format_recommendation_message(
    restaurant_name: str,
    best_reviewed: Dict,
    worst_reviewed: Dict,
    diet_option: Dict,
    image_source: Optional[str] = None,
    review_link: Optional[str] = None,
    best_review_link: Optional[str] = None,
    worst_review_link: Optional[str] = None,
    diet_review_link: Optional[str] = None
) -> str:
    """
    Format a recommendation message for WhatsApp with three options.
    Ensures message stays under 1500 characters for Twilio limits.
    Dish names are hyperlinked if review links are available.
    
    Args:
        restaurant_name: Name of the restaurant
        best_reviewed: Dict with dish, explanation, and highlights
        worst_reviewed: Dict with dish, explanation, and complaints
        diet_option: Dict with dish, explanation, and ingredients
        image_source: Source of the dish image ("google" or "generated" or None)
        review_link: URL to the review page if image is from Google
        best_review_link: URL to reviews for best reviewed dish
        worst_review_link: URL to reviews for worst reviewed dish
        diet_review_link: URL to reviews for diet option
        
    Returns:
        Formatted message string (max 1500 characters)
    """
    MAX_LENGTH = 1500
    
    # Truncate individual text fields to reasonable lengths
    # Allocate space: ~500 chars for each main section, ~200 for header/footer
    def truncate_field(text: str, max_chars: int) -> str:
        if len(text) <= max_chars:
            return text
        return truncate_text(text, max_chars)
    
    best_explanation = truncate_field(best_reviewed.get('explanation', ''), 180)
    best_highlights = truncate_field(best_reviewed.get('highlights', 'No highlights available'), 130)
    
    worst_explanation = truncate_field(worst_reviewed.get('explanation', ''), 180)
    worst_complaints = truncate_field(worst_reviewed.get('complaints', 'No complaints available'), 130)
    
    diet_explanation = truncate_field(diet_option.get('explanation', ''), 180)
    diet_ingredients = truncate_field(diet_option.get('ingredients', 'Not available'), 130)
    
    # Format dish names - WhatsApp doesn't support markdown links, so we format as:
    # *Dish Name* - https://url.com (WhatsApp will auto-detect and make URL clickable)
    best_dish_name = best_reviewed.get('dish', 'N/A')
    if best_review_link:
        best_dish_formatted = f"*{best_dish_name}*\n🔗 {best_review_link}"
    else:
        best_dish_formatted = f"*{best_dish_name}*"
    
    worst_dish_name = worst_reviewed.get('dish', 'N/A')
    if worst_review_link:
        worst_dish_formatted = f"*{worst_dish_name}*\n🔗 {worst_review_link}"
    else:
        worst_dish_formatted = f"*{worst_dish_name}*"
    
    diet_dish_name = diet_option.get('dish', 'N/A')
    if diet_review_link:
        diet_dish_formatted = f"*{diet_dish_name}*\n🔗 {diet_review_link}"
    else:
        diet_dish_formatted = f"*{diet_dish_name}*"
    
    # Build message
    message = f"""🍽 *Restaurant:* {restaurant_name or 'Unknown'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ *BEST REVIEWED:*
{best_dish_formatted}

{best_explanation}

⭐ *Review Highlights:*
{best_highlights}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❌ *WORST REVIEWED (Avoid):*
{worst_dish_formatted}

{worst_explanation}

⚠️ *Complaints:*
{worst_complaints}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🥗 *BEST DIET OPTION:*
{diet_dish_formatted}

{diet_explanation}

🥬 *Ingredients & Benefits:*
{diet_ingredients}"""
    
    # Add image source information if available
    if image_source == "google":
        message += "\n\n📷 *Photo:* Real customer photo from Google Reviews"
        if review_link:
            message += f"\n🔗 *View Review:* {review_link}"
    elif image_source == "generated":
        message += "\n\n🎨 *Photo:* AI-generated image"
    
    message += "\n\nBon appétit! 🍴"
    
    # Final safety check: if still too long, truncate the entire message
    if len(message) > MAX_LENGTH:
        # Truncate from the end, keeping the beginning intact
        excess = len(message) - MAX_LENGTH + 20  # Add buffer
        message = message[:-excess] + "...\n\nBon appétit! 🍴"
    
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


async def download_and_verify_image_url(image_url: str) -> Optional[str]:
    """
    Download an image from a URL and verify it's accessible.
    Returns the original URL if accessible, or None if not.
    
    This is useful for verifying DALL-E URLs before sending to Twilio.
    
    Args:
        image_url: URL of the image to verify
        
    Returns:
        The original URL if accessible, None if not
    """
    try:
        print(f"Verifying image URL is accessible: {image_url[:80]}...")
        response = await asyncio.to_thread(
            requests.get,
            image_url,
            timeout=10,
            stream=True  # Don't download full content, just verify
        )
        response.raise_for_status()
        
        # Check if it's actually an image
        content_type = response.headers.get('Content-Type', '').lower()
        if not content_type.startswith('image/'):
            print(f"URL does not point to an image (Content-Type: {content_type})")
            return None
        
        print(f"Image URL verified: {content_type}")
        return image_url
        
    except Exception as e:
        print(f"Error verifying image URL: {e}")
        return None
