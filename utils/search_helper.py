"""
Serper.dev API helper for searching Google Reviews and Images.
"""
import os
import asyncio
import requests
from typing import Optional, Dict


async def search_google_reviews(restaurant_name: str, location: Optional[str] = None) -> str:
    """
    Search for Google reviews of a restaurant using Serper.dev API.
    
    Args:
        restaurant_name: Name of the restaurant
        location: Optional location (city, address) to narrow search
        
    Returns:
        String containing review snippets and ratings
    """
    api_key = os.getenv("SERPER_API_KEY")
    if not api_key:
        return "No API key configured for reviews search."
    
    # Build search query
    query = f"{restaurant_name} reviews"
    if location:
        query += f" {location}"
    
    try:
        url = "https://google.serper.dev/search"
        headers = {
            "X-API-KEY": api_key,
            "Content-Type": "application/json"
        }
        
        payload = {
            "q": query,
            "num": 10  # Get top 10 results
        }
        
        response = await asyncio.to_thread(
            requests.post, url, headers=headers, json=payload, timeout=10
        )
        response.raise_for_status()
        data = response.json()
        
        # Extract review snippets from organic results
        reviews_text = []
        
        # Get organic results
        if "organic" in data:
            for result in data["organic"][:5]:  # Top 5 results
                snippet = result.get("snippet", "")
                title = result.get("title", "")
                if snippet:
                    reviews_text.append(f"{title}: {snippet}")
        
        # Try to get answer box or knowledge graph info
        if "answerBox" in data:
            answer = data["answerBox"]
            reviews_text.insert(0, f"Featured: {answer.get('snippet', '')}")
        
        # Combine all reviews
        reviews_combined = "\n\n".join(reviews_text)
        
        if not reviews_combined.strip():
            return f"No reviews found for {restaurant_name}. You may want to try asking the staff for recommendations."
        
        return reviews_combined
        
    except requests.exceptions.RequestException as e:
        return f"Error searching reviews: {str(e)}. Try asking the staff for recommendations."
    except Exception as e:
        return f"Unexpected error: {str(e)}"


async def search_dish_image(restaurant_name: str, dish_name: str) -> tuple[Optional[str], Optional[str]]:
    """
    Search for real photos of a dish from Google Images (often from reviews).
    This finds actual user-uploaded photos from Google Reviews or restaurant sites.
    
    Args:
        restaurant_name: Name of the restaurant
        dish_name: Name of the dish to search for
        
    Returns:
        Tuple of (image_url, review_link) where:
        - image_url: URL of the first relevant image found, or None if no image found
        - review_link: URL to the source page (Google Review, etc.), or None if not available
    """
    api_key = os.getenv("SERPER_API_KEY")
    if not api_key:
        print("No SERPER_API_KEY configured for image search")
        return None, None
    
    # Build search query - search for restaurant + dish name
    # This often returns review photos
    query = f"{restaurant_name} {dish_name}"
    
    try:
        url = "https://google.serper.dev/images"
        headers = {
            "X-API-KEY": api_key,
            "Content-Type": "application/json"
        }
        
        payload = {
            "q": query,
            "num": 5  # Get top 5 images
        }
        
        print(f"Searching Google Images for: {query}")
        response = await asyncio.to_thread(
            requests.post, url, headers=headers, json=payload, timeout=10
        )
        response.raise_for_status()
        data = response.json()
        
        # Extract image URLs and source links from results
        if "images" in data and len(data["images"]) > 0:
            # Get the first image that looks relevant
            for image in data["images"][:3]:  # Check top 3 images
                image_url = image.get("imageUrl") or image.get("url")
                review_link = image.get("link") or image.get("sourceUrl") or image.get("contextUrl")
                
                if image_url:
                    # Verify it's a valid image URL
                    if image_url.startswith(("http://", "https://")):
                        print(f"Found real dish image: {image_url[:80]}...")
                        if review_link:
                            print(f"Found review link: {review_link[:80]}...")
                        return image_url, review_link
        
        print("No relevant images found in Google Images search")
        return None, None
        
    except requests.exceptions.RequestException as e:
        print(f"Error searching for dish image: {e}")
        return None, None
    except Exception as e:
        print(f"Unexpected error searching images: {e}")
        return None, None
