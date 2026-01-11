import requests
import os
from dotenv import load_dotenv

# [cite_start]טעינת המפתחות מהקובץ הסודי שלך [cite: 1]
load_dotenv()

def test_edamam():
    app_id = os.getenv("EDAMAM_APP_ID")
    app_key = os.getenv("EDAMAM_APP_KEY")
    
    print(f"--- Starting API Test ---")
    print(f"Using ID: {app_id}")
    
    # הכתובת שאליה הקוד שלך מנסה לגשת
    url = "https://api.edamam.com/api/recipes/v2"
    params = {
        "type": "public",
        "q": "chicken",
        "app_id": app_id,
        "app_key": app_key
    }
    
    try:
        print("Sending request to Edamam...")
        response = requests.get(url, params=params)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            hits = data.get('hits', [])
            print(f"Success! Found {len(hits)} recipes.")
            if hits:
                print(f"First recipe found: {hits[0]['recipe']['label']}")
        elif response.status_code == 401:
            print("Error 401: Unauthorized. Check if your APP_ID and APP_KEY are correct.")
        elif response.status_code == 403:
            print("Error 403: Forbidden. You might have hit a limit or used wrong credentials.")
        else:
            print(f"Error {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"Network Connection Error: {e}")

if __name__ == "__main__":
    test_edamam()