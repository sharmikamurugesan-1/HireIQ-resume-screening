"""
HireIQ — REST API Server
Provides endpoints for resume screening, candidate ranking, blind PII anonymization,
status pipeline transitions, and shortlist reports.
"""

from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from parser import ResumeParser
from matcher import JobMatcher

app = Flask(__name__)
CORS(app)

parser = ResumeParser()

# In-memory candidate repository with persistence support
CANDIDATE_STORE = []

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        "status": "online",
        "service": "HireIQ Assistive Screening Engine",
        "version": "2.0.0",
        "capabilities": ["multi_criteria_scoring", "skill_gap_analysis", "pii_anonymization", "pipeline_tracking"]
    })

@app.route('/api/screen', methods=['POST'])
def screen_resumes():
    """Screens candidate resumes against target job specifications."""
    data = request.get_json(force=True) or {}
    job_title = data.get("job_title", "Senior Python & AI Engineer")
    required_skills = data.get("required_skills", ["Python", "FastAPI", "RAG", "Docker", "Git"])
    min_exp = int(data.get("min_years_experience", 3))
    resumes_text = data.get("resumes", [])

    matcher = JobMatcher(job_title=job_title, required_skills=required_skills, min_years_exp=min_exp)
    
    parsed_candidates = []
    for idx, r_text in enumerate(resumes_text):
        cand = parser.parse_text(r_text, filename=f"resume_{idx+1}.txt")
        parsed_candidates.append(cand)

    ranked = matcher.rank_candidates(parsed_candidates)
    
    global CANDIDATE_STORE
    CANDIDATE_STORE = ranked
    
    return jsonify({
        "job_title": job_title,
        "required_skills": required_skills,
        "total_screened": len(ranked),
        "candidates": ranked
    })

@app.route('/api/candidates/<blind_id>/status', methods=['POST'])
def update_candidate_status(blind_id: str):
    """Updates candidate hiring pipeline stage (NEW, UNDER_REVIEW, SHORTLISTED, PASSED)."""
    data = request.get_json(force=True) or {}
    new_status = data.get("status", "UNDER_REVIEW")
    notes = data.get("notes", "")

    for c in CANDIDATE_STORE:
        if c.get("blind_id") == blind_id:
            c["status"] = new_status
            if notes:
                c["recruiter_notes"] = notes
            return jsonify({"success": True, "blind_id": blind_id, "status": new_status})

    return jsonify({"error": "Candidate not found"}), 404

@app.route('/api/export/shortlist', methods=['GET'])
def export_shortlist():
    """Generates a structured recruitment shortlist report."""
    shortlist = [c for c in CANDIDATE_STORE if c.get("status") == "SHORTLISTED"] or CANDIDATE_STORE
    csv_rows = ["Blind_ID,Name,Match_Score,Experience,Matched_Skills,Missing_Skills,Status,Notes"]
    for c in shortlist:
        matched = ";".join(c["skill_gap_analysis"]["matched_skills"])
        missing = ";".join(c["skill_gap_analysis"]["missing_critical_skills"])
        csv_rows.append(f"{c['blind_id']},{c['name']},{c['match_score']}%,{c['years_experience']} yrs,\"{matched}\",\"{missing}\",{c['status']},\"{c['recruiter_notes']}\"")

    return Response("\n".join(csv_rows), mimetype="text/csv", headers={"Content-Disposition": "attachment;filename=hireiq_candidate_shortlist.csv"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004, debug=True)
