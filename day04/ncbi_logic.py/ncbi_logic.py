import requests
import xml.etree.ElementTree as ET  # ספרייה לקריאת XML

def search_pubmed(term, retmax=3):
    """
    מחפש מונח ומחזיר רשימה של מזהים (IDs).
    נשאר ללא שינוי.
    """
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": term,
        "retmode": "json",
        "retmax": retmax
    }
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    return response.json()["esearchresult"]["idlist"]

def fetch_details(id_list):
    """
    מקבל רשימת מזהים ומחזיר רשימה של מילונים עם כותרת ותקציר.
    שינינו כאן ל-efetch ולפורמט XML.
    """
    if not id_list:
        return []

    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    
    params = {
        "db": "pubmed",
        "id": ",".join(id_list),
        "retmode": "xml"  # שינוי חשוב: מבקשים XML
    }
    
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    
    # --- חלק חדש: ניתוח ה-XML ---
    # המרה של הטקסט שחזר מהשרת למבנה שהקוד מבין
    root = ET.fromstring(response.content)
    
    articles_data = []
    
    # עוברים על כל מאמר שנמצא בתשובה
    for article in root.findall(".//PubmedArticle"):
        # ניסיון למצוא כותרת
        title_node = article.find(".//ArticleTitle")
        title = title_node.text if title_node is not None else "No Title"
        
        # ניסיון למצוא תקציר
        abstract_node = article.find(".//AbstractText")
        abstract = abstract_node.text if abstract_node is not None else "No Abstract Available"
        
        # ניסיון למצוא שם ג'ורנל
        journal_node = article.find(".//Title") # בתוך Journal
        journal = journal_node.text if journal_node is not None else "Unknown Journal"

        articles_data.append({
            "title": title,
            "abstract": abstract,
            "journal": journal
        })
        
    return articles_data