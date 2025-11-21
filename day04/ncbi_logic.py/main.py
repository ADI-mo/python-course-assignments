import ncbi_logic

def run():
    print("--- NCBI PubMed Search Tool (With Abstract) ---")
    term = input("Enter a search term: ")
    
    try:
        print(f"Searching for '{term}'...")
        ids = ncbi_logic.search_pubmed(term)
        
        if not ids:
            print("No results found.")
            return

        print(f"Found {len(ids)} articles. Fetching abstracts...")
        # הפעם אנחנו מקבלים רשימה מסודרת של מאמרים
        articles = ncbi_logic.fetch_details(ids)
        
        full_output = "" # נצבור את הטקסט כדי לשמור אותו לקובץ אחר כך

        for item in articles:
            # הכנת הטקסט להדפסה
            text_block = (
                f"\n{'='*40}\n"
                f"Title:   {item['title']}\n"
                f"Abstract: {item['abstract']}\n" # הדפסת התקציר
                f"{'='*40}\n"
            )
            
            print(text_block)
            full_output += text_block
                
        # שמירה לקובץ
        filename = f"{term.replace(' ', '_')}_abstracts.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(full_output)
        print(f"\nSaved full details to {filename}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run()