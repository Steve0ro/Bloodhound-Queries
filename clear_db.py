#!/usr/bin/env python3
import json
import requests
import argparse

AUTH_URL = "http://localhost:8080/api/v2/login"
BLOODHOUND_URL = "http://localhost:8080/api/v2/clear-database"


def authenticate(auth_url, username, password):
    auth_payload = {"login_method": "secret", "username": username, "secret": password}
    headers = {"Content-Type": "application/json", "accept": "application/json"}
    response = requests.post(auth_url, json=auth_payload, headers=headers)
    if response.status_code == 200:
        session_token = response.json().get("data", {}).get("session_token")
        if session_token:
            print("Authentication successful.")
            return session_token
        else:
            raise ValueError("Failed to retrieve session token from response.")
    else:
        raise ValueError(
            f"Authentication failed. Status Code: {response.status_code}, Response: {response.text}"
        )


def delete_db(app_url, token):
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    body = {
        "deleteCollectedGraphData": True,
        "deleteFileIngestHistory": True,
        "deleteDataQualityHistory": True,
        "deleteAssetGroupSelectors": [],
    }

    try:
        response = requests.post(BLOODHOUND_URL, headers=headers, json=body)
        response.raise_for_status()
        print("[+] Request successful!")

        if response.text.strip():
            try:
                print(json.dumps(response.json(), indent=4))
            except json.JSONDecodeError:
                print("[!] Response is not JSON:")
                print(response.text)
        else:
            print("[*] Database cleared.")

    except requests.exceptions.RequestException as e:
        print(f"[!] Error: {e}")
        if "response" in locals() and response is not None:
            print(f"Response: {response.text}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clears Bloodhound Data")
    parser.add_argument("-u", "--username", required=True, help="BloodHound username.")
    parser.add_argument("-p", "--password", required=True, help="BloodHound password.")
    args = parser.parse_args()

    try:
        token = authenticate(AUTH_URL, args.username, args.password)
        delete_db(BLOODHOUND_URL, token)
    except Exception as e:
        print(f"Error: {e}")
