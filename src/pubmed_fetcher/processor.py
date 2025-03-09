import datetime
import re
from typing import Optional, Dict

ACADEMIC_KEYWORDS = ['university', 'college', 'institute', 'academy', 'school', 'lab']
PHARMA_KEYWORDS = [
    'pharma', 'biotech', 'pharmaceutical', 'life sciences',
    'inc.', 'ltd', 'corporation', 'co.', 'research',
    'bio', 'genentech', 'novartis', 'pfizer',  
    'roche', 'merck', 'gsk', 'sanofi', 'astrazeneca'
]
def is_academic(affiliation: str) -> bool:
    pattern = re.compile(r'\b(' + '|'.join(ACADEMIC_KEYWORDS) + r')\b', re.I)
    return bool(pattern.search(affiliation)) if affiliation else False

def is_pharma_biotech(affiliation: str) -> bool:
    pattern = re.compile(r'\b(' + '|'.join(PHARMA_KEYWORDS) + r')\b', re.I)
    return bool(pattern.search(affiliation)) if affiliation else False

def extract_email(affiliation: str) -> Optional[str]:
    match = re.search(r'\b[\w.-]+@[\w.-]+\.\w+\b', affiliation)
    return match.group(0) if match else None

def process_paper(paper: Dict) -> Optional[Dict]:
    article = paper['MedlineCitation']['Article']
    pubmed_id = str(paper['MedlineCitation']['PMID'])
    title = article.get('ArticleTitle', '')
    pub_date = article['Journal']['JournalIssue']['PubDate']
    
    # Format publication date
    year = pub_date.get('Year', '')
    month = pub_date.get('Month', '01').lower()[:3]
    day = pub_date.get('Day', '01')
    try:
        month_num = f"{datetime.datetime.strptime(month, '%b').month:02d}"
    except ValueError:
        month_num = '01'
    publication_date = f"{year}-{month_num}-{day.zfill(2)}" if year else ""
    
    # Process authors
    authors = article.get('AuthorList', [])
    non_academic_authors = []
    companies = set()
    emails = []
    
    for author in authors:
        name = f"{author.get('ForeName', '')} {author.get('LastName', '')}".strip()
        if not name:
            continue
        
        affiliation = '; '.join([info.get('Affiliation', '') for info in author.get('AffiliationInfo', [])])
        if not is_academic(affiliation):
            non_academic_authors.append(name)
            if is_pharma_biotech(affiliation):
                companies.add(affiliation)
        
        email = extract_email(affiliation)
        if email:
            emails.append(email)
    
    if not companies:
        return None
    
    return {
        'PubmedID': pubmed_id,
        'Title': title,
        'Publication Date': publication_date,
        'Non-academic Author(s)': '; '.join(non_academic_authors),
        'Company Affiliation(s)': '; '.join(companies),
        'Corresponding Author Email': emails[0] if emails else ''
    }