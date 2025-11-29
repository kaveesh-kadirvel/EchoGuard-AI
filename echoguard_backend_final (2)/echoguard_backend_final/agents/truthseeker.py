def find_evidence(claim_type: str):
    sources = {
        "weather": ["imd.gov.in", "pib.gov.in"],
        "education": ["nta.ac.in"],
        "health": ["mohfw.gov.in"],
        "general": ["pib.gov.in"]
    }

    return sources.get(claim_type, [])
