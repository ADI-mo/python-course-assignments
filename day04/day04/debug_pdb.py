import requests

def debug_ace2():
    print("--- 🕵️‍♂️ STARTING DEBUG ---")
    
    # נלך ישירות ל-ID של ACE2 כדי למנוע בעיות חיפוש
    url = "https://rest.uniprot.org/uniprotkb/Q9BYF1.json"
    print(f"1. Connecting to: {url}")
    
    try:
        r = requests.get(url)
        data = r.json()
        print("2. Download successful.")
        
        # בדיקת רשימת ההפניות
        refs = data.get('uniProtKBCrossReferences', [])
        print(f"3. Found {len(refs)} total references in the file.")
        
        # ספירת PDB
        pdb_list = [ref for ref in refs if ref['database'] == 'PDB']
        print(f"4. Found {len(pdb_list)} PDB structures inside.")
        
        if len(pdb_list) > 0:
            print("\n✅ SUCCESS! Data exists. Here represents the first one:")
            print(pdb_list[0])
        else:
            print("\n❌ ERROR: No PDB entries found. Listing first 5 databases found instead:")
            for ref in refs[:5]:
                print(f" - {ref.get('database')}")

    except Exception as e:
        print(f"❌ CRASHED: {e}")

if __name__ == "__main__":
    debug_ace2()