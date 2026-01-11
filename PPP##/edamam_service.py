import os
import requests
from dotenv import load_dotenv

load_dotenv()

class EdamamService:
    def __init__(self):
        self.app_id = os.getenv("EDAMAM_APP_ID")
        self.app_key = os.getenv("EDAMAM_APP_KEY")
        self.base_url = "https://api.edamam.com/api/recipes/v2"

    def fetch_recipes(self, query, diet='Standard', max_time=45):
        params = {
            "type": "public",
            "q": query,
            "app_id": self.app_id,
            "app_key": self.app_key,
            "time": f"1-{max_time}"
        }
        
        if diet == 'Vegan': params["health"] = "vegan"
        elif diet == 'Vegetarian': params["health"] = "vegetarian"

        try:
            response = requests.get(self.base_url, params=params)
            if response.status_code == 200:
                return self._normalize(response.json().get('hits', []))
        except Exception as e:
            print(f"API Error: {e}")
        return []

    def _normalize(self, hits):
        normalized = []
        for hit in hits:
            r = hit['recipe']
            # זיהוי סוג מנה בסיסי לכשרות
            ingredients_str = " ".join(r['ingredientLines']).lower()
            m_type = "Parve"
            if any(x in ingredients_str for x in ['meat', 'chicken', 'beef']): m_type = "Meat"
            elif any(x in ingredients_str for x in ['cheese', 'milk', 'cream']): m_type = "Dairy"

            normalized.append({
                "name": r['label'],
                "type": m_type,
                "is_vegan": "Vegan" in r.get('healthLabels', []),
                "is_vegetarian": "Vegetarian" in r.get('healthLabels', []),
                "prep_time": int(r.get('totalTime', 30)),
                "ingredients": {ing: 1 for ing in r['ingredientLines']} 
            })
        return normalized