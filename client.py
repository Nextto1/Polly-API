import requests
import json
from typing import List, Dict, Any, Optional

def register_user(username: str, password: str, base_url: str = "http://localhost:8000") -> dict:
    """
    Register a new user via the /register endpoint.
    
    Args:
        username: The username for the new user
        password: The password for the new user
        base_url: The base URL of the API (default: http://localhost:8000)
        
    Returns:
        dict: The response from the API containing the user information
        
    Raises:
        requests.exceptions.RequestException: If the request fails
        ValueError: If the username is already registered or other validation errors
    """
    # Prepare the request URL and headers
    url = f"{base_url}/register"
    headers = {"Content-Type": "application/json"}
    
    # Prepare the request payload according to UserCreate schema
    payload = {
        "username": username,
        "password": password
    }
    
    # Send the POST request to the /register endpoint
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    
    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 400:
        raise ValueError("Username already registered")
    else:
        # Raise an exception for other errors
        response.raise_for_status()
        
    return response.json()


def get_polls(skip: int = 0, limit: int = 10, base_url: str = "http://localhost:8000") -> List[Dict[str, Any]]:
    """
    Fetch paginated poll data from the /polls endpoint.
    
    Args:
        skip: Number of items to skip (default: 0)
        limit: Maximum number of items to return (default: 10)
        base_url: The base URL of the API (default: http://localhost:8000)
        
    Returns:
        List[Dict[str, Any]]: A list of poll objects with their details
        
    Raises:
        requests.exceptions.RequestException: If the request fails
    """
    # Prepare the request URL with query parameters for pagination
    url = f"{base_url}/polls"
    params = {
        "skip": skip,
        "limit": limit
    }
    
    # Send the GET request to the /polls endpoint
    response = requests.get(url, params=params)
    
    # Check if the request was successful
    response.raise_for_status()
    
    # Return the list of polls
    return response.json()


def vote_on_poll(poll_id: int, option_id: int, access_token: str, base_url: str = "http://localhost:8000") -> Dict[str, Any]:
    """
    Cast a vote on an existing poll.
    
    Args:
        poll_id: The ID of the poll to vote on
        option_id: The ID of the option to vote for
        access_token: JWT access token for authentication
        base_url: The base URL of the API (default: http://localhost:8000)
        
    Returns:
        Dict[str, Any]: The vote information from the API
        
    Raises:
        requests.exceptions.RequestException: If the request fails
        ValueError: If unauthorized or poll/option not found
    """
    # Prepare the request URL and headers
    url = f"{base_url}/polls/{poll_id}/vote"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    
    # Prepare the request payload according to VoteCreate schema
    payload = {
        "option_id": option_id
    }
    
    # Send the POST request to the vote endpoint
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    
    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 401:
        raise ValueError("Unauthorized - invalid or missing access token")
    elif response.status_code == 404:
        raise ValueError("Poll or option not found")
    else:
        response.raise_for_status()
        
    return response.json()


def get_poll_results(poll_id: int, base_url: str = "http://localhost:8000") -> Dict[str, Any]:
    """
    Retrieve poll results for a specific poll.
    
    Args:
        poll_id: The ID of the poll to get results for
        base_url: The base URL of the API (default: http://localhost:8000)
        
    Returns:
        Dict[str, Any]: Poll results with vote counts for each option
        
    Raises:
        requests.exceptions.RequestException: If the request fails
        ValueError: If poll not found
    """
    # Prepare the request URL
    url = f"{base_url}/polls/{poll_id}/results"
    
    # Send the GET request to the results endpoint
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        raise ValueError("Poll not found")
    else:
        response.raise_for_status()
        
    return response.json()


# Example usage
if __name__ == "__main__":
    try:
        # Example 1: Register a new user
        # result = register_user("new_user", "password123")
        # print(f"User registered successfully: {result}")
        
        # Example 2: Get paginated polls
        polls = get_polls(skip=0, limit=5)
        print(f"Retrieved {len(polls)} polls:")
        for poll in polls:
            print(f"  - {poll['question']} (ID: {poll['id']})")
        
        # Example 3: Vote on a poll (requires authentication)
        # access_token = "your_jwt_token_here"
        # vote_result = vote_on_poll(poll_id=1, option_id=1, access_token=access_token)
        # print(f"Vote cast successfully: {vote_result}")
        
        # Example 4: Get poll results
        # results = get_poll_results(poll_id=1)
        # print(f"Poll results: {results['question']}")
        # for result in results['results']:
        #     print(f"  - {result['text']}: {result['vote_count']} votes")
        
    except ValueError as e:
        print(f"Error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
    except ValueError as e:
        print(f"Registration error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")