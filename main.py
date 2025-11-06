"""
MenuMate - AI Menu & Restaurant Advisor
FastAPI application for handling WhatsApp webhooks and processing menu images.
"""
import os
from fastapi import FastAPI, Request
from fastapi.responses import Response
from dotenv import load_dotenv
import asyncio
from typing import Optional
import time

from utils.openai_helper import (
    analyze_menu_image,
    summarize_reviews_and_recommend,
    generate_dish_image
)
from utils.search_helper import search_google_reviews, search_dish_image, get_review_link_for_dish
from utils.whatsapp_helper import (
    send_whatsapp_message,
    format_recommendation_message,
    download_twilio_media,
    download_and_verify_image_url
)

# Load environment variables
load_dotenv()

app = FastAPI(title="MenuMate API", version="1.0.0")

# In-memory cache to store menu images when waiting for restaurant name
# Format: {phone_number: {"image_url": str, "user_question": str, "timestamp": float}}
# Cache expires after 10 minutes
pending_menu_cache = {}
CACHE_EXPIRY_SECONDS = 600  # 10 minutes


@app.get("/")
@app.head("/")
async def root():
    """Health check endpoint. Supports both GET and HEAD for Render health checks."""
    return {
        "status": "healthy",
        "service": "MenuMate - AI Menu & Restaurant Advisor",
        "version": "1.0.0"
    }


@app.get("/health")
@app.head("/health")
async def health():
    """Health check for Render. Supports both GET and HEAD."""
    return {"status": "ok"}


async def process_menu_request(
    from_number: str,
    image_url: str,
    user_question: str
):
    """
    Process menu analysis in the background.
    This function runs after we've responded to Twilio.
    """
    try:
        # Step 1: Download and convert Twilio media if needed
        # Twilio Media URLs require authentication, so we download and convert to base64
        processed_image_url = image_url
        
        if image_url and "api.twilio.com" in image_url:
            # This is a Twilio Media URL - download and convert to base64
            print(f"Downloading Twilio media: {image_url}")
            downloaded_image = await download_twilio_media(image_url)
            if downloaded_image:
                processed_image_url = downloaded_image
                print("Successfully downloaded and converted Twilio media")
            else:
                await send_whatsapp_message(
                    from_number,
                    "⚠️ Sorry, I couldn't download the image from Twilio. Please try sending it again."
                )
                return
        
        # Step 2: Analyze the menu image with GPT-4o
        menu_analysis = await analyze_menu_image(processed_image_url, user_question)
        
        if "error" in menu_analysis:
            await send_whatsapp_message(
                from_number,
                f"⚠️ Sorry, I had trouble analyzing the image. Error: {menu_analysis.get('error', 'Unknown error')}"
            )
            return
        
        restaurant_name = menu_analysis.get("restaurant_name")
        # Handle null values (could be None, "null", or empty string)
        if not restaurant_name or restaurant_name in ["null", "None", ""]:
            restaurant_name = None
        
        menu_items = menu_analysis.get("menu_items", [])
        cuisine_type = menu_analysis.get("cuisine_type", "unknown")
        
        # Step 2.5: Check if user provided restaurant name in the text message
        if not restaurant_name:
            if user_question and user_question.lower() not in ["what should i order?", "what should i order", ""]:
                # Try to extract restaurant name from user question
                # If it's a simple name (not a question), use it
                potential_name = user_question.strip()
                # If it doesn't look like a question, treat as restaurant name
                if not potential_name.endswith("?") and len(potential_name.split()) <= 5:
                    restaurant_name = potential_name
                    print(f"Using restaurant name from user message: {restaurant_name}")
        
        # Step 3: Search for Google Reviews (only if restaurant name is available)
        reviews_data = "No reviews available."
        if restaurant_name:
            reviews_data = await search_google_reviews(restaurant_name)
        else:
            # No restaurant name found - proceed without reviews, analyze menu only
            print("No restaurant name found. Proceeding with menu analysis only (no review search).")
            reviews_data = "No reviews available. Analyzing menu items only."
        
        # Step 4: Summarize reviews and get three recommendations
        recommendation = await summarize_reviews_and_recommend(
            reviews_data,
            menu_items,
            restaurant_name or "the restaurant"
        )
        
        best_reviewed = recommendation.get("best_reviewed", {
            "dish": "Ask the waiter for recommendations",
            "explanation": "Based on available information.",
            "highlights": "No reviews available."
        })
        worst_reviewed = recommendation.get("worst_reviewed", {
            "dish": "Not available",
            "explanation": "Unable to determine.",
            "complaints": "No complaints data available."
        })
        diet_option = recommendation.get("diet_option", {
            "dish": "Not available",
            "explanation": "Unable to determine.",
            "ingredients": "No ingredient data available."
        })
        
        # Step 4.5: Get review links for each dish
        best_dish_name = best_reviewed.get("dish", "")
        worst_dish_name = worst_reviewed.get("dish", "")
        diet_dish_name = diet_option.get("dish", "")
        
        best_review_link = None
        worst_review_link = None
        diet_review_link = None
        
        if restaurant_name:
            if best_dish_name and best_dish_name.lower() not in ["ask the waiter for recommendations", "not available", "n/a"]:
                print(f"Getting review link for best reviewed dish: {best_dish_name}")
                best_review_link = await get_review_link_for_dish(restaurant_name, best_dish_name)
            
            if worst_dish_name and worst_dish_name.lower() not in ["not available", "n/a"]:
                print(f"Getting review link for worst reviewed dish: {worst_dish_name}")
                worst_review_link = await get_review_link_for_dish(restaurant_name, worst_dish_name)
            
            if diet_dish_name and diet_dish_name.lower() not in ["not available", "n/a"]:
                print(f"Getting review link for diet option: {diet_dish_name}")
                diet_review_link = await get_review_link_for_dish(restaurant_name, diet_dish_name)
        
        # Step 5: Find or generate dish image for best reviewed option
        dish_image_url = None
        image_source = None  # Track where the image came from
        review_link = None  # Track review link if from Google
        
        best_dish = best_reviewed.get("dish", "")
        if best_dish and best_dish.lower() not in ["ask the waiter for recommendations", "not available", "n/a"]:
            print(f"Searching for real photo of dish: {best_dish}")
            
            # First, try to find a real photo from Google Images (often from reviews)
            if restaurant_name:
                image_url, source_link = await search_dish_image(restaurant_name, best_dish)
                if image_url:
                    dish_image_url = image_url
                    review_link = source_link
                    image_source = "google"
                    print(f"Found real photo from Google Images")
            
            # If no real photo found, generate one with DALL-E 3
            if not dish_image_url:
                print(f"No real photo found, generating image with DALL-E 3 for: {best_dish}")
                dish_image_url = await generate_dish_image(
                    restaurant_name or "restaurant",
                    best_dish,
                    cuisine_type
                )
                if dish_image_url:
                    image_source = "generated"
                    print(f"Generated image with DALL-E 3")
            
            if dish_image_url:
                print(f"Successfully found/generated dish image: {dish_image_url[:80]}...")
                # Verify the URL is accessible before sending
                verified_url = await download_and_verify_image_url(dish_image_url)
                if verified_url:
                    dish_image_url = verified_url
                    print("Image URL verified and ready to send")
                else:
                    print("Warning: Image URL is not accessible, will send without image")
                    dish_image_url = None
                    image_source = None
                    review_link = None
            else:
                print("Failed to find or generate dish image, will send without image")
        
        # Step 6: Format and send response
        message = format_recommendation_message(
            restaurant_name or "Restaurant",
            best_reviewed,
            worst_reviewed,
            diet_option,
            image_source,
            review_link,
            best_review_link,
            worst_review_link,
            diet_review_link
        )
        
        # Send message with image if available
        if dish_image_url:
            print(f"🖼️ Sending message with dish image URL: {dish_image_url[:80]}...")
            
            # Try sending message with image first
            success = await send_whatsapp_message(
                from_number,
                message,
                media_url=dish_image_url
            )
            
            if success:
                print("✅ Message with image sent successfully!")
            else:
                # Fallback: Try sending image as separate message first, then text
                print("⚠️ Failed to send with image, trying separate messages...")
                image_only_success = await send_whatsapp_message(
                    from_number,
                    f"🖼️ Here's what {best_dish} looks like:",
                    media_url=dish_image_url
                )
                
                if image_only_success:
                    print("✅ Image sent separately, now sending text message...")
                    await send_whatsapp_message(from_number, message)
                else:
                    print("⚠️ Failed to send image separately, sending text only...")
                    await send_whatsapp_message(from_number, message)
        else:
            # Send message without image
            print("ℹ️ Sending message without image (no image available or verification failed)")
            await send_whatsapp_message(from_number, message)
            
    except Exception as e:
        import traceback
        error_traceback = traceback.format_exc()
        
        # Print detailed error to console for debugging
        print("=" * 60)
        print("ERROR IN BACKGROUND PROCESSING:")
        print("=" * 60)
        print(f"Error: {str(e)}")
        print(f"Type: {type(e).__name__}")
        print("\nFull traceback:")
        print(error_traceback)
        print("=" * 60)
        
        # Send error message to user
        try:
            await send_whatsapp_message(
                from_number,
                f"❌ Sorry, an error occurred while processing your request. Please try again."
            )
        except:
            pass


async def process_menu_request_with_restaurant_name(
    from_number: str,
    processed_image_url: str,
    user_question: str,
    restaurant_name: str
):
    """
    Process menu analysis when we have a stored image and restaurant name.
    This is used when user sends restaurant name separately after sending menu image.
    """
    try:
        # Step 2: Analyze the menu image with GPT-4o
        menu_analysis = await analyze_menu_image(processed_image_url, user_question)
        
        if "error" in menu_analysis:
            await send_whatsapp_message(
                from_number,
                f"⚠️ Sorry, I had trouble analyzing the image. Error: {menu_analysis.get('error', 'Unknown error')}"
            )
            return
        
        menu_items = menu_analysis.get("menu_items", [])
        cuisine_type = menu_analysis.get("cuisine_type", "unknown")
        
        # We already have restaurant_name from the parameter, so skip extraction
        
        # Step 3: Search for Google Reviews
        reviews_data = "No reviews available."
        if restaurant_name:
            reviews_data = await search_google_reviews(restaurant_name)
        elif menu_items:
            # Try searching with cuisine type and first menu item
            search_query = f"{cuisine_type} restaurant"
            reviews_data = await search_google_reviews(search_query)
        
        # Step 4: Summarize reviews and get three recommendations
        recommendation = await summarize_reviews_and_recommend(
            reviews_data,
            menu_items,
            restaurant_name or "the restaurant"
        )
        
        best_reviewed = recommendation.get("best_reviewed", {
            "dish": "Ask the waiter for recommendations",
            "explanation": "Based on available information.",
            "highlights": "No reviews available."
        })
        worst_reviewed = recommendation.get("worst_reviewed", {
            "dish": "Not available",
            "explanation": "Unable to determine.",
            "complaints": "No complaints data available."
        })
        diet_option = recommendation.get("diet_option", {
            "dish": "Not available",
            "explanation": "Unable to determine.",
            "ingredients": "No ingredient data available."
        })
        
        # Step 4.5: Get review links for each dish
        best_dish_name = best_reviewed.get("dish", "")
        worst_dish_name = worst_reviewed.get("dish", "")
        diet_dish_name = diet_option.get("dish", "")
        
        best_review_link = None
        worst_review_link = None
        diet_review_link = None
        
        if restaurant_name:
            if best_dish_name and best_dish_name.lower() not in ["ask the waiter for recommendations", "not available", "n/a"]:
                print(f"Getting review link for best reviewed dish: {best_dish_name}")
                best_review_link = await get_review_link_for_dish(restaurant_name, best_dish_name)
            
            if worst_dish_name and worst_dish_name.lower() not in ["not available", "n/a"]:
                print(f"Getting review link for worst reviewed dish: {worst_dish_name}")
                worst_review_link = await get_review_link_for_dish(restaurant_name, worst_dish_name)
            
            if diet_dish_name and diet_dish_name.lower() not in ["not available", "n/a"]:
                print(f"Getting review link for diet option: {diet_dish_name}")
                diet_review_link = await get_review_link_for_dish(restaurant_name, diet_dish_name)
        
        # Step 5: Find or generate dish image for best reviewed option
        dish_image_url = None
        image_source = None  # Track where the image came from
        review_link = None  # Track review link if from Google
        
        best_dish = best_reviewed.get("dish", "")
        if best_dish and best_dish.lower() not in ["ask the waiter for recommendations", "not available", "n/a"]:
            print(f"Searching for real photo of dish: {best_dish}")
            
            # First, try to find a real photo from Google Images (often from reviews)
            if restaurant_name:
                image_url, source_link = await search_dish_image(restaurant_name, best_dish)
                if image_url:
                    dish_image_url = image_url
                    review_link = source_link
                    image_source = "google"
                    print(f"Found real photo from Google Images")
            
            # If no real photo found, generate one with DALL-E 3
            if not dish_image_url:
                print(f"No real photo found, generating image with DALL-E 3 for: {best_dish}")
                dish_image_url = await generate_dish_image(
                    restaurant_name or "restaurant",
                    best_dish,
                    cuisine_type
                )
                if dish_image_url:
                    image_source = "generated"
                    print(f"Generated image with DALL-E 3")
            
            if dish_image_url:
                print(f"Successfully found/generated dish image: {dish_image_url[:80]}...")
                # Verify the URL is accessible before sending
                verified_url = await download_and_verify_image_url(dish_image_url)
                if verified_url:
                    dish_image_url = verified_url
                    print("Image URL verified and ready to send")
                else:
                    print("Warning: Image URL is not accessible, will send without image")
                    dish_image_url = None
                    image_source = None
                    review_link = None
            else:
                print("Failed to find or generate dish image, will send without image")
        
        # Step 6: Format and send response
        message = format_recommendation_message(
            restaurant_name or "Restaurant",
            best_reviewed,
            worst_reviewed,
            diet_option,
            image_source,
            review_link,
            best_review_link,
            worst_review_link,
            diet_review_link
        )
        
        # Send message with image if available
        if dish_image_url:
            print(f"🖼️ Sending message with dish image URL: {dish_image_url[:80]}...")
            
            # Try sending message with image first
            success = await send_whatsapp_message(
                from_number,
                message,
                media_url=dish_image_url
            )
            
            if success:
                print("✅ Message with image sent successfully!")
            else:
                # Fallback: Try sending image as separate message first, then text
                print("⚠️ Failed to send with image, trying separate messages...")
                image_only_success = await send_whatsapp_message(
                    from_number,
                    f"🖼️ Here's what {best_dish} looks like:",
                    media_url=dish_image_url
                )
                
                if image_only_success:
                    print("✅ Image sent separately, now sending text message...")
                    await send_whatsapp_message(from_number, message)
                else:
                    print("⚠️ Failed to send image separately, sending text only...")
                    await send_whatsapp_message(from_number, message)
        else:
            # Send message without image
            print("ℹ️ Sending message without image (no image available or verification failed)")
            await send_whatsapp_message(from_number, message)
            
    except Exception as e:
        import traceback
        error_traceback = traceback.format_exc()
        
        # Print detailed error to console for debugging
        print("=" * 60)
        print("ERROR IN BACKGROUND PROCESSING (WITH RESTAURANT NAME):")
        print("=" * 60)
        print(f"Error: {str(e)}")
        print(f"Type: {type(e).__name__}")
        print("\nFull traceback:")
        print(error_traceback)
        print("=" * 60)
        
        # Send error message to user
        try:
            await send_whatsapp_message(
                from_number,
                f"❌ Sorry, an error occurred while processing your request. Please try again."
            )
        except:
            pass


@app.post("/webhook")
async def webhook(request: Request):
    """
    Handle incoming WhatsApp webhook from Twilio.
    
    CRITICAL: This endpoint responds immediately (within 5 seconds) to prevent
    Twilio 11200 errors. All processing happens in the background using asyncio.create_task.
    
    Twilio sends form data with:
    - From: sender's WhatsApp number
    - Body: text message
    - MediaUrl0, MediaUrl1, etc.: URLs of attached images
    - NumMedia: number of media items
    """
    try:
        # Parse form data from Twilio
        form_data = await request.form()
        
        from_number = form_data.get("From", "").replace("whatsapp:", "")
        body = form_data.get("Body", "").strip()
        num_media = int(form_data.get("NumMedia", "0"))
        
        # Get image URL if present
        image_url = None
        if num_media > 0:
            image_url = form_data.get("MediaUrl0")
        
        # Validate we have an image
        if not image_url:
            # User sent text-only message - ask for menu photo
            if body and body.strip():
                asyncio.create_task(send_whatsapp_message(
                    from_number,
                    "📸 Please send a photo of the menu or restaurant along with your question!\n\n💡 Tip: You can include the restaurant name in your message along with the menu photo."
                ))
            else:
                # No image and no text - ask for menu photo
                asyncio.create_task(send_whatsapp_message(
                    from_number,
                    "📸 Please send a photo of the menu or restaurant along with your question!"
                ))
            return Response(content="OK", status_code=200)
        
        # Get user question or use default
        user_question = body if body else "What should I order?"
        
        # CRITICAL: Respond to Twilio IMMEDIATELY with 200 OK
        # Process everything in the background using asyncio.create_task
        # This creates a fire-and-forget task that runs after we return
        asyncio.create_task(process_menu_request(
            from_number,
            image_url,
            user_question
        ))
        
        # Return immediately - Twilio is happy!
        return Response(content="OK", status_code=200)
        
    except Exception as e:
        import traceback
        error_traceback = traceback.format_exc()
        
        # Print detailed error to console for debugging
        print("=" * 60)
        print("ERROR IN WEBHOOK:")
        print("=" * 60)
        print(f"Error: {str(e)}")
        print(f"Type: {type(e).__name__}")
        print("\nFull traceback:")
        print(error_traceback)
        print("=" * 60)
        
        # Still respond quickly to Twilio, even on error
        return Response(content="OK", status_code=200)


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
