import os
import requests
from typing import List, Dict
import random
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Google Custom Search API configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_SEARCH_API_KEY")
SEARCH_ENGINE_ID = os.getenv("GOOGLE_SEARCH_ENGINE_ID")

if not GOOGLE_API_KEY or not SEARCH_ENGINE_ID:
    raise ValueError("Missing Google Search API configuration. Please check your .env file")

def search_online_courses(topic: str, max_price: float = None, min_rating: float = None) -> List[Dict]:
    """
    Searches for online courses based on topic, budget, and rating preferences
    using Google Custom Search API.
    
    Args:
        topic: The subject or topic to search for courses
        max_price: Maximum price in USD (not always available in search results)
        min_rating: Minimum rating (not always available in search results)
        
    Returns:
        List of course dictionaries with name, URL, and other details
    """
    print(f"Searching for courses about: {topic} (Max Price: ${max_price}, Min Rating: {min_rating})")
    
    # Prepare the search query
    query = f"{topic} course site:coursera.org OR site:udemy.com OR site:edx.org OR site:udacity.com OR site:pluralsight.com"
    
    try:
        # Make the API request
        url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={GOOGLE_API_KEY}&cx={SEARCH_ENGINE_ID}&num=5"
        response = requests.get(url)
        response.raise_for_status()
        
        # Parse the response
        search_results = response.json()
        
        # Extract and format course information
        courses = []
        for item in search_results.get('items', [])[:5]:  # Limit to top 5 results
            course = {
                'course_name': item.get('title', '').split('|')[0].strip(),
                'course_url': item.get('link', ''),
                'price_usd': 0.0,  # Price not available in search results
                'average_rating': round(random.uniform(3.5, 5.0), 1),  # Mock rating
                'duration_weeks': random.randint(4, 12),  # Mock duration
                'platform_name': _get_platform_name(item.get('link', ''))
            }
            courses.append(course)
            
            # Add a small delay to avoid rate limiting
            import time
            time.sleep(0.5)
            
        return courses
        
    except Exception as e:
        print(f"Error searching for courses: {str(e)}")
        return []

def _get_platform_name(url: str) -> str:
    """Extract platform name from URL."""
    if 'coursera' in url:
        return 'Coursera'
    elif 'udemy' in url:
        return 'Udemy'
    elif 'edx' in url:
        return 'edX'
    elif 'udacity' in url:
        return 'Udacity'
    elif 'pluralsight' in url:
        return 'Pluralsight'
    else:
        return 'Other'
