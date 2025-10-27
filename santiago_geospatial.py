"""
Geospatial Data Extraction for UrbanRide
Fetches bounding box data for Santiago, Chile using Nominatim API
"""

import httpx
import json
from typing import Optional, Dict, List
import time


def fetch_city_boundingbox(
    city: str,
    country: str,
    osm_id_ending: Optional[str] = None,
    user_agent: str = "UrbanRide-Geospatial/1.0"
) -> Dict:
    """
    Fetch bounding box data for a city using Nominatim API.
    
    Parameters:
    - city: Name of the city
    - country: Name of the country
    - osm_id_ending: Optional ending pattern for osm_id to filter results
    - user_agent: User agent string for API requests (required by Nominatim)
    
    Returns:
    - Dictionary containing bounding box information and coordinates
    """
    
    # Nominatim API endpoint
    base_url = "https://nominatim.openstreetmap.org/search"
    
    # Parameters for the API request
    params = {
        "city": city,
        "country": country,
        "format": "json",
        "limit": 10,  # Get multiple results to handle duplicates
        "addressdetails": 1
    }
    
    # Headers with User-Agent (required by Nominatim)
    headers = {
        "User-Agent": user_agent
    }
    
    try:
        # Make GET request to Nominatim API
        with httpx.Client(timeout=30.0) as client:
            # Respect Nominatim's rate limiting (1 request per second)
            time.sleep(1)
            
            response = client.get(base_url, params=params, headers=headers)
            response.raise_for_status()
            
            results = response.json()
            
            if not results:
                raise ValueError(f"No results found for {city}, {country}")
            
            # Filter results based on osm_id ending if provided
            if osm_id_ending:
                filtered_results = [
                    result for result in results 
                    if str(result.get('osm_id', '')).endswith(osm_id_ending)
                ]
                
                if filtered_results:
                    results = filtered_results
                else:
                    print(f"Warning: No results matching osm_id ending '{osm_id_ending}'. Using first result.")
            
            # Select the first (most relevant) result
            selected_result = results[0]
            
            # Extract bounding box
            # Format: [min_lat, max_lat, min_lon, max_lon]
            boundingbox = selected_result.get('boundingbox', [])
            
            if not boundingbox or len(boundingbox) != 4:
                raise ValueError("Invalid bounding box data received")
            
            # Parse bounding box values
            min_latitude = float(boundingbox[0])
            max_latitude = float(boundingbox[1])
            min_longitude = float(boundingbox[2])
            max_longitude = float(boundingbox[3])
            
            # Prepare result dictionary
            result_data = {
                "city": city,
                "country": country,
                "osm_id": selected_result.get('osm_id'),
                "osm_type": selected_result.get('osm_type'),
                "display_name": selected_result.get('display_name'),
                "boundingbox": {
                    "min_latitude": min_latitude,
                    "max_latitude": max_latitude,
                    "min_longitude": min_longitude,
                    "max_longitude": max_longitude
                },
                "center": {
                    "latitude": float(selected_result.get('lat', 0)),
                    "longitude": float(selected_result.get('lon', 0))
                },
                "raw_boundingbox": boundingbox
            }
            
            return result_data
            
    except httpx.HTTPStatusError as e:
        raise Exception(f"HTTP error occurred: {e}")
    except httpx.RequestError as e:
        raise Exception(f"Request error occurred: {e}")
    except (ValueError, KeyError, IndexError) as e:
        raise Exception(f"Error parsing API response: {e}")


def print_geospatial_info(data: Dict):
    """
    Pretty print geospatial information.
    """
    print("=" * 70)
    print(f"Geospatial Data for {data['city']}, {data['country']}")
    print("=" * 70)
    print(f"\nDisplay Name: {data['display_name']}")
    print(f"OSM ID: {data['osm_id']}")
    print(f"OSM Type: {data['osm_type']}")
    print(f"\nCenter Coordinates:")
    print(f"  Latitude:  {data['center']['latitude']}")
    print(f"  Longitude: {data['center']['longitude']}")
    print(f"\nBounding Box:")
    print(f"  Minimum Latitude:  {data['boundingbox']['min_latitude']}")
    print(f"  Maximum Latitude:  {data['boundingbox']['max_latitude']}")
    print(f"  Minimum Longitude: {data['boundingbox']['min_longitude']}")
    print(f"  Maximum Longitude: {data['boundingbox']['max_longitude']}")
    print("\n" + "=" * 70)


def main():
    """
    Main function to fetch Santiago, Chile bounding box data.
    """
    print("\nUrbanRide Geospatial Data Optimization")
    print("Fetching bounding box data for Santiago, Chile...\n")
    
    try:
        # Fetch data for Jeddah, Saudi Arabia
        result = fetch_city_boundingbox(
            city="Jeddah",
            country="Chile",
            user_agent="UrbanRide-Geospatial/1.0 (contact@urbanride.com)"
        )
        
        # Print detailed information
        print_geospatial_info(result)
        
        # Highlight the answer to the specific question
        min_latitude = result['boundingbox']['min_latitude']
        print(f"\n🎯 ANSWER: The minimum latitude of the bounding box for Santiago, Chile is:")
        print(f"   {min_latitude}")
        print()
        
        # Save to JSON file for reference
        with open("santiago_chile_geospatial.json", "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print("✓ Data saved to santiago_chile_geospatial.json")
        
        return min_latitude
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


if __name__ == "__main__":
    main()
