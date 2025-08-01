import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load the API key from environment variables
api_key = os.getenv("POSIT_CONNECT_API_KEY",None)
base_url = os.getenv("POSIT_CONNECT_URL",None)



#STATUS ENDPOINT
# Construct the full URL
url = f"{base_url}/status"
headers = {
    "accept": "application/json",
    "Authorization": f"Key {api_key}"
}
response = requests.get(url, headers=headers)
# If you want JSON data
if response.ok:
    data = response.json()
    print(data)
else:
    print(f"Error {response.status_code}: {response.text}")


# PREDICT ENDPOINT
url = f"{base_url}/predict"  # Adjust if upload endpoint is different
headers = {
    "Authorization": f"Key {api_key}",
    "accept": "application/json"
}
# Upload image
files = {
    "file": ("habitat.jpg", open("habitat.jpg", "rb"), "image/jpeg")
}
response = requests.post(url, headers=headers, files=files)
# Handle response
if response.ok:
    print(response.json())
else:
    print(f"Error {response.status_code}: {response.text}")
