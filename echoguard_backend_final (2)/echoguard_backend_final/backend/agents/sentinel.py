def classify_claim(text: str) -> str:
    t = text.lower()

    if any(w in t for w in ["cyclone", "storm", "rain", "weather"]):
        return "weather"

    if any(w in t for w in ["neet", "exam", "result", "postpone"]):
        return "education"

    if any(w in t for w in ["covid", "virus", "disease"]):
        return "health"

    if any(w in t for w in ["train", "metro", "local"]):
        return "transport"

    return "general"
