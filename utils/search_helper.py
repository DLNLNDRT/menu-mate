"""
Serper.dev API helper for searching Google Reviews.
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
