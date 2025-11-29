from fastapi import APIRouter
from pydantic import BaseModel
from supabase_client import supabase

from agents.sentinel import classify_claim
from agents.truthseeker import find_evidence
from agents.echopulse import analyze_sentiment
from agents.nova import generate_verdict

router = APIRouter(prefix="/analysis", tags=["Analysis"])

def save_claim_text(text: str):
    try:
        if supabase:
            supabase.table("claims").insert({"text": text}).execute()
    except Exception as e:
        print("❌ Error saving claim:", e)

class ClaimRequest(BaseModel):
    text: str

@router.post("/process_claim")
def process_claim(req: ClaimRequest):

    claim = req.text.strip()

    save_claim_text(claim)

    # Agent pipeline
    claim_type = classify_claim(claim)
    evidence = find_evidence(claim, claim_type)
    sentiment = analyze_sentiment(claim)
    status, confidence, summary, panic_index = generate_verdict(
        claim, claim_type, evidence, sentiment
    )

    result = {
        "claim": claim,
        "type": claim_type,
        "status": status,
        "confidence": confidence,
        "evidence": evidence,
        "sentiment": sentiment,
        "summary": summary,
        "panic_index": panic_index,
        "risk": round(confidence / 100, 2)
    }

    # Save to DB
    try:
        if supabase:
            supabase.table("verified_results").insert(result).execute()
    except Exception as e:
        print("DB Insert Error:", e)

    return result


