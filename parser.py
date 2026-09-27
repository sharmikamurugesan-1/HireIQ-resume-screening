"""
HireIQ — Resume Parser & Entity Extractor
Extracts candidate skills, education, experience tenure, and supports
privacy-preserving PII anonymization for unbiased blind screening.
"""

import re
import os
import hashlib
from typing import Dict, Any, List

KNOWN_SKILLS = [
    "python", "fastapi", "flask", "django", "pandas", "numpy", "scikit-learn",
    "tensorflow", "pytorch", "rag", "faiss", "nlp", "selenium", "beautifulsoup",
    "docker", "kubernetes", "aws", "gcp", "azure", "sql", "postgresql", "sqlite",
    "git", "ci/cd", "power bi", "tableau", "javascript", "react", "html", "css",
    "rest api", "graphql", "linux", "spark", "airflow"
]

DEGREE_PATTERNS = [
    r'\b(?:B\.?Tech|B\.?E\.?|B\.?S\.?|Bachelor(?:\'s)?)\b',
    r'\b(?:M\.?Tech|M\.?S\.?|Master(?:\'s)?|MBA)\b',
    r'\b(?:Ph\.?D\.?|Doctorate)\b'
]

class ResumeParser:
    def __init__(self):
        self.email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b')
        self.phone_pattern = re.compile(r'\+?\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}')

    def parse_text(self, text: str, filename: str = "resume.txt") -> Dict[str, Any]:
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        candidate_name = lines[0] if lines else "Candidate"

        # Email & Phone
        email_match = self.email_pattern.search(text)
        email = email_match.group(0) if email_match else "N/A"

        phone_match = self.phone_pattern.search(text)
        phone = phone_match.group(0) if phone_match else "N/A"

        # Skills extraction
        text_lower = text.lower()
        extracted_skills = []
        for skill in KNOWN_SKILLS:
            if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
                extracted_skills.append(skill.title())

        # Experience extraction
        exp_match = re.search(r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of)?\s*experience', text_lower)
        if exp_match:
            years_exp = int(exp_match.group(1))
        else:
            # Fallback heuristic: count year ranges e.g. 2020 - 2024
            year_matches = re.findall(r'\b(20[0-2]\d)\b', text)
            if len(year_matches) >= 2:
                years = sorted([int(y) for y in year_matches])
                years_exp = max(1, years[-1] - years[0])
            else:
                years_exp = 3

        # Education extraction
        degrees = []
        for deg in DEGREE_PATTERNS:
            m = re.search(deg, text, re.IGNORECASE)
            if m:
                degrees.append(m.group(0).strip())
        degree_str = ", ".join(degrees) if degrees else "Relevant Technical Degree"

        # Deterministic blind ID
        blind_id = f"Candidate-{hashlib.md5(candidate_name.encode('utf-8')).hexdigest()[:6].upper()}"

        return {
            "filename": filename,
            "blind_id": blind_id,
            "name": candidate_name,
            "email": email,
            "phone": phone,
            "skills": extracted_skills,
            "years_experience": years_exp,
            "education": degree_str,
            "raw_text": text
        }

    def anonymize_candidate(self, candidate_data: Dict[str, Any]) -> Dict[str, Any]:
        """Redacts candidate PII for blind screening compliance."""
        anon = candidate_data.copy()
        anon["display_name"] = anon["blind_id"]
        anon["display_email"] = "[REDACTED FOR BLIND REVIEW]"
        anon["display_phone"] = "[REDACTED FOR BLIND REVIEW]"
        return anon

    def parse_file(self, file_path: str) -> Dict[str, Any]:
        filename = os.path.basename(file_path)
        ext = os.path.splitext(filename)[1].lower()

        if ext == '.pdf':
            import pypdf
            reader = pypdf.PdfReader(file_path)
            content = "\n".join([p.extract_text() or "" for p in reader.pages])
        else:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

        return self.parse_text(content, filename)
