import requests
import os
from dotenv import load_dotenv

# טעינת המפתחות מקובץ .env 
load_dotenv()

def test_edamam():
    # שליפת המפתחות מהסביבה 
    app_id = os.getenv("EDAMAM_APP_ID")
    app_key = os.getenv("EDAMAM_APP_KEY")
    
    print("--- בדיקה סופית: API v2 ---")
    print(f"ID:  {repr(app_id)}")
    print(f"KEY: {repr(app_key)}")
    print("--------------------------")
    
    # הכתובת הרשמית והמעודכנת לחיפוש מתכונים
    url = "https://api.edamam.com/api/recipes/v2"
    
    # בגרסה v2 חובה להוסיף את הפרמטר type=public
    params = {
        "type": "public",
        "q": "chicken",
        "app_id": app_id,
        "app_key": app_key
    }
    
    try:
        print(f"שולח בקשה לכתובת: {url}...")
        response = requests.get(url, params=params)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            hits = data.get('hits', [])
            print(f"הצלחה! המערכת מחוברת. נמצאו {len(hits)} מתכונים.")
            if hits:
                print(f"מתכון ראשון שחזר: {hits[0]['recipe']['label']}")
        elif response.status_code == 401:
            print("שגיאה 401 (Unauthorized):")
            print("המפתחות נדחו על ידי השרת. וודא שהעתקת אותם במדויק מה-Dashboard באתר Edamam.")
        elif response.status_code == 404:
            print("שגיאה 404 (Not Found):")
            print("הכתובת לא נמצאה. וודא שאין טעות כתיב ב-URL.")
        else:
            print(f"שגיאה {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"שגיאת תקשורת חמורה: {e}")

if __name__ == "__main__":
    test_edamam()