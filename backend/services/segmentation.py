"""
Intelligent Segmentation Engine — Objective 1
Classifies citizens into voter segments and calculates Key Voter Score
"""

from typing import Dict, Any, List


# ── Segment Classification ───────────────────────────────────────────────────

def get_segments(profile: Dict[str, Any]) -> List[str]:
    """Auto-classify citizen into one or more voter segments."""
    segments = []
    age        = profile.get("age", 0)
    gender     = profile.get("gender", "")
    occupation = profile.get("occupation", "")

    if 18 <= age <= 35:
        segments.append("YOUTH")
    if gender == "F":
        segments.append("WOMEN")
    if occupation == "FARMER":
        segments.append("FARMER")
    if occupation == "BUSINESS":
        segments.append("BUSINESSMAN")
    if age >= 60:
        segments.append("SENIOR_CITIZEN")
    if occupation == "DAILY_WAGE":
        segments.append("DAILY_WAGE_WORKER")
    if occupation == "STUDENT":
        segments.append("STUDENT")

    return segments if segments else ["GENERAL"]


# ── Key Voter Score (Max 16 pts) ─────────────────────────────────────────────

def calculate_key_voter_score(profile: Dict[str, Any]) -> Dict:
    """
    Calculate Key Voter Score based on multi-segment overlap,
    economic vulnerability, and demographic factors.
    Score >= 7 → KEY VOTER 🔑
    """
    score    = 0
    breakdown = []
    segments = get_segments(profile)

    age        = profile.get("age", 0)
    gender     = profile.get("gender", "")
    occupation = profile.get("occupation", "")
    bpl        = profile.get("bpl", False)
    income     = profile.get("income", 999999)

    # Segment overlap bonus
    n = len(segments)
    if n >= 3:
        score += 6
        breakdown.append(("Multi-segment (3+)", +6))
    elif n == 2:
        score += 4
        breakdown.append(("Multi-segment (2)", +4))
    elif n == 1:
        score += 1
        breakdown.append(("Single segment", +1))

    # Economic vulnerability
    if bpl and income < 50000:
        score += 5
        breakdown.append(("Antyodaya / BPL + very low income", +5))
    elif bpl:
        score += 3
        breakdown.append(("BPL card holder", +3))

    # Age factors
    if 18 <= age <= 25:
        score += 3
        breakdown.append(("First-time voter age (18–25)", +3))
    elif 26 <= age <= 35:
        score += 2
        breakdown.append(("Youth voter (26–35)", +2))

    # Gender
    if gender == "F":
        score += 2
        breakdown.append(("Female voter", +2))

    # Occupation
    if occupation == "FARMER":
        score += 2
        breakdown.append(("Farmer", +2))
    elif occupation == "DAILY_WAGE":
        score += 3
        breakdown.append(("Daily wage worker", +3))
    elif occupation == "BUSINESS":
        score += 2
        breakdown.append(("Businessperson", +2))

    is_key_voter = score >= 7

    return {
        "segments":     segments,
        "score":        min(score, 16),   # cap at 16
        "is_key_voter": is_key_voter,
        "breakdown":    breakdown,
        "label":        "KEY VOTER 🔑" if is_key_voter else ("HIGH PRIORITY" if score >= 4 else "STANDARD"),
    }


# ── Booth-Level Aggregation (for Admin Dashboard) ────────────────────────────

def booth_segment_summary(citizens: List[Dict]) -> Dict:
    """Aggregate segment data for a booth — used in admin dashboard."""
    summary  = {"YOUTH": 0, "WOMEN": 0, "FARMER": 0, "BUSINESSMAN": 0,
                "SENIOR_CITIZEN": 0, "DAILY_WAGE_WORKER": 0, "STUDENT": 0, "GENERAL": 0}
    key_voters = 0
    total      = len(citizens)

    for c in citizens:
        segs  = get_segments(c)
        score = calculate_key_voter_score(c)
        if score["is_key_voter"]:
            key_voters += 1
        for seg in segs:
            summary[seg] = summary.get(seg, 0) + 1

    return {
        "total":       total,
        "segments":    summary,
        "key_voters":  key_voters,
        "coverage_pct": round((key_voters / total * 100) if total else 0, 1),
    }
