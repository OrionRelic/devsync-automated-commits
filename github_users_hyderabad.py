"""
GitHub User Search for CodeConnect
Finds users in Hyderabad with over 190 followers and identifies the newest user
"""

import httpx
import json
from typing import List, Dict, Optional
from datetime import datetime
import os


def search_github_users(
    location: str,
    min_followers: int,
    github_token: Optional[str] = None
) -> List[Dict]:
    """
    Search GitHub users by location and minimum follower count.
    
    Parameters:
    - location: City or location to search for
    - min_followers: Minimum number of followers
    - github_token: Optional GitHub personal access token for higher rate limits
    
    Returns:
    - List of user dictionaries with relevant information
    """
    
    # GitHub API endpoint for user search
    base_url = "https://api.github.com/search/users"
    
    # Construct search query
    # Format: location:Hyderabad followers:>190
    query = f"location:{location} followers:>{min_followers}"
    
    # Parameters for the API request
    params = {
        "q": query,
        "sort": "joined",  # Sort by join date
        "order": "desc",   # Descending order (newest first)
        "per_page": 100    # Maximum results per page
    }
    
    # Headers
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "CodeConnect-Recruitment/1.0"
    }
    
    # Add authentication token if provided
    if github_token:
        headers["Authorization"] = f"token {github_token}"
    
    all_users = []
    
    try:
        with httpx.Client(timeout=30.0) as client:
            # Make initial request
            response = client.get(base_url, params=params, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            
            total_count = data.get('total_count', 0)
            items = data.get('items', [])
            
            print(f"Found {total_count} users in {location} with over {min_followers} followers")
            print(f"Retrieved {len(items)} users in this request")
            
            # Check rate limit
            rate_limit_remaining = response.headers.get('X-RateLimit-Remaining', 'unknown')
            print(f"API Rate Limit Remaining: {rate_limit_remaining}\n")
            
            # Since the search API already sorts by 'joined' in descending order,
            # the first user is the newest. We can extract basic info from search results.
            print("Processing user data (using search results to avoid additional API calls)...\n")
            
            # For each user, we'll use the data from the search endpoint
            # and only fetch detailed info if absolutely necessary
            for idx, user in enumerate(items):
                # The search endpoint provides basic info
                # We need to make individual calls to get created_at
                user_login = user.get('login')
                user_url = user.get('url')
                
                print(f"  Fetching details for user {idx+1}/{len(items)}: {user_login}")
                
                # Check if we're running low on rate limit
                if rate_limit_remaining != 'unknown' and int(rate_limit_remaining) < 5:
                    print(f"\n⚠️  Approaching rate limit. Retrieved {len(all_users)} users so far.")
                    print(f"   To get all users, please set a GITHUB_TOKEN environment variable.")
                    break
                
                # Fetch detailed user information
                try:
                    user_response = client.get(user_url, headers=headers)
                    user_response.raise_for_status()
                    user_details = user_response.json()
                    
                    # Update rate limit counter
                    rate_limit_remaining = user_response.headers.get('X-RateLimit-Remaining', rate_limit_remaining)
                    
                    # Extract relevant information
                    user_info = {
                        "login": user_details.get('login'),
                        "name": user_details.get('name'),
                        "location": user_details.get('location'),
                        "followers": user_details.get('followers'),
                        "public_repos": user_details.get('public_repos'),
                        "created_at": user_details.get('created_at'),
                        "html_url": user_details.get('html_url'),
                        "bio": user_details.get('bio'),
                        "company": user_details.get('company')
                    }
                    
                    all_users.append(user_info)
                    
                except httpx.HTTPStatusError as e:
                    if e.response.status_code == 403:
                        print(f"\n⚠️  Rate limit exceeded after fetching {len(all_users)} users.")
                        print(f"   Please set a GITHUB_TOKEN environment variable for higher limits.")
                        break
                    else:
                        print(f"   Error fetching {user_login}: {e}")
                        continue
            
            print(f"\nSuccessfully retrieved details for {len(all_users)} users.")
            return all_users
            
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 403:
            print("⚠️  Rate limit exceeded on initial search.")
            print("   Please set a GITHUB_TOKEN environment variable.")
        raise Exception(f"HTTP error occurred: {e}")
    except httpx.RequestError as e:
        raise Exception(f"Request error occurred: {e}")
    except Exception as e:
        raise Exception(f"Error: {e}")


def find_newest_user(users: List[Dict]) -> Dict:
    """
    Find the newest user (most recent created_at date) from the list.
    
    Parameters:
    - users: List of user dictionaries
    
    Returns:
    - Dictionary containing the newest user's information
    """
    if not users:
        raise ValueError("No users provided")
    
    # Sort users by created_at date (most recent first)
    sorted_users = sorted(
        users,
        key=lambda x: datetime.fromisoformat(x['created_at'].replace('Z', '+00:00')),
        reverse=True
    )
    
    return sorted_users[0]


def print_user_summary(users: List[Dict]):
    """
    Print a summary of all users found.
    """
    print("=" * 80)
    print(f"GitHub Users in Hyderabad with over 190 followers")
    print("=" * 80)
    print(f"\nTotal Users Found: {len(users)}\n")
    
    for idx, user in enumerate(users, 1):
        print(f"{idx}. {user['login']} (@{user['login']})")
        print(f"   Name: {user['name'] or 'N/A'}")
        print(f"   Followers: {user['followers']}")
        print(f"   Public Repos: {user['public_repos']}")
        print(f"   Created: {user['created_at']}")
        print(f"   Profile: {user['html_url']}")
        if user.get('company'):
            print(f"   Company: {user['company']}")
        print()


def print_newest_user_info(user: Dict):
    """
    Print detailed information about the newest user.
    """
    print("=" * 80)
    print("NEWEST USER (Most Recently Joined GitHub)")
    print("=" * 80)
    print(f"\nUsername: {user['login']}")
    print(f"Name: {user['name'] or 'N/A'}")
    print(f"Location: {user['location']}")
    print(f"Followers: {user['followers']}")
    print(f"Public Repositories: {user['public_repos']}")
    print(f"Profile URL: {user['html_url']}")
    if user.get('company'):
        print(f"Company: {user['company']}")
    if user.get('bio'):
        print(f"Bio: {user['bio']}")
    print(f"\n🎯 ACCOUNT CREATED: {user['created_at']}")
    print("=" * 80)


def main():
    """
    Main function to search for GitHub users and find the newest one.
    """
    print("\nCodeConnect - GitHub User Search")
    print("Finding users in Hyderabad with over 190 followers...\n")
    
    # Check for GitHub token in environment
    github_token = os.environ.get('GITHUB_TOKEN')
    
    if not github_token:
        print("⚠️  No GitHub token found. Rate limits may apply.")
        print("   Set GITHUB_TOKEN environment variable for higher limits.\n")
    
    try:
        # Search for users
        users = search_github_users(
            location="Hyderabad",
            min_followers=190,
            github_token=github_token
        )
        
        if not users:
            print("❌ No users found matching the criteria.")
            return
        
        # Print summary of all users
        print_user_summary(users)
        
        # Find the newest user
        newest_user = find_newest_user(users)
        
        # Print newest user information
        print_newest_user_info(newest_user)
        
        # Extract the creation date
        created_at = newest_user['created_at']
        
        print(f"\n✅ ANSWER: The newest user joined GitHub on: {created_at}\n")
        
        # Save results to JSON
        results = {
            "search_criteria": {
                "location": "Hyderabad",
                "min_followers": 190
            },
            "total_users_found": len(users),
            "newest_user": newest_user,
            "all_users": users
        }
        
        with open("hyderabad_github_users.json", "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print("✓ Data saved to hyderabad_github_users.json")
        
        return created_at
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


if __name__ == "__main__":
    main()
