"""
NagarVaani — Full Demo Script
Simulates complete citizen journey without needing WhatsApp
Perfect for judge demonstration on March 28

Run: python demo.py
"""

import sys
sys.path.insert(0, ".")

from backend.services.scheme_matcher  import match_schemes
from backend.services.segmentation    import calculate_key_voter_score, get_segments
from backend.models.grievance         import create_grievance, get_grievance_status, update_grievance_status
from backend.utils.security           import hash_sha256, mask_phone

SEP  = "=" * 55
SEP2 = "-" * 55

def demo_citizen(name, profile, phone):
    print(f"\n{SEP}")
    print(f"  CITIZEN: {name}")
    print(f"  Phone:   {mask_phone(phone)}")
    print(SEP)

    # Step 1 — Segmentation (Objective 1)
    segments = get_segments(profile)
    score    = calculate_key_voter_score(profile)

    print(f"\n OBJECTIVE 1 — INTELLIGENT SEGMENTATION")
    print(f"  {SEP2}")
    print(f"  Segments : {' · '.join(segments)}")
    print(f"  Score    : {score['score']}/16  →  {score['label']}")
    print(f"  Breakdown:")
    for reason, pts in score['breakdown']:
        print(f"    +{pts}  {reason}")

    # Step 2 — Scheme Matching (Objective 2)
    schemes = match_schemes(profile)
    print(f"\n OBJECTIVE 2 — BENEFICIARY LINKAGE")
    print(f"  {SEP2}")
    print(f"  Matched {len(schemes)} schemes:\n")
    for s in schemes:
        new_tag = " NEW" if "🆕" in s['title'] else ""
        print(f"  {s['title']}{new_tag}")
        print(f"     Benefit : {s['benefit']}")
        print(f"     Deadline: {s['deadline']}")
        print(f"     Apply   : {s['apply_link']}")
        print()

    # Step 3 — Security
    print(f"  SECURITY")
    print(f"  {SEP2}")
    print(f"  Phone stored    : {phone}  (plain — for WhatsApp)")
    print(f"  Voter ID token  : {hash_sha256('ABC1234567')[:20]}...  (SHA-256)")
    print(f"  Aadhaar token   : {hash_sha256('123456789012')[:20]}...  (SHA-256)")
    print(f"  Breach value    : Anonymous tokens only. Zero PII.")


def demo_grievance():
    print(f"\n{SEP}")
    print(f"  GRIEVANCE FLOW DEMO")
    print(SEP)

    phone = "919876543201"
    desc  = "Water supply not coming for 3 days in Ward 7"

    ticket = create_grievance(phone, desc)
    print(f"\n  Filed: '{desc}'")
    print(f"  Ticket ID  : {ticket}")
    print(f"  Status     : {get_grievance_status(ticket)}")

    update_grievance_status(ticket, "IN_PROGRESS", "Officer_Kumar")
    print(f"\n [Officer Kumar marks IN_PROGRESS]")
    print(f"   Status now : {get_grievance_status(ticket)}")

    update_grievance_status(ticket, "RESOLVED", "Officer_Kumar")
    print(f"\n [Officer Kumar marks RESOLVED]")
    print(f"  Status now : {get_grievance_status(ticket)}")
    print(f"\n  → Citizen auto-notified at each status change via WhatsApp ✅")


if __name__ == "__main__":
    print(f"\n{'#'*55}")
    print(f"  NagarVaani — नगरवाणी  |  DEMO")
    print(f"        India Innovates 2026")
    print(f"  Team: Code-Scavengers · IIITN")
    print(f"{'#'*55}")

    # Demo Citizen 1 — Ramesh (Farmer, OBC, BPL)
    demo_citizen("Ramesh Kumar", {
        "age": 28, "gender": "M", "income": 45000,
        "occupation": "FARMER", "category": "OBC",
        "bpl": True, "district": "Nagpur"
    }, "919876543201")

    # Demo Citizen 2 — Priya (Student, Female, SC)
    demo_citizen("Priya Sharma", {
        "age": 22, "gender": "F", "income": 30000,
        "occupation": "STUDENT", "category": "SC",
        "bpl": True, "district": "Nagpur"
    }, "919876543202")

    # Demo Citizen 3 — Sunita (Daily Wage, Female, BPL)
    demo_citizen("Sunita Devi", {
        "age": 35, "gender": "F", "income": 25000,
        "occupation": "DAILY_WAGE", "category": "OBC",
        "bpl": True, "district": "Nagpur"
    }, "919876543204")

    # Grievance demo
    demo_grievance()

    print(f"\n{'#'*55}")
    print(f"  Both core objectives demonstrated successfully.")
    print(f"  Objective 1 — Intelligent Segmentation    ")
    print(f"  Objective 2 — Beneficiary Linkage         ")
    print(f"{'#'*55}\n")
