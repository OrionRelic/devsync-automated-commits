"""
GitHub User Search - Optimized Version
Finds the newest user in Hyderabad with over 190 followers
Optimized to minimize API calls
"""

import httpx
import json
from typing import Optional, Dict
import os


def get_newest_user_hyderabad(
    location: str = "Hyderabad",
    min_followers: int = 190,
    github_token: Optional[str] = None
) -> Dict:
    """
    Get the newest GitHub user in a location with minimum followers.
    
    Since the search API allows sorting by 'joined' in descending order,
    we only need to fetch the first result to get the newest user.
    
    Parameters:
    - location: City or location to search for
    - min_followers: Minimum number of followers
    - github_token: Optional GitHub personal access token
    
    Returns:
    - Dictionary with the newest user's information
    """
    
    # GitHub API endpoint
    search_url = "https://api.github.com/search/users"
    
    # Construct search query
    query = f"location:{location} followers:>{min_followers}"
    
    # Parameters - get only 1 result since we want the newest
    params = {
        "q": query,
        "sort": "joined",
        "order": "desc",
        "per_page": 1  # Only get the first (newest) result
    }
    
    # Headers
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "CodeConnect-Recruitment/1.0"
    }
    
    if github_token:
        headers["Authorization"] = f"token {github_token}"
    
    try:
        with httpx.Client(timeout=30.0) as client:
            # Search for users
            print(f"Searching for users in {location} with over {min_followers} followers...")
            response = client.get(search_url, params=params, headers=headers)
            response.raise_for_status()
            
            search_data = response.json()
            total_count = search_data.get('total_count', 0)
            items = search_data.get('items', [])
            
            print(f"Total users found: {total_count}")
            
            if not items:
                raise ValueError("No users found matching the criteria")
            
            # Get the first user (newest)
            user_basic = items[0]
            user_login = user_basic.get('login')
            
            print(f"Newest user: {user_login}")
            print(f"Fetching detailed information...")
            
            # Get detailed user information
            user_url = user_basic.get('url')
            user_response = client.get(user_url, headers=headers)
            user_response.raise_for_status()
            
            user_details = user_response.json()
            
            # Extract information
            user_info = {
                "login": user_details.get('login'),
                "name": user_details.get('name'),
                "location": user_details.get('location'),
                "followers": user_details.get('followers'),
                "public_repos": user_details.get('public_repos'),
                "created_at": user_details.get('created_at'),
                "html_url": user_details.get('html_url'),
                "bio": user_details.get('bio'),
                "company": user_details.get('company'),
                "blog": user_details.get('blog'),
                "twitter_username": user_details.get('twitter_username')
            }
            
            return user_info
            
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 403:
            print("\n⚠️  Rate limit exceeded.")
            print("   To increase rate limits, set a GITHUB_TOKEN environment variable:")
            print("   1. Create a token at: https://github.com/settings/tokens")
            print("   2. Set environment variable: $env:GITHUB_TOKEN='your_token_here'")
        raise Exception(f"HTTP error: {e}")
    except Exception as e:
        raise Exception(f"Error: {e}")


def print_user_details(user: Dict):
    """
    Print formatted user details.
    """
    print("\n" + "=" * 80)
    print("NEWEST GITHUB USER IN HYDERABAD WITH OVER 190 FOLLOWERS")
    print("=" * 80)
    print(f"\nUsername:       {user['login']}")
    print(f"Name:           {user['name'] or 'N/A'}")
    print(f"Location:       {user['location']}")
    print(f"Followers:      {user['followers']}")
    print(f"Public Repos:   {user['public_repos']}")
    print(f"Profile URL:    {user['html_url']}")
    
    if user.get('company'):
        print(f"Company:        {user['company']}")
    
    if user.get('blog'):
        print(f"Blog/Website:   {user['blog']}")
    
    if user.get('twitter_username'):
        print(f"Twitter:        @{user['twitter_username']}")
    
    if user.get('bio'):
        print(f"\nBio:            {user['bio']}")
    
    print(f"\n{'='*80}")
    print(f"🎯 ACCOUNT CREATED: {user['created_at']}")
    print("=" * 80)


def main():
    """
    Main function.
    """
    print("\n" + "="*80)
    print("CodeConnect - GitHub User Search (Optimized)")
    print("="*80)
    print()
    
    # Check for GitHub token
    github_token = os.environ.get('GITHUB_TOKEN')
    
    if github_token:
        print("✓ GitHub token found - using authenticated requests")
    else:
        print("⚠️  No GitHub token found - using unauthenticated requests (limited)")
        print("   Set GITHUB_TOKEN for higher rate limits\n")
    
    try:
        # Get the newest user
        newest_user = get_newest_user_hyderabad(
            location="Hyderabad",
            min_followers=190,
            github_token=github_token
        )
        
        # Print details
        print_user_details(newest_user)
        
        # Extract the creation date
        created_at = newest_user['created_at']
        
        print(f"\n✅ ANSWER: {created_at}\n")
        
        # Save to JSON
        output = {
            "search_criteria": {
                "location": "Hyderabad",
                "min_followers": 190,
                "sorted_by": "joined date (newest first)"
            },
            "newest_user": newest_user,
            "answer": created_at
        }
        
        with open("hyderabad_newest_user.json", "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        print("✓ Data saved to hyderabad_newest_user.json\n")
        
        return created_at
        
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        return None


if __name__ == "__main__":
    main()
