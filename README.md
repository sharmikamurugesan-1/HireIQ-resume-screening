# 🎯 HireIQ — NLP Resume Screening & Job-Match Scorer

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![NLP Powered](https://img.shields.io/badge/NLP-TF--IDF%20Similarity-blueviolet.svg)]()

> **Impact:** ⚡ Screens and ranks 100 resumes against a job description in under 30 seconds.

**HireIQ** is an NLP-powered candidate screening and resume ranking tool designed for fast-growing startups and hiring teams. It extracts technical skills, years of experience, and contact data from candidate resumes, then calculates TF-IDF cosine similarity scores against job requirements to output an automated ranked candidate shortlist.

---

## 📌 Architecture & NLP Workflow

```
[Candidate Resumes (PDF / DOCX)]
              │
              ▼
[Entity Parser & Normalizer] ──► Extracts Skills, Experience & Contact
              │
              ▼
[TF-IDF Vector Space Matrix] ──► Computes Cosine Similarity against JD
              │
              ▼
[Ranked Leaderboard Output]  ──► Generates sorted Excel shortlist & verdicts
```

---

## ✨ Features

- **Automated Resume Parsing:** Extracts email, phone, candidate names, and 30+ core technical skills.
- **TF-IDF & Cosine Similarity Scoring:** Measures content relevance between candidate backgrounds and target job specifications.
- **Match Verdicts:** Automatically categorizes applicants into *Strong Match*, *Potential Fit*, or *Review Needed*.
- **Excel Shortlist Export:** Exports ranked tables with scores and extracted skills for hiring managers.

---

## 🚀 Quickstart

### 1. Installation
```bash
git clone https://github.com/sharmika-murugesan/HireIQ-resume-screening.git
cd HireIQ-resume-screening
pip install -r requirements.txt
```

### 2. Run Resume Screening
Place test resumes into `sample_resumes/` and run:
```bash
python app.py
```

---

## 🛠️ Tech Stack

- **NLP & Machine Learning:** Scikit-learn, TF-IDF Vectorizer, Cosine Similarity
- **Data & Parsing:** Pandas, PyMuPDF, Regular Expressions
- **Web App:** Flask

---

## 📄 License
MIT License. Developed by **Sharmika Murugesan** — Available for freelance NLP & AI development projects.
