def generate_verdict(claim: str, claim_type: str, evidence: list, sentiment: str):
    
    if len(evidence) > 0:
        status = "UNVERIFIED"
        confidence = 60
    else:
        status = "FAKE"
        confidence = 85

    summary = f"The claim '{claim}' appears {status.lower()} based on available sources."
    
    return status, confidence, summary
