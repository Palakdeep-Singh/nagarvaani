from fastapi import APIRouter
from backend.services.scheme_matcher import get_all_schemes, match_schemes
from backend.services.segmentation import calculate_key_voter_score
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class Profile(BaseModel):
    age: int
    gender: str          # M / F / O
    income: int
    occupation: str      # FARMER / STUDENT / BUSINESS / DAILY_WAGE / OTHER
    category: str        # GEN / OBC / SC / ST
    bpl: bool
    district: Optional[str] = ""

@router.get("/all")
def all_schemes():
    return get_all_schemes()

@router.post("/match")
def match(profile: Profile):
    p = profile.dict()
    return {
        "schemes":    match_schemes(p),
        "segmentation": calculate_key_voter_score(p)
    }
