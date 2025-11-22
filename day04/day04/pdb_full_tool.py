import requests
import csv
import os
from pathlib import Path

def get_full_protein_data(protein_name):
    print(f"\n--- 🧬 UniProt Full Data Fetcher 🧬 ---")
    print(f"Searching for human protein '{protein_name}'...")
    
    # 1. חיפוש החלבון
    search_url = "https://rest.uniprot.org/uniprotkb/search"
    params = {
        "query": f"(gene_exact:{protein_name} OR protein_name:{protein_name}) AND organism_id:9606 AND reviewed:true",
        "format": "json",
        "size": 1
    }
    
    try:
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        results = response.json().get('results', [])
        
        if not results:
            print("❌ No matching human protein found.")
            return

        entry = results[0]
        gene_name = entry['genes'][0]['geneName']['value']
        print(f"✅ Found Gene: {gene_name}")

        # --- שלב חדש: חילוץ מידע כללי על החלבון ---
        
        # 1. אורך כולל (Total Length)
        total_length = entry['sequence']['length']
        
        # 2. תפקיד ומחלות (Function & Disease)
        # המידע הזה נמצא בתוך רשימת ה-'comments'
        function_list = []
        disease_list = []
        
        for comment in entry.get('comments', []):
            # חילוץ תפקיד
            if comment['commentType'] == 'FUNCTION':
                for txt in comment.get('texts', []):
                    function_list.append(txt['value'])
            
            # חילוץ מחלה
            if comment['commentType'] == 'DISEASE':
                # בדרך כלל המידע נמצא בתוך note->texts
                if 'note' in comment and 'texts' in comment['note']:
                    for txt in comment['note']['texts']:
                        disease_list.append(txt['value'])
                # לפעמים ישירות ב-texts
                elif 'texts' in comment:
                    for txt in comment['texts']:
                        disease_list.append(txt['value'])

        # איחוד הטקסטים (למקרה שיש כמה סעיפים)
        function_str = " | ".join(function_list)
        if len(function_str) > 300: function_str = function_str[:300] + "..." # קיצור אם זה ארוך מדי

        disease_str = " | ".join(disease_list)
        if not disease_str: disease_str = "No disease association mentioned"
        
        print(f"   -> Length: {total_length} AA")
        print(f"   -> Disease info found: {'Yes' if disease_list else 'No'}")

        # -----------------------------------------------

        # 3. חילוץ המבנים (כמו קודם)
        structures = []
        db_refs = entry.get('uniProtKBCrossReferences', [])
        
        for ref in db_refs:
            if ref['database'] == 'PDB':
                pdb_id = ref['id']
                method = "Unknown"
                resolution = "N/A"
                chains = "N/A"
                
                for prop in ref.get('properties', []):
                    if prop['key'] == 'Method': method = prop['value']
                    elif prop['key'] == 'Resolution': resolution = prop['value']
                    elif prop['key'] == 'Chains': chains = prop['value']

                structures.append({
                    "PDB ID": pdb_id,
                    "Method": method,
                    "Resolution": resolution,
                    "Solved Ranges": chains,
                    # הוספת העמודות החדשות לכל שורה
                    "Total Protein Length": total_length,
                    "Function": function_str,
                    "Associated Diseases": disease_str
                })

        if not structures:
            print("⚠️ Protein found, but NO structures listed in PDB.")
            return

        # 4. שמירה לקובץ
        filename = f"{gene_name}_full_data.csv"
        current_dir = Path(__file__).parent.absolute()
        full_path = current_dir / filename
        
        # הגדרת סדר העמודות
        headers = ["PDB ID", "Method", "Resolution", "Solved Ranges", 
                   "Total Protein Length", "Function", "Associated Diseases"]

        with open(full_path, "w", newline='', encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(structures)
        
        print(f"\n✅ SUCCESS! File created at:\n{full_path}")
        try:
            os.startfile(current_dir)
        except:
            pass

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    term = input("Enter gene name (e.g. TP53, INS, CFTR): ").strip()
    if term:
        get_full_protein_data(term)