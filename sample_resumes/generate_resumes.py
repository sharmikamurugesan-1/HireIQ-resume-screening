import os

def create_sample_resumes(directory: str = "sample_resumes"):
    os.makedirs(directory, exist_ok=True)
    
    samples = [
        ("resume_alex_chen_ai_engineer.txt", """Alex Chen
Email: alex.chen@example.com | Phone: +1-555-0192
Senior Python & AI Engineer with 5+ years of experience building production NLP models, FastAPI backends, and RAG architectures.

Core Skills:
- Python, FastAPI, Docker, RAG, FAISS, LangChain, PyTorch, Scikit-learn, PostgreSQL, REST API.
Experience:
- Architected vector search retrieval pipeline serving 100k queries/day with FAISS and Python.
- Built scalable FastAPI microservices with Docker deployment on AWS.
Education:
- B.S. in Computer Science
"""),
        ("resume_priya_sharma_data_analyst.txt", """Priya Sharma
Email: priya.s@example.com | Phone: +91-98765-43210
Data Analyst with 3 years of experience in business reporting, SQL, and data visualization.

Core Skills:
- Python, Pandas, NumPy, Power BI, Tableau, SQL, SQLite, Excel, Matplotlib.
Experience:
- Automated weekly executive reports reducing processing time by 80% using Pandas and Python.
- Designed interactive Power BI dashboards tracking monthly revenue KPIs.
Education:
- B.Tech in Artificial Intelligence & Data Science
"""),
        ("resume_marcus_devops.txt", """Marcus Brody
Email: marcus.b@example.com | Phone: +1-555-0982
Cloud & Site Reliability Engineer with 4 years of experience.

Core Skills:
- Docker, Kubernetes, AWS, Terraform, Linux, Git, Bash, CI/CD, Python scripting.
Experience:
- Automated infrastructure provisioning using Terraform and Docker.
Education:
- B.S. in Information Technology
""")
    ]
    
    for filename, content in samples:
        path = os.path.join(directory, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

if __name__ == "__main__":
    create_sample_resumes()
