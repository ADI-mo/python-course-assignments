import ncbi_logic
import csv
from pathlib import Path

def run():
    print("--- 🧬 Advanced PubMed Researcher 🧬 ---")
    
    # 1. קלט משתמש מתקדם
    term = input("Enter search term: ")
    try:
        limit = int(input("How many articles to analyze? (Max 50): "))
    except ValueError:
        limit = 5 # ברירת מחדל אם המשתמש הקיש שטויות

    try:
        # 2. חיפוש
        print(f"\n🔍 Searching for '{term}'...")
        ids = ncbi_logic.search_pubmed(term, limit)
        
        if not ids:
            print("❌ No results found.")
            return

        # 3. הורדה
        print(f"📥 Found {len(ids)} articles. Downloading abstracts...")
        articles = ncbi_logic.fetch_details(ids)
        
        # 4. ניתוח נתונים (החלק המתוחכם)
        print("🧠 Analyzing text patterns...")
        top_keywords = ncbi_logic.analyze_keywords(articles)
        
        print(f"\n📊 Top keywords in these papers:")
        print("-" * 30)
        for word, count in top_keywords:
            print(f"{word:15} : {count} times")
        print("-" * 30)

        # 5. שמירה לקובץ CSV (טבלה לאקסל)
        save_folder = Path(__file__).parent
        filename = f"{term.replace(' ', '_')}_analysis.csv"
        full_path = save_folder / filename
        
        with open(full_path, "w", newline='', encoding="utf-8") as csvfile:
            fieldnames = ['id', 'year', 'journal', 'title', 'abstract']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader() # כתיבת כותרות העמודות
            for art in articles:
                writer.writerow(art)
                
        print(f"\n✅ Success! Data saved to: {filename}")
        print("(You can open this file in Excel)")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run()