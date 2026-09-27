"""
HireIQ — TF-IDF Matcher & Candidate Ranker
Computes cosine similarity between candidate resumes and target job description.
"""

from typing import List, Dict, Any

class JobMatcher:
    def __init__(self, job_description: str):
        self.job_description = job_description

    def score_candidates(self, candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if not candidates:
            return []

        try:
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.metrics.pairwise import cosine_similarity

            corpus = [self.job_description] + [c["raw_text"] for c in candidates]
            vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
            tfidf_matrix = vectorizer.fit_transform(corpus)

            # Cosine similarity of JD (index 0) against all candidate resumes (1..n)
            sim_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

            ranked = []
            for i, c in enumerate(candidates):
                score_pct = round(float(sim_scores[i]) * 100, 1)
                entry = c.copy()
                del entry["raw_text"]  # Omit large payload from report
                entry["match_score"] = score_pct
                entry["verdict"] = "Strong Match" if score_pct >= 65 else ("Potential Fit" if score_pct >= 40 else "Review Needed")
                ranked.append(entry)

            # Sort descending by match score
            ranked.sort(key=lambda x: x["match_score"], reverse=True)
            return ranked

        except ImportError:
            # Fallback simple keyword overlap scoring
            jd_words = set(self.job_description.lower().split())
            ranked = []
            for c in candidates:
                cand_words = set(c["raw_text"].lower().split())
                overlap = len(jd_words.intersection(cand_words))
                score_pct = round(min((overlap / max(len(jd_words), 1)) * 140, 96.0), 1)
                
                entry = c.copy()
                del entry["raw_text"]
                entry["match_score"] = score_pct
                entry["verdict"] = "Strong Match" if score_pct >= 60 else "Potential Fit"
                ranked.append(entry)

            ranked.sort(key=lambda x: x["match_score"], reverse=True)
            return ranked
