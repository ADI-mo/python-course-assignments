import pdb_logic
import csv
from pathlib import Path

def run():
    print("--- 🧬 PDB Range Fetcher 🧬 ---")
    protein = input("Enter protein name (e.g., p53, Hemoglobin): ").strip()
    
    if not protein:
        return

    print(f"\n🔍 Searching PDB for '{protein}'...")
    ids = pdb_logic.search_structures(protein, limit=10)
    
    if not ids:
        print("No structures found.")
        return
    
    print(f"Found {len(ids)} structures. Fetching amino acid ranges...")
    data = pdb_logic.get_structure_details(ids)
    
    # שמירה ל-CSV
    save_folder = Path(__file__).parent
    filename = f"{protein}_ranges.csv"
    full_path = save_folder / filename
    
    try:
        with open(full_path, "w", newline='', encoding="utf-8") as f:
            # עדכון הכותרות לעמודה החדשה
            fieldnames = ["PDB ID", "Method", "Resolution", "Covered Ranges (AA)", "Description"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
            
        print(f"\n✅ Success! File saved to: {full_path}")
        
        # הדפסה למסך כדי שתראה שזה עובד
        print("\nPreview of ranges found:")
        for item in data[:3]:
            print(f"ID: {item['PDB ID']} | Ranges: {item['Covered Ranges (AA)']}")
            print(f"   -> {item['Description'][:60]}...")
            print("-" * 30)

    except Exception as e:
        print(f"Error saving file: {e}")

if __name__ == "__main__":
    run()