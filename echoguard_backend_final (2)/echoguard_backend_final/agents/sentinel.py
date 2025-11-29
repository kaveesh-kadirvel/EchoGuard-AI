def classify_claim(text: str):
    text_lower = text.lower()

    if "cyclone" in text or "rain" in text or "storm" in text:
        return "weather"
    if "neet" in text or "exam" in text or "result" in text:
        return "education"
    if "covid" in text or "virus" in text:
        return "health"
    
    return "general"
