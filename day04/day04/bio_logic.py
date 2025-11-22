import requests

def fetch_protein_data_robust(gene_name):
    print(f"--- LOGIC: Searching for {gene_name} ---")
    
    # שלב 1: חיפוש ה-ID של החלבון
    search_url = "https://rest.uniprot.org/uniprotkb/search"
    params = {
        "query": f"(gene_exact:{gene_name} OR protein_name:{gene_name}) AND organism_id:9606 AND reviewed:true",
        "format": "json",
        "size": 1
    }
    
    try:
        # חיפוש ראשוני
        r = requests.get(search_url, params=params)
        r.raise_for_status()
        results = r.json().get('results', [])
        
        if not results:
            print("❌ Logic: No ID found.")
            return None, []

        accession_id = results[0]['primaryAccession']
        print(f"✅ Logic: Found Accession ID -> {accession_id}")
        
        # שלב 2: שליפת הקובץ המלא לפי ה-ID
        # זה השלב הקריטי שמוודא שנקבל את כל מאות המבנים
        full_url = f"https://rest.uniprot.org/uniprotkb/{accession_id}.json"
        
        r_full = requests.get(full_url)
        r_full.raise_for_status()
        entry = r_full.json()
        
        # --- עיבוד הנתונים ---
        
        # 1. מידע כללי (Metadata)
        try:
            g_name = entry['genes'][0]['geneName']['value']
        except: 
            g_name = gene_name
        
        try:
            p_name = entry['proteinDescription']['recommendedName']['fullName']['value']
        except: 
            p_name = "Unknown"
        
        metadata = {
            "gene": g_name,
            "protein": p_name,
            "length": entry.get('sequence', {}).get('length', 0),
            "disease": "None mentioned",
            "function": "None mentioned"
        }
        
        # חילוץ מחלות ותפקיד מתוך ההערות
        diseases = []
        funcs = []
        for c in entry.get('comments', []):
            if c['commentType'] == 'DISEASE':
                if 'note' in c: diseases.append(c['note']['texts'][0]['value'])
                elif 'texts' in c: diseases.append(c['texts'][0]['value'])
            if c['commentType'] == 'FUNCTION':
                funcs.append(c['texts'][0]['value'])
        
        if diseases: metadata['disease'] = " | ".join(diseases)
        if funcs: metadata['function'] = funcs[0]

        # 2. חילוץ המבנים (PDB)
        structures = []
        all_refs = entry.get('uniProtKBCrossReferences', [])
        
        for ref in all_refs:
            if ref['database'] == 'PDB':
                props = {p['key']: p['value'] for p in ref.get('properties', [])}
                structures.append({
                    "id": ref['id'],
                    "method": props.get('Method', '-'),
                    "res": props.get('Resolution', '-'),
                    "chains": props.get('Chains', '-')
                })
        
        print(f"✅ Logic: Returning {len(structures)} structures.")
        return metadata, structures

    except Exception as e:
        print(f"❌ Logic Error: {e}")
        return None, []