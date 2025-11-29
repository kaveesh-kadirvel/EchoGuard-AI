def generate_verdict(claim, claim_type, evidence, sentiment):

    if evidence:
        status = "UNVERIFIED"
        confidence = 65
    else:
        status = "FAKE"
        confidence = 85

    if sentiment == "panic":
        confidence -= 10

    panic_index = {
        "mumbai": round(confidence / 100, 2)
    }

    summary = f"The claim '{claim}' appears {status.lower()}."

    return status, confidence, summary, panic_index
