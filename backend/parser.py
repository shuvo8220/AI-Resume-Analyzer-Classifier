import pdfplumber
import re
import spacy
from datetime import datetime
from sentence_transformers import SentenceTransformer, util

print("Loading NLP Models...")
try:
    nlp = spacy.load("en_core_web_sm")
except:
    import subprocess, sys
    subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

SKILLS_DB = [
    "Python", "Java", "C++", "JavaScript", "TypeScript", "React", "Next.js", "Node.js",
    "SQL", "NoSQL", "MongoDB", "PostgreSQL", "AWS", "Azure", "Docker", "Kubernetes",
    "TensorFlow", "PyTorch", "Scikit-learn", "Pandas", "NumPy", "Flask", "Django", "FastAPI",
    "HTML", "CSS", "Tailwind", "Git", "Linux", "CI/CD", "Machine Learning", "Deep Learning",
    "NLP", "Data Analysis", "Communication", "Problem Solving"
]

skill_embeddings = embedding_model.encode(SKILLS_DB, convert_to_tensor=True)

def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            t = page.extract_text()
            if t: text += t + "\n"
    return text

def clean_text(text):
    return re.sub(r'\s+', ' ', text).strip()

def extract_details(text):
    # 1. Email
    email = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    
    # 2. Universal Phone Extraction
    phone_pattern = r'(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4,}'
    phone = re.search(phone_pattern, text)

    # 3. Smart Name Extraction
    BLOCKLIST = ["resume", "curriculum", "vitae", "cv", "bio", "data", "road", "house", "bazar", "dhaka", "street", "lane", "objective", "summary"]
    
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    top_lines = lines[:15]
    
    name = "Unknown Candidate"
    
    for line in top_lines:
        words = line.split()
        if 1 < len(words) <= 4 and line.istitle():
            if not any(bad_word in line.lower() for bad_word in BLOCKLIST):
                doc = nlp(line)
                if doc.ents and doc.ents[0].label_ == "PERSON":
                    name = line
                    break
                elif not re.search(r'\d', line) and "@" not in line:
                    name = line
                    break
    return name, email.group(0) if email else None, phone.group(0) if phone else None

def extract_education(text):
    """
    Extracts Education degrees and institutions.
    """
    education_keywords = ["B.Sc", "M.Sc", "Bachelor", "Master", "PhD", "Diploma", "Degree", "University", "Institute", "College"]
    edu_lines = []
    
    lines = text.split('\n')
    for line in lines:
        # Check if line contains any education keyword
        if any(kw.lower() in line.lower() for kw in education_keywords):
            # Avoid single word lines (noise)
            if len(line.split()) > 2: 
                edu_lines.append(line.strip())
    
    # Return unique top 3 education entries
    return list(set(edu_lines))[:3]

def extract_skills_ai(text):
    found_skills = set()
    text_lower = text.lower()

    # Fast: Direct Match
    for skill in SKILLS_DB:
        if re.search(r'\b' + re.escape(skill.lower()) + r'\b', text_lower):
            found_skills.add(skill)

    # Smart: AI Match
    doc = nlp(text)
    phrases = list(set([c.text for c in doc.noun_chunks if len(c.text.split()) < 3]))
    phrases = [p for p in phrases if p.lower() not in [s.lower() for s in found_skills]]

    if phrases:
        emb = embedding_model.encode(phrases, convert_to_tensor=True)
        scores = util.cos_sim(emb, skill_embeddings)
        for i in range(len(phrases)):
            for j in range(len(SKILLS_DB)):
                if scores[i][j] > 0.85:
                    found_skills.add(SKILLS_DB[j])
    return list(found_skills)

def calculate_experience_smart(text):
    """
    Calculates experience based on Date Ranges (e.g. 2018 - 2020)
    If ranges fail, falls back to Year Gap method.
    """
    text = text.lower()
    
    # 1. Regex for Date Ranges (e.g. "Jan 2020 - Present", "2018 - 2019", "05/2020 - 06/2021")
    # Matches: (Month Year) or (Year) ...to... (Month Year) or (Year) or (Present)
    date_range_pattern = r'(\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)?[a-z]*[-. ]*(?:19|20)\d{2})\s*(?:-|to|–)\s*(\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)?[a-z]*[-. ]*(?:19|20)\d{2}|present|current|now)'
    
    ranges = re.findall(date_range_pattern, text)
    
    total_months = 0
    
    if ranges:
        for start_str, end_str in ranges:
            try:
                # Normalize End Date
                if any(x in end_str for x in ["present", "current", "now"]):
                    end_date = datetime.now()
                else:
                    end_date = parse_date(end_str)

                start_date = parse_date(start_str)
                
                if start_date and end_date:
                    # Calculate difference in months
                    diff = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
                    if diff > 0:
                        total_months += diff
            except:
                continue
        
        exp_years = round(total_months / 12, 1)
    else:
        # Fallback: Max Year - Min Year (Excluding Education years)
        exp_years = calculate_fallback_experience(text)

    # Cap logic
    if exp_years > 30: exp_years = 0.0

    if exp_years >= 5: level = "Senior"
    elif exp_years >= 2: level = "Mid"
    else: level = "Junior"

    return exp_years, level

def parse_date(date_str):
    """Helper to parse fuzzy dates"""
    try:
        # Try finding just the year
        year = re.search(r'(20\d{2}|19\d{2})', date_str)
        if year:
            return datetime(int(year.group(0)), 1, 1)
    except:
        return None
    return None

def calculate_fallback_experience(text):
    # Old logic: Max - Min year (excluding education)
    lines = text.split('\n')
    valid_years = []
    current_year = datetime.now().year
    education_keywords = ["ssc", "hsc", "gpa", "school", "college", "university", "passing", "bachelor"]

    for line in lines:
        if any(kw in line.lower() for kw in education_keywords):
            continue
        years_in_line = re.findall(r'\b(20\d{2})\b', line)
        for y in years_in_line:
            y_int = int(y)
            if 2010 <= y_int <= current_year:
                valid_years.append(y_int)
    
    if not valid_years: return 0.0
    return float(current_year - min(valid_years))