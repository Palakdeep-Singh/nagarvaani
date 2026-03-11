import sys
sys.path.insert(0, ".")

from backend.services.scheme_matcher import match_schemes
from backend.services.segmentation import calculate_key_voter_score

# Test profile — Ramesh, 28yr old farmer, BPL
profile = {
    "age": 28,
    "gender": "M",
    "income": 45000,
    "occupation": "FARMER",
    "category": "OBC",
    "bpl": True,
    "district": "Nagpur"
}

schemes = match_schemes(profile)
score   = calculate_key_voter_score(profile)

print("=" * 45)
print("SCHEME MATCHING — Objective 2")
print("=" * 45)
print(f"Schemes matched: {len(schemes)}\n")
for s in schemes:
    print(f"  ✅ {s['title']}")
    print(f"     Benefit:  {s['benefit']}")
    print(f"     Deadline: {s['deadline']}\n")

print("=" * 45)
print("KEY VOTER SCORING — Objective 1")
print("=" * 45)
print(f"Score:    {score['score']}/16")
print(f"Segments: {', '.join(score['segments'])}")
print(f"Label:    {score['label']}")
print("\nBreakdown:")
for reason, pts in score['breakdown']:
    print(f"  +{pts}  {reason}")
print("=" * 45)
