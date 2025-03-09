from Bio import Entrez
from typing import List, Dict
from dotenv import load_dotenv
import os

def configure_email():
    load_dotenv()
    email = os.environ.get("PUBMED_EMAIL")
    if not email:
        raise ValueError("Set PUBMED_EMAIL environment variable.")
    Entrez.email = email

def search_papers(query: str, max_results: int = 100) -> List[str]:
    handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
    record = Entrez.read(handle)
    handle.close()
    return record["IdList"]

def fetch_paper_details(pm_ids: List[str]) -> List[Dict]:
    if not pm_ids:
        return []
    handle = Entrez.efetch(db="pubmed", id=pm_ids, retmode="xml")
    records = Entrez.read(handle)['PubmedArticle']
    handle.close()
    return records