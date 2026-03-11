from fastapi import APIRouter
from backend.models.grievance import get_all_grievances, update_grievance_status
from pydantic import BaseModel

router = APIRouter()

class StatusUpdate(BaseModel):
    ticket_id: str
    status: str        # OPEN / IN_PROGRESS / RESOLVED
    officer: str = ""

@router.get("/all")
def all_grievances():
    return get_all_grievances()

@router.post("/update")
def update_status(body: StatusUpdate):
    update_grievance_status(body.ticket_id, body.status, body.officer)
    return {"status": "updated", "ticket_id": body.ticket_id}
