import json
import requests
import time
import argparse

# Using Bloodhound-CE: curl -Ls https://ghst.ly/getbhce | docker compose -f - up
AUTH_URL = "http://localhost:8080/api/v2/login"
API_URL = "http://localhost:8080/api/v2/saved-queries"
DELAY = 1


def authenticate(auth_url, username, password):
    auth_payload = {
        "login_method": "secret",
        "username": username,
        "secret": password
    }
    headers = {
        "Content-Type": "application/json",
        "accept": "application/json"
    }
    response = requests.post(auth_url, json=auth_payload, headers=headers)
    if response.status_code == 200:
        session_token = response.json().get("data", {}).get("session_token")
        if session_token:
            print("Authentication successful.")
            return session_token
        else:
            raise ValueError("Failed to retrieve session token from response.")
    else:
        raise ValueError(f"Authentication failed. Status Code: {response.status_code}, Response: {response.text}")


def load_and_validate_json(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)
    valid_queries = [
        {"name": query.get("name"), "query": query.get("query")}
        for query in data
        if query.get("name") and query.get("query")
    ]
    if not valid_queries:
        raise ValueError("No valid queries found in the input file.")
    return valid_queries


def upload_queries(queries, api_url, token):
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    for query in queries:
        try:
            response = requests.post(api_url, json=query, headers=headers)
            if response.status_code in [200, 201]:
                print(f"Uploaded successfully: {query['name']}")
            else:
                print(f"Failed to upload: {query['name']}")
                print(f"Status Code: {response.status_code}, Response: {response.text}")
        except Exception as e:
            print(f"Error uploading {query['name']}: {e}")
        finally:
            time.sleep(DELAY)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload custom queries to BloodHound via API.")
    parser.add_argument("-f", "--file", required=True, help="Path to the JSON file containing queries.")
    parser.add_argument("-u", "--username", required=True, help="BloodHound username.")
    parser.add_argument("-p", "--password", required=True, help="BloodHound password.")
    args = parser.parse_args()

    try:
        token = authenticate(AUTH_URL, args.username, args.password)
        queries = load_and_validate_json(args.file)
        print(f"Loaded {len(queries)} valid queries from {args.file}.")
        upload_queries(queries, API_URL, token)
    except Exception as e:
        print(f"Error: {e}")
