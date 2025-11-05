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
                                "url": image_url,  # Can be regular URL or data URL
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
    Use GPT-4o to analyze reviews and provide three recommendations:
    1. Best reviewed option
    2. Worst reviewed option (to avoid)
    3. Best option if on a diet (with ingredient details)
    
    Args:
        reviews_data: Text containing Google reviews snippets
        menu_items: List of menu items found in the menu
        restaurant_name: Name of the restaurant
        
    Returns:
        Dictionary with best_reviewed, worst_reviewed, diet_option, and explanations
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
                    and provide three recommendations based on reviews. Be concise but informative."""
                },
                {
                    "role": "user",
                    "content": f"""Restaurant: {restaurant_name}
                    
Available menu items: {menu_items_str}

Google Reviews:
{reviews_data}

CRITICAL: ALL recommendations MUST be from the menu items listed above. DO NOT suggest dishes that are not in the "Available menu items" list.

Based on these reviews and the menu items, provide THREE recommendations:

1. BEST REVIEWED OPTION: The dish from the menu items that received the most positive reviews
   - MUST be one of the menu items listed above
   - Include: dish name (must match menu item exactly), brief explanation (2-3 sentences), key positive review highlights
   - If no menu items match positive reviews, choose the best-reviewed menu item anyway

2. WORST REVIEWED OPTION: The dish from the menu items that received negative reviews or complaints (to help users avoid bad choices)
   - MUST be one of the menu items listed above
   - Include: dish name (must match menu item exactly), brief explanation (2-3 sentences), what reviewers complained about
   - If no menu items have negative reviews, choose the least-reviewed menu item

3. BEST DIET OPTION: The healthiest option from the menu items suitable for someone on a diet, with ingredient details
   - MUST be one of the menu items listed above
   - Include: dish name (must match menu item exactly), brief explanation (2-3 sentences), list of main ingredients and why it's diet-friendly

Return your response in this JSON format:
{{
    "best_reviewed": {{
        "dish": "dish name",
        "explanation": "brief explanation",
        "highlights": "key positive mentions"
    }},
    "worst_reviewed": {{
        "dish": "dish name",
        "explanation": "brief explanation",
        "complaints": "what reviewers complained about"
    }},
    "diet_option": {{
        "dish": "dish name",
        "explanation": "brief explanation",
        "ingredients": "list of main ingredients and why it's diet-friendly"
    }}
}}"""
                }
            ],
            response_format={"type": "json_object"},
            max_tokens=800
        )
        
        import json
        recommendation = json.loads(response.choices[0].message.content)
        return recommendation
        
    except Exception as e:
        return {
            "best_reviewed": {
                "dish": menu_items[0] if menu_items else "Ask the waiter for recommendations",
                "explanation": "Unable to analyze reviews at this time.",
                "highlights": str(e)
            },
            "worst_reviewed": {
                "dish": "Not available",
                "explanation": "Unable to analyze reviews.",
                "complaints": ""
            },
            "diet_option": {
                "dish": "Not available",
                "explanation": "Unable to analyze reviews.",
                "ingredients": ""
            }
        }


async def generate_dish_image(restaurant_name: str, dish_name: str, cuisine_type: str = "unknown") -> Optional[str]:
    """
    Generate a photorealistic image of the recommended dish using DALL-E 3.
    
    Args:
        restaurant_name: Name of the restaurant (can be generic if unknown)
        dish_name: Name of the dish
        cuisine_type: Type of cuisine
        
    Returns:
        URL of the generated image, or None if generation fails
    """
    try:
        # Create a prompt for realistic user-uploaded review photos (like Google Reviews/Yelp)
        # Style: casual phone camera, natural lighting, authentic restaurant setting
        if cuisine_type != "unknown":
            prompt = f"Realistic smartphone photo of {dish_name}, a {cuisine_type} dish, taken by a customer at a restaurant. Casual phone camera shot, natural restaurant lighting, authentic plating as served, seen from customer's perspective, looks like a real user-uploaded review photo on Google Reviews or Yelp, slightly informal composition, typical restaurant table setting in background."
        else:
            prompt = f"Realistic smartphone photo of {dish_name} taken by a customer at a restaurant. Casual phone camera shot, natural restaurant lighting, authentic plating as served, seen from customer's perspective, looks like a real user-uploaded review photo on Google Reviews or Yelp, slightly informal composition, typical restaurant table setting in background."
        
        print(f"Generating DALL-E 3 image with prompt: {prompt[:100]}...")
        
        response = await asyncio.to_thread(
            client.images.generate,
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1
        )
        
        image_url = response.data[0].url
        print(f"DALL-E 3 image generated successfully: {image_url}")
        return image_url
        
    except Exception as e:
        print(f"Error generating DALL-E 3 image: {e}")
        return None
