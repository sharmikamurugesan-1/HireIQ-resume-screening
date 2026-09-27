"""
HireIQ — Resume Parser & Entity Extractor
Extracts candidate skills, contact info, and experience from resume text.
"""

import re
import os
from typing import Dict, Any, List

KNOWN_SKILLS = [
    "python", "fastapi", "flask", "django", "pandas", "numpy", "scikit-learn",
    "tensorflow", "pytorch", "rag", "faiss", "nlp", "selenium", "beautifulsoup",
    "docker", "kubernetes", "aws", "gcp", "sql", "postgresql", "sqlite", "git",
    "power bi", "tableau", "javascript", "react", "html", "css", "rest api"
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
            # Word boundary matching
            if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
                extracted_skills.append(skill.title())

        # Experience inference
        exp_match = re.search(r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of)?\s*experience', text_lower)
        years_exp = int(exp_match.group(1)) if exp_match else 2

        return {
            "filename": filename,
            "name": candidate_name,
            "email": email,
            "phone": phone,
            "skills": extracted_skills,
            "years_experience": years_exp,
            "raw_text": text
        }

    def parse_file(self, file_path: str) -> Dict[str, Any]:
        filename = os.path.basename(file_path)
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return self.parse_text(f.read(), filename)
