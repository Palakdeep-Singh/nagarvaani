from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import webhook, schemes, grievance

app = FastAPI(
    title="NagarVaani API",
    description="AI-Driven Booth Management System — India Innovates 2026",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(webhook.router,   prefix="/webhook",   tags=["WhatsApp Webhook"])
app.include_router(schemes.router,   prefix="/schemes",   tags=["Scheme Matching"])
app.include_router(grievance.router, prefix="/grievance", tags=["Grievance Tracking"])

@app.get("/")
def root():
    return {
        "project": "NagarVaani — नगरवाणी",
        "tagline": "Every Citizen Heard. Every Vote Counted. Every Scheme Delivered.",
        "event": "India Innovates 2026 · Bharat Mandapam",
        "team": "Code-Scavengers · IIITN",
        "status": "live"
    }

@app.get("/health")
def health():
    return {"status": "ok"}
