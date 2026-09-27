# Security Policy: HireIQ-resume-screening

## 1. Supported Versions
| Version | Supported          |
| ------- | ------------------ |
| 2.0.x   | :white_check_mark: |
| < 2.0   | :x:                |

## 2. Threat Model & Mitigations

### Candidate PII Protection & Blind Review Compliance
- **PII Scrubbing:** HireIQ features a cryptographic Blind Review mode that transforms real identities into deterministic anonymous tokens (`Candidate #XXXX`) while redacting emails, phone numbers, and physical addresses during initial evaluation.
- **GDPR / CCPA Data Ephemerality:** Resume files uploaded for screening are parsed in memory and not stored indefinitely without recruiter consent.

### Algorithmic Fairness & Ethical AI Safeguards
- **Assistive Framing:** The system is explicitly configured as an assistive recommendation tool. Scoring weights (Skills 40%, Experience 25%, Education 15%, Semantic Fit 20%) are fully transparent, inspectable, and auditable to prevent discriminatory bias.
- **Anti-Keyword Stuffing Normalization:** Match ratios are bounded and normalized against total required criteria rather than rewarding repetitive keyword stuffing.

## 3. Reporting a Vulnerability
To report a security vulnerability or candidate privacy concern, please contact `sharmika.murugesan@gmail.com`. Disclosures are acknowledged within 24 hours.
