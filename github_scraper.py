"""
GitHub User Search - Web Scraping Fallback
When API rate limits are hit, we can parse the GitHub search page directly
"""

import httpx
from bs4 import BeautifulSoup
import json
from typing import List, Dict
import re


def scrape_github_search(location: str, min_followers: int) -> List[Dict]:
    """
    Scrape GitHub's web search interface to find users.
    This is a fallback when API rate limits are exceeded.
    
    Parameters:
    - location: City name
    - min_followers: Minimum follower count
    
    Returns:
    - List of user dictionaries
    """
    
    # Construct the search URL
    query = f"location:{location} followers:>{min_followers}"
    search_url = f"https://github.com/search"
    
    params = {
        "q": query,
        "type": "users",
        "s": "joined",  # Sort by joined
        "o": "desc"     # Descending order
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }
    
    try:
        with httpx.Client(timeout=30.0, follow_redirects=True) as client:
            print(f"Fetching GitHub search page for: {query}")
            response = client.get(search_url, params=params, headers=headers)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Save HTML for debugging
            with open("github_search_page.html", "w", encoding="utf-8") as f:
                f.write(soup.prettify())
            print("✓ Saved HTML to github_search_page.html for inspection")
            
            users = []
            
            # Find user results
            # GitHub's search results are in divs with class "user-list-item"
            user_items = soup.find_all('div', class_='user-list-item')
            
            if not user_items:
                print("No user-list-item divs found. Trying alternative selectors...")
                # Try alternative selectors
                user_items = soup.select('[data-testid="results-list"] > div')
            
            print(f"Found {len(user_items)} user result containers")
            
            for idx, item in enumerate(user_items, 1):
                try:
                    # Extract username
                    username_link = item.find('a', {'data-hovercard-type': 'user'})
                    if not username_link:
                        username_link = item.find('a', class_='Link--primary')
                    
                    if username_link:
                        username = username_link.get_text().strip()
                        profile_url = f"https://github.com{username_link.get('href')}"
                        
                        # Extract follower count
                        followers_text = item.find(text=re.compile(r'followers?'))
                        followers = 0
                        if followers_text:
                            # Extract number before "followers"
                            match = re.search(r'([\d,]+)\s*followers?', followers_text.parent.get_text())
                            if match:
                                followers = int(match.group(1).replace(',', ''))
                        
                        # Extract location
                        location_elem = item.find('span', class_='Link--secondary')
                        location_text = location_elem.get_text().strip() if location_elem else ""
                        
                        user_info = {
                            "username": username,
                            "profile_url": profile_url,
                            "followers": followers,
                            "location": location_text,
                            "position": idx
                        }
                        
                        users.append(user_info)
                        print(f"  {idx}. {username} - {followers} followers - {location_text}")
                
                except Exception as e:
                    print(f"  Error parsing user {idx}: {e}")
                    continue
            
            return users
            
    except Exception as e:
        print(f"Error scraping GitHub: {e}")
        return []


def get_user_creation_date(username: str) -> str:
    """
    Scrape a user's profile page to get their join date.
    
    Parameters:
    - username: GitHub username
    
    Returns:
    - Creation date string
    """
    
    profile_url = f"https://github.com/{username}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.get(profile_url, headers=headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Look for the join date
            # It's typically in a relative-time element with datetime attribute
            time_elem = soup.find('relative-time')
            if time_elem and time_elem.has_attr('datetime'):
                return time_elem['datetime']
            
            # Alternative: look for text like "Joined on"
            join_text = soup.find(text=re.compile(r'Joined'))
            if join_text:
                # Find nearby time element
                parent = join_text.parent
                time_elem = parent.find_next('relative-time')
                if time_elem and time_elem.has_attr('datetime'):
                    return time_elem['datetime']
            
            return None
            
    except Exception as e:
        print(f"Error fetching profile for {username}: {e}")
        return None


def main():
    """
    Main function using web scraping approach.
    """
    print("\n" + "="*80)
    print("GitHub User Search - Web Scraping Method")
    print("="*80)
    print("\nThis method scrapes GitHub's web interface when API limits are exceeded.\n")
    
    # Search for users
    users = scrape_github_search("Hyderabad", 190)
    
    if not users:
        print("\n❌ No users found")
        return
    
    print(f"\n✓ Found {len(users)} users")
    
    # The first user is the newest (already sorted by joined date desc)
    if users:
        newest_user = users[0]
        username = newest_user['username']
        
        print(f"\n{'='*80}")
        print(f"NEWEST USER: {username}")
        print(f"{'='*80}")
        print(f"Profile: {newest_user['profile_url']}")
        print(f"Followers: {newest_user['followers']}")
        print(f"Location: {newest_user['location']}")
        
        # Try to get creation date from profile
        print(f"\nFetching join date from profile page...")
        created_at = get_user_creation_date(username)
        
        if created_at:
            print(f"\n🎯 ANSWER: {created_at}")
            print(f"{'='*80}\n")
            
            # Save results
            output = {
                "newest_user": {
                    "username": username,
                    "created_at": created_at,
                    "profile_url": newest_user['profile_url'],
                    "followers": newest_user['followers'],
                    "location": newest_user['location']
                },
                "all_users_found": users
            }
            
            with open("hyderabad_users_scraped.json", "w", encoding="utf-8") as f:
                json.dump(output, f, indent=2)
            
            print("✓ Saved to hyderabad_users_scraped.json\n")
        else:
            print("\n⚠️  Could not extract creation date from profile")


if __name__ == "__main__":
    main()
