import requests

def search_structures(protein_name, limit=10):
    """
    חיפוש PDB לפי טקסט מלא
    """
    search_url = "https://search.rcsb.org/rcsbsearch/v2/query"
    
    query = {
        "query": {
            "type": "terminal",
            "service": "full_text",
            "parameters": {
                "value": protein_name
            }
        },
        "return_type": "entry",
        "request_options": {
            "paginate": {"start": 0, "rows": limit}
        }
    }
    
    try:
        response = requests.post(search_url, json=query)
        response.raise_for_status()
        
        result_set = response.json().get('result_set', [])
        ids = [item['identifier'] for item in result_set]
        return ids
        
    except Exception as e:
        print(f"Search Error: {e}")
        return []

def get_structure_details(pdb_ids):
    """
    שליפת נתונים מורחבת בצורה יציבה (Robust)
    """
    if not pdb_ids:
        return []

    url = "https://data.rcsb.org/graphql"
    
    # השאילתה המקורית
    query_string = """
    query structure_data($ids: [String!]!) {
      entries(entry_ids: $ids) {
        rcsb_id
        struct {
          title
        }
        exptl {
          method
        }
        rcsb_entry_info {
          resolution_combined
        }
        polymer_entities {
          entity_poly {
            rcsb_sample_sequence_length
            type
          }
          struct_ref {
            db_name
            pdbx_db_accession
            pdbx_align_begin
            pdbx_align_end
          }
        }
      }
    }
    """
    
    try:
        response = requests.post(url, json={'query': query_string, 'variables': {'ids': pdb_ids}})
        
        # הדפסת שגיאה אם השרת החזיר תשובה לא תקינה
        if response.status_code != 200:
            print(f"Server Error {response.status_code}: {response.text}")
            return []
            
        data = response.json()
        
        # בדיקה אם ה-API החזיר שגיאות פנימיות
        if 'errors' in data:
            print("Note: Some PDB errors occurred (partial data might be returned).")
        
        parsed_results = []
        entries = data.get('data', {}).get('entries', []) or []

        if not entries:
            print("Warning: No entry data found in response.")
            return []

        for entry in entries:
            try:
                # 1. שיטה ורזולוציה
                methods = [e['method'] for e in entry.get('exptl', []) if e.get('method')]
                method_str = ", ".join(methods) if methods else "Unknown"
                
                res = entry.get('rcsb_entry_info', {}).get('resolution_combined')
                resolution = f"{res[0]} Å" if res else "N/A"

                # 2. חילוץ הטווחים (Ranges)
                mapped_ranges = []
                
                # בדיקה שהשדה polymer_entities בכלל קיים
                if entry.get('polymer_entities'):
                    for entity in entry['polymer_entities']:
                        poly_info = entity.get('entity_poly')
                        
                        # דילוג אם אין מידע על הפולימר
                        if not poly_info:
                            continue

                        # וידוא שזה חלבון (בודקים אם המילה polypeptide מופיעה בסוג)
                        p_type = poly_info.get('type', '')
                        if 'polypeptide' in p_type:
                            
                            # בדיקה אם יש מידע על טווחים (struct_ref)
                            refs = entity.get('struct_ref')
                            if refs:
                                for ref in refs:
                                    # אנחנו רוצים רק מידע שקשור ל-UniProt (UNP)
                                    if ref.get('db_name') == 'UNP':
                                        start = ref.get('pdbx_align_begin', '?')
                                        end = ref.get('pdbx_align_end', '?')
                                        uniprot_id = ref.get('pdbx_db_accession', 'Unknown')
                                        
                                        range_str = f"{uniprot_id}: {start}-{end}"
                                        if range_str not in mapped_ranges:
                                            mapped_ranges.append(range_str)
                
                ranges_str = ", ".join(mapped_ranges) if mapped_ranges else "N/A"
                title = entry.get('struct', {}).get('title', 'No Title')

                parsed_results.append({
                    "PDB ID": entry['rcsb_id'],
                    "Method": method_str,
                    "Resolution": resolution,
                    "Covered Ranges (AA)": ranges_str,
                    "Description": title
                })
            
            except Exception as inner_e:
                # אם שורה אחת נכשלת, נדלג עליה אבל לא נהרוס את כל הקובץ
                print(f"Skipping entry {entry.get('rcsb_id', 'unknown')} due to error: {inner_e}")
                continue
            
        return parsed_results
        
    except Exception as e:
        print(f"Critical Fetch Error: {e}")
        return []