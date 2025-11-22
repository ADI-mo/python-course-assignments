import requests
import xml.etree.ElementTree as ET
import re
from collections import Counter

def search_pubmed(term, limit=10):
    """מחפש ומחזיר רשימה של IDs לפי הכמות שהמשתמש ביקש"""
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": term,
        "retmode": "json",
        "retmax": limit  # שימוש בפרמטר דינמי
    }
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    # טיפול במקרה שאין תוצאות
    if "idlist" not in response.json()["esearchresult"]:
        return []
    return response.json()["esearchresult"]["idlist"]

def fetch_details(id_list):
    """מוריד את הפרטים המלאים כולל Abstract"""
    if not id_list:
        return []

    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        "db": "pubmed",
        "id": ",".join(id_list),
        "retmode": "xml"
    }
    
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    
    root = ET.fromstring(response.content)
    articles_data = []
    
    for article in root.findall(".//PubmedArticle"):
        title = article.findtext(".//ArticleTitle", default="No Title")
        abstract = article.findtext(".//AbstractText", default="")
        journal = article.findtext(".//Title", default="Unknown Journal")
        pub_year = article.findtext(".//PubDate/Year", default="N/A")

        articles_data.append({
            "id": article.findtext(".//PMID"),
            "title": title,
            "abstract": abstract,
            "journal": journal,
            "year": pub_year
        })
        
    return articles_data

def analyze_keywords(articles_list):
    """
    פונקציה חכמה: לוקחת את כל התקצירים, מנקה מילות קישור,
    ומחזירה את 10 המילים הכי נפוצות במחקרים האלו.
    """
    all_text = " ".join([art['abstract'] for art in articles_list]).lower()
    
    # ניקוי סימני פיסוק וחלוקה למילים
    words = re.findall(r'\b[a-z]{3,}\b', all_text)
    
    # רשימת מילים שכיחות שאין להן משמעות (Stop words)
    stop_words = {
        "the", "and", "of", "in", "to", "with", "is", "for", "that", "was", 
        "were", "are", "by", "as", "on", "from", "at", "this", "these", "an"
    }
    
    # סינון מילות קישור
    meaningful_words = [w for w in words if w not in stop_words]
    
    # ספירה והחזרה של ה-10 הכי נפוצות
    return Counter(meaningful_words).most_common(10)