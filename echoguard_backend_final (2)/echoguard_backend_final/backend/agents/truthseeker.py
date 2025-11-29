def find_evidence(text: str, claim_type: str):
    mapping = {
        "weather": ["imd.gov.in", "pib.gov.in"],
        "education": ["nta.ac.in"],
        "health": ["mohfw.gov.in"],
        "transport": ["indianrail.gov.in"],
        "general": ["pib.gov.in"]
    }

    return [{"source": src, "url": f"https://{src}"} for src in mapping.get(claim_type, [])]
