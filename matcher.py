"""
HireIQ — Multi-Criteria Candidate Matcher & Gap Analyzer
Implements transparent 4-pillar scoring summing to 100%:
1. Required Skills Match: 40%
2. Experience Tenure: 25%
3. Education / Credentials: 15%
4. Semantic Context Fit: 20%
Includes skill-gap decomposition and ethical assistive guardrails.
"""

import re
from typing import List, Dict, Any, Optional

ETHICAL_DISCLAIMER = (
    "ASSISTIVE DECISION SUPPORT: HireIQ provides objective criteria matching to reduce initial screening friction. "
    "Scores are assistive recommendations and must NEVER replace human judgment, structured interviews, and holistic candidate review."
)

class JobMatcher:
    def __init__(self, job_title: str, required_skills: List[str], min_years_exp: int = 3,
                 preferred_education: str = "B.Tech / Bachelor's in CS or related field"):
        self.job_title = job_title
        self.required_skills = [s.strip().title() for s in required_skills if s.strip()]
        self.min_years_exp = max(1, min_years_exp)
        self.preferred_education = preferred_education

    def score_candidate(self, candidate: Dict[str, Any]) -> Dict[str, Any]:
        """Calculates transparent multi-criteria breakdown (Total = 100%)."""
        cand_skills = [s.title() for s in candidate.get("skills", [])]
        cand_exp = candidate.get("years_experience", 0)

        # 1. Skills Match (40% Weight)
        matched_skills = [s for s in self.required_skills if any(cs.lower() == s.lower() for cs in cand_skills)]
        missing_skills = [s for s in self.required_skills if s not in matched_skills]
        bonus_skills = [s for s in cand_skills if not any(rs.lower() == s.lower() for rs in self.required_skills)]

        skills_ratio = len(matched_skills) / len(self.required_skills) if self.required_skills else 1.0
        skills_score = round(skills_ratio * 40.0, 1)

        # 2. Experience Tenure (25% Weight)
        exp_ratio = min(1.0, cand_exp / self.min_years_exp)
        exp_score = round(exp_ratio * 25.0, 1)

        # 3. Education Match (15% Weight)
        cand_edu = candidate.get("education", "")
        edu_score = 15.0 if cand_edu and "Relevant" not in cand_edu else 12.0

        # 4. Semantic Context Fit (20% Weight)
        raw_text = candidate.get("raw_text", "").lower()
        title_words = set(re.findall(r'\b\w{3,}\b', self.job_title.lower()))
        text_words = set(re.findall(r'\b\w{3,}\b', raw_text))
        semantic_ratio = len(title_words.intersection(text_words)) / max(1, len(title_words))
        semantic_score = round(min(1.0, max(0.5, semantic_ratio)) * 20.0, 1)

        total_score = round(skills_score + exp_score + edu_score + semantic_score, 1)

        # Assistive recommendation
        if total_score >= 78.0:
            recommendation = "Strong Candidate for Interview"
        elif total_score >= 55.0:
            recommendation = "Potential Fit (Review Gaps)"
        else:
            recommendation = "Skills Gap Exceeds Threshold"

        return {
            "blind_id": candidate.get("blind_id"),
            "name": candidate.get("name"),
            "email": candidate.get("email"),
            "phone": candidate.get("phone"),
            "years_experience": cand_exp,
            "education": cand_edu,
            "match_score": total_score,
            "recommendation": recommendation,
            "status": candidate.get("status", "NEW"),
            "recruiter_notes": candidate.get("recruiter_notes", ""),
            "score_breakdown": {
                "skills_match": {"score": skills_score, "max": 40.0, "pct": round(skills_ratio * 100, 1)},
                "experience_tenure": {"score": exp_score, "max": 25.0, "pct": round(exp_ratio * 100, 1)},
                "education": {"score": edu_score, "max": 15.0, "pct": round((edu_score / 15.0) * 100, 1)},
                "semantic_fit": {"score": semantic_score, "max": 20.0, "pct": round((semantic_score / 20.0) * 100, 1)}
            },
            "skill_gap_analysis": {
                "matched_skills": matched_skills,
                "missing_critical_skills": missing_skills,
                "bonus_skills": bonus_skills[:6]
            },
            "disclaimer": ETHICAL_DISCLAIMER
        }

    def rank_candidates(self, candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        scored = [self.score_candidate(c) for c in candidates]
        scored.sort(key=lambda x: x["match_score"], reverse=True)
        return scored
