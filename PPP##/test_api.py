import os
import json
import pandas as pd
from dotenv import load_dotenv

def pre_flight_check():
    print("--- מתחיל בדיקת תקינות מערכת ---")
    all_passed = True

    # 1. בדיקת סביבה (Environment)
    load_dotenv()
    app_id = os.getenv("EDAMAM_APP_ID")
    app_key = os.getenv("EDAMAM_APP_KEY")
    
    if app_id and app_key:
        print(f"✅ מפתחות API נטענו בהצלחה (ID מסתיים ב: {app_id[-3:]})")
    else:
        print("❌ שגיאה: מפתחות API חסרים בתוך קובץ .env")
        all_passed = False

    # 2. בדיקת תיקיות וקבצי נתונים
    required_files = {
        'data/recipes.json': 'מאגר מתכונים מקומי',
        'data/pantry.json': 'מלאי מזווה',
        'data/cbs_prices.csv': 'נתוני מחירים מהלמ"ס'
    }

    if not os.path.exists('data'):
        os.makedirs('data')
        print("📂 יצרתי תיקיית 'data' חדשה")

    for path, description in required_files.items():
        if os.path.exists(path):
            print(f"✅ קובץ קיים: {path} ({description})")
        else:
            print(f"⚠️ אזהרה: הקובץ {path} חסר. המערכת תשתמש בברירות מחדל.")

    # 3. בדיקת תקינות פורמט JSON (recipes)
    recipe_path = 'data/recipes.json'
    if os.path.exists(recipe_path):
        try:
            with open(recipe_path, 'r', encoding='utf-8') as f:
                json.load(f)
            print("✅ פורמט JSON של המתכונים תקין")
        except Exception as e:
            print(f"❌ שגיאה: קובץ המתכונים פגום - {e}")
            all_passed = False

    # 4. בדיקת ספריות מותקנות
    try:
        import requests
        print(f"✅ ספריית requests מותקנת")
    except ImportError:
        print("❌ שגיאה: ספריית requests לא מותקנת. הרץ: pip install requests")
        all_passed = False

    print("\n--- סיכום בדיקה ---")
    if all_passed:
        print("🚀 המערכת מוכנה להרצה! אפשר להפעיל את main.py")
    else:
        print("🛠️ יש לתקן את השגיאות לעיל לפני הרצת המערכת.")

if __name__ == "__main__":
    pre_flight_check()