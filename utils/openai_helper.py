"""
OpenAI helper functions for image analysis and image generation.
"""
import os
import asyncio
from openai import OpenAI
from typing import Dict, Optional

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


async def analyze_menu_image(image_url: str, user_question: str = "What should I order?") -> Dict:
    """
    Analyze a menu/restaurant image using GPT-4o vision model.
    
    Args:
        image_url: URL of the image to analyze
        user_question: User's question about the menu
        
    Returns:
        Dictionary containing restaurant name, menu items, language, and other context
    """
    try:
        # Run blocking OpenAI calls in thread pool
        response = await asyncio.to_thread(
            client.chat.completions.create,
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": """You are an expert at analyzing restaurant menus and restaurant photos. 
                    Extract the following information:
                    1. Restaurant name (if visible)
                    2. All menu items listed (dish names, descriptions)
                    3. Language of the menu (if non-English, also translate dish names to English)
                    4. Cuisine type
                    5. Any notable characteristics about the restaurant or menu
                    
                    Return a structured analysis of the menu."""
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": user_question + "\n\nPlease analyze this menu/restaurant image and extract all relevant information."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_url,
                                "detail": "high"
                            }
                        }
                    ]
                }
            ],
            max_tokens=1000
        )
        
        analysis_text = response.choices[0].message.content
        
        # Parse the analysis to extract structured data
        # Use GPT to extract structured JSON
        structure_response = await asyncio.to_thread(
            client.chat.completions.create,
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are a JSON parser. Extract structured information from the menu analysis."
                },
                {
                    "role": "user",
                    "content": f"""From this analysis, extract JSON with the following structure:
                    {{
                        "restaurant_name": "name or null if not found",
                        "menu_items": ["item1", "item2", ...],
                        "cuisine_type": "type",
                        "language": "language",
                        "analysis": "full analysis text"
                    }}
                    
                    Analysis: {analysis_text}"""
                }
            ],
            response_format={"type": "json_object"}
        )
        
        import json
        structured_data = json.loads(structure_response.choices[0].message.content)
        structured_data["raw_analysis"] = analysis_text
        
        return structured_data
        
    except Exception as e:
        return {
            "error": str(e),
            "restaurant_name": None,
            "menu_items": [],
            "cuisine_type": "unknown",
            "language": "unknown",
            "analysis": ""
        }


async def summarize_reviews_and_recommend(reviews_data: str, menu_items: list, restaurant_name: str) -> Dict:
    """
    Use GPT-4o to summarize reviews and recommend the best dish.
    
    Args:
        reviews_data: Text containing Google reviews snippets
        menu_items: List of menu items found in the menu
        restaurant_name: Name of the restaurant
        
    Returns:
        Dictionary with best_dish, reasoning, and review_highlights
    """
    try:
        menu_items_str = ", ".join(menu_items) if menu_items else "Not specified"
        
        response = await asyncio.to_thread(
            client.chat.completions.create,
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": """You are a food critic and restaurant advisor. Analyze Google reviews 
                    and recommend the best dish from the menu. Be concise but informative."""
                },
                {
                    "role": "user",
                    "content": f"""Restaurant: {restaurant_name}
                    
Available menu items: {menu_items_str}

Google Reviews:
{reviews_data}

Based on these reviews and the menu items, recommend:
1. The BEST dish to order (must be from the menu items if available)
2. A brief, engaging explanation (2-3 sentences max)
3. Key review highlights that support your recommendation

Return your response in this JSON format:
{{
    "best_dish": "dish name",
    "reasoning": "brief explanation",
    "review_highlights": "key positive mentions from reviews"
}}"""
                }
            ],
            response_format={"type": "json_object"},
            max_tokens=500
        )
        
        import json
        recommendation = json.loads(response.choices[0].message.content)
        return recommendation
        
    except Exception as e:
        return {
            "best_dish": menu_items[0] if menu_items else "Ask the waiter for recommendations",
            "reasoning": "Unable to analyze reviews at this time.",
            "review_highlights": str(e)
        }


async def generate_dish_image(restaurant_name: str, dish_name: str, cuisine_type: str = "unknown") -> Optional[str]:
    """
    Generate a photorealistic image of the recommended dish using OpenAI DALL-E.
    
    Args:
        restaurant_name: Name of the restaurant
        dish_name: Name of the dish
        cuisine_type: Type of cuisine
        
    Returns:
        URL of the generated image, or None if generation fails
    """
    try:
        prompt = f"Photorealistic high-quality food photography of {dish_name} from {restaurant_name}, a {cuisine_type} restaurant. Professional restaurant lighting, appetizing presentation, shot on white plate, shallow depth of field."
        
        response = await asyncio.to_thread(
            client.images.generate,
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1
        )
        
        image_url = response.data[0].url
        return image_url
        
    except Exception as e:
        print(f"Error generating image: {e}")
        return None
