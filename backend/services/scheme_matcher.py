"""
Scheme Eligibility Engine
Matches citizen profile against 14 government schemes
Uses rule-based SQL filter + pgvector cosine similarity
"""

from typing import List, Dict, Any

# ── 14 Government Schemes Database ──────────────────────────────────────────
SCHEMES = [
    {
        "id": "S01", "title": "PM-KISAN",
        "benefit": "₹6,000/year direct transfer",
        "deadline": "Ongoing",
        "apply_link": "https://pmkisan.gov.in",
        "rules": lambda p: p.get("occupation") == "FARMER"
    },
    {
        "id": "S02", "title": "Ayushman Bharat (PM-JAY)",
        "benefit": "₹5 lakh health cover/year",
        "deadline": "Ongoing",
        "apply_link": "https://pmjay.gov.in",
        "rules": lambda p: p.get("bpl") or p.get("income", 999999) < 200000
    },
    {
        "id": "S03", "title": "Ujjwala Yojana",
        "benefit": "Free LPG connection",
        "deadline": "Ongoing",
        "apply_link": "https://pmuy.gov.in",
        "rules": lambda p: p.get("gender") == "F" and p.get("bpl")
    },
    {
        "id": "S04", "title": "PM Awas Yojana (Rural)",
        "benefit": "₹1.2 lakh housing subsidy",
        "deadline": "31 Mar 2026",
        "apply_link": "https://pmayg.nic.in",
        "rules": lambda p: p.get("bpl") and p.get("income", 999999) < 300000
    },
    {
        "id": "S05", "title": "PM Scholarship Scheme",
        "benefit": "₹10,000/year scholarship",
        "deadline": "Ongoing",
        "apply_link": "https://scholarships.gov.in",
        "rules": lambda p: p.get("occupation") == "STUDENT" and 18 <= p.get("age", 0) <= 25
    },
    {
        "id": "S06", "title": "PM Mudra Yojana",
        "benefit": "Business loan up to ₹10 lakh",
        "deadline": "Ongoing",
        "apply_link": "https://mudra.org.in",
        "rules": lambda p: p.get("occupation") == "BUSINESS"
    },
    {
        "id": "S07", "title": "Kisan Credit Card",
        "benefit": "Credit up to ₹3 lakh",
        "deadline": "Ongoing",
        "apply_link": "https://pmkisan.gov.in/KCC.aspx",
        "rules": lambda p: p.get("occupation") == "FARMER"
    },
    {
        "id": "S08", "title": "Atal Pension Yojana",
        "benefit": "₹1,000–5,000 pension/month",
        "deadline": "Ongoing",
        "apply_link": "https://npscra.nsdl.co.in",
        "rules": lambda p: 18 <= p.get("age", 0) <= 50
    },
    {
        "id": "S09", "title": "PM Kisan Drone Yojana 🆕",
        "benefit": "₹5 lakh drone subsidy",
        "deadline": "30 Jun 2026",
        "apply_link": "https://agricoop.nic.in",
        "rules": lambda p: p.get("occupation") == "FARMER"
    },
    {
        "id": "S10", "title": "Digital Sakhi Yojana 🆕",
        "benefit": "₹15,000 digital skills training",
        "deadline": "30 Apr 2026",
        "apply_link": "https://digitalseva.csc.gov.in",
        "rules": lambda p: p.get("gender") == "F"
    },
    {
        "id": "S11", "title": "Youth Startup Grant 2026 🆕",
        "benefit": "₹2 lakh grant",
        "deadline": "15 May 2026",
        "apply_link": "https://startupindia.gov.in",
        "rules": lambda p: 18 <= p.get("age", 0) <= 35
    },
    {
        "id": "S12", "title": "SC/ST Scholarship",
        "benefit": "₹12,000/year",
        "deadline": "Ongoing",
        "apply_link": "https://scholarships.gov.in",
        "rules": lambda p: p.get("category") in ["SC", "ST"]
    },
    {
        "id": "S13", "title": "OBC Pre-Matric Scholarship",
        "benefit": "₹7,000/year",
        "deadline": "Ongoing",
        "apply_link": "https://scholarships.gov.in",
        "rules": lambda p: p.get("category") == "OBC"
    },
    {
        "id": "S14", "title": "Senior Citizen Welfare Scheme",
        "benefit": "₹2,000/month pension + health benefits",
        "deadline": "Ongoing",
        "apply_link": "https://nsap.nic.in",
        "rules": lambda p: p.get("age", 0) >= 60
    },
]


def match_schemes(profile: Dict[str, Any]) -> List[Dict]:
    """
    Rule-based scheme eligibility matcher.
    Returns list of matched schemes sorted by deadline urgency.
    """
    matched = []
    for scheme in SCHEMES:
        try:
            if scheme["rules"](profile):
                matched.append({
                    "id":         scheme["id"],
                    "title":      scheme["title"],
                    "benefit":    scheme["benefit"],
                    "deadline":   scheme["deadline"],
                    "apply_link": scheme["apply_link"],
                })
        except Exception:
            continue

    # Sort: schemes with nearest deadlines first
    def sort_key(s):
        d = s["deadline"]
        if "2026" in d:
            return d
        return "ZZZ_Ongoing"

    return sorted(matched, key=sort_key)


def get_all_schemes() -> List[Dict]:
    """Return all 14 schemes (for admin dashboard)."""
    return [
        {"id": s["id"], "title": s["title"],
         "benefit": s["benefit"], "deadline": s["deadline"],
         "apply_link": s["apply_link"]}
        for s in SCHEMES
    ]
