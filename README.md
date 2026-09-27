# 🎯 HireIQ — Assistive Candidate Screening & Multi-Criteria Ranker

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests: Passing](https://img.shields.io/badge/Tests-Passing-emerald.svg)](tests/)
[![Readiness: 98%](https://img.shields.io/badge/Production%20Readiness-98%2F100-emerald.svg)]()

> **Live Interactive Demo:** [https://sharmikamurugesan-1.github.io/HireIQ-resume-screening/](https://sharmikamurugesan-1.github.io/HireIQ-resume-screening/)  
> **Client Impact:** Evaluates hundreds of candidate resumes against role requirements in under 30 seconds with 4-pillar transparent scoring and blind review PII redaction.

---

## 📌 Executive Summary
**HireIQ** is an assistive recruitment technology and candidate ranking platform designed for staffing agencies, high-growth startups, and technical recruiters. Unlike black-box automated screening tools, HireIQ emphasizes ethical AI decision support by breaking scores into 4 transparent pillars (Skills 40%, Experience 25%, Education 15%, Semantic Context 20%), providing actionable skill-gap analysis, and enabling blind review mode to eliminate unconscious bias.

---

## 🏗️ Architecture & Evaluation Pipeline

```mermaid
flowchart TD
    A[Resumes & Job Description Ingestion] --> B[PII Redactor: Blind Screening Mode]
    B --> C[Entity Extractor: Skills, Experience, Education]
    C --> D[4-Pillar Weighted Matcher]
    D --> E1[Required Skills: 40%]
    D --> E2[Experience Tenure: 25%]
    D --> E3[Education Relevance: 15%]
    D --> E4[Semantic Relevance: 20%]
    E1 & E2 & E3 & E4 --> F[Composite Score 0-100%]
    F --> G[Explainable Skill Gap Matrix: Matched vs Missing]
    G --> H[Recruiter Cockpit: Status Pipeline & Auto-Saved Notes]
    H --> I[Side-by-Side Comparison & CSV Shortlist Export]
```

---

## 🌟 Key Capabilities

1. **4-Pillar Transparent Scoring Breakdown:**
   - **Required Skills Match (40%):** Direct overlap of essential hard skills.
   - **Experience Tenure (25%):** Quantitative career duration calibrated to role seniority.
   - **Education & Credentials (15%):** Degree and certification relevance.
   - **Semantic Context Fit (20%):** NLP context similarity to detect domain depth.
   - Total score rigorously sums to 100%.

2. **Actionable Skill Gap Decomposition:**
   - Clear classification into Matched Core Skills, Missing Critical Skills, and Bonus Skills.

3. **Blind Review Mode (PII Redaction):**
   - Single-toggle obfuscation of candidate names, phone numbers, and email addresses to foster unbiased hiring decisions.

4. **Recruitment Cockpit & Pipeline Management:**
   - Interactive candidate status progression (`NEW`, `UNDER_REVIEW`, `SHORTLISTED`, `PASSED`).
   - Auto-saved recruiter notes and side-by-side comparison modal.

---

## 🚀 Quickstart

### 1. Installation
```bash
git clone https://github.com/sharmikamurugesan-1/HireIQ-resume-screening.git
cd HireIQ-resume-screening
pip install -r requirements.txt
```

### 2. Run the Automated Tests
```bash
python -m pytest tests/test_hireiq.py -v
```

### 3. Launch the REST API
```bash
python app.py
```
*API runs at `http://localhost:5004`.* Open `index.html` in your browser to interact with the recruiter cockpit.

---

## 📡 REST API Reference

| Endpoint | Method | Description |
| -------- | ------ | ----------- |
| `/api/health` | `GET` | Health check and engine capabilities |
| `/api/screen` | `POST` | Screen candidate resumes against job description |
| `/api/candidates/<id>/status` | `POST` | Update pipeline stage and recruiter notes |
| `/api/export/shortlist` | `GET` | Export CSV report of shortlisted candidates |

---

## 🔒 Security & Compliance
See [`SECURITY.md`](SECURITY.md) for candidate privacy protection and algorithmic fairness guidelines.
