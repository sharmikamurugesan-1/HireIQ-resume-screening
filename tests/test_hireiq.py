"""
Unit & Integration Tests for HireIQ-resume-screening
Validates resume entity parsing, PII anonymization, multi-criteria scoring breakdown,
and skill gap analysis.
"""

import pytest
from parser import ResumeParser
from matcher import JobMatcher

SAMPLE_RESUME_TEXT = """
Alex Chen
Email: alex.chen@ai-innovations.io
Phone: (415) 555-0192
Location: San Francisco, CA

PROFESSIONAL SUMMARY
Senior AI Engineer with 6+ years of experience designing RAG pipelines, FastAPI microservices, and deploying machine learning models to production using Docker and Kubernetes.

TECHNICAL SKILLS
Languages & Frameworks: Python, FastAPI, Flask, PyTorch, Scikit-learn, SQL, Docker, Git.
Specializations: RAG, FAISS, NLP, Vector Embeddings.

EDUCATION
B.Tech in Computer Science & Engineering, Top Tier University (2018)
"""

def test_resume_parser_and_pii_anonymization():
    parser = ResumeParser()
    parsed = parser.parse_text(SAMPLE_RESUME_TEXT, "resume_alex.txt")
    
    assert parsed["name"] == "Alex Chen"
    assert parsed["email"] == "alex.chen@ai-innovations.io"
    assert parsed["years_experience"] >= 5
    assert "Python" in parsed["skills"]
    assert "Fastapi" in parsed["skills"]
    assert "B.Tech" in parsed["education"]

    # Test blind review anonymization
    anon = parser.anonymize_candidate(parsed)
    assert anon["display_name"].startswith("Candidate-")
    assert "[REDACTED" in anon["display_email"]

def test_multi_criteria_scoring_and_gap_analysis():
    parser = ResumeParser()
    cand = parser.parse_text(SAMPLE_RESUME_TEXT, "resume_alex.txt")

    matcher = JobMatcher(
        job_title="Senior Python & AI Engineer",
        required_skills=["Python", "FastAPI", "RAG", "Docker", "Airflow"],
        min_years_exp=4
    )
    scored = matcher.score_candidate(cand)

    assert scored["match_score"] >= 75.0
    breakdown = scored["score_breakdown"]
    
    # Check 4 pillars exist and weights sum to 100
    assert "skills_match" in breakdown
    assert "experience_tenure" in breakdown
    assert "education" in breakdown
    assert "semantic_fit" in breakdown
    assert (breakdown["skills_match"]["max"] + breakdown["experience_tenure"]["max"] +
            breakdown["education"]["max"] + breakdown["semantic_fit"]["max"]) == 100.0

    # Skill gaps
    gaps = scored["skill_gap_analysis"]
    assert "Python" in gaps["matched_skills"]
    assert "Fastapi" in gaps["matched_skills"]
    assert "Airflow" in gaps["missing_critical_skills"]
    assert "disclaimer" in scored
