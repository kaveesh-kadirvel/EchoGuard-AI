# backend/models/claims.py
import re

# ---------------------
# Sentinel: simple category rules
# ---------------------
def classify_claim(text: str) -> str:
    t = text.lower()
    if any(w in t for w in ["cyclone", "storm", "rain", "weather", "imdur"]):
        return "weather"
    if any(w in t for w in ["neet", "exam", "postpon", "result", "entrance"]):
        return "education"
    if any(w in t for w in ["covid", "virus", "disease", "health", "vaccine"]):
        return "health"
    if any(w in t for w in ["train", "metro", "local", "shutdown", "railway"]):
        return "transport"
    return "general"

# ---------------------
# TruthSeeker: very small evidence mapping
# ---------------------
def find_evidence(text: str, claim_type: str):
    # Basic mapping to authoritative domains; can replace with real search later
    mapping = {
        "weather": ["imd.gov.in", "pib.gov.in"],
        "education": ["nta.ac.in"],
        "health": ["mohfw.gov.in"],
        "transport": ["indianrail.gov.in", "m.railways.gov.in"],
        "general": ["pib.gov.in", "reuters.com"]
    }
    # If claim mentions a known source, include it
    found = []
    for domain in mapping.get(claim_type, []):
        found.append({"source": domain, "url": f"https://{domain}"})
    # small heuristic: if dates or numbers are present, add a 'news' placeholder
    if re.search(r"\d{1,2}\s?(am|pm|hours|hrs|today|tomorrow)|\d{4}", text.lower()):
        found.append({"source": "news", "url": "https://news.google.com"})
    return found

# ---------------------
# EchoPulse: sentiment/emotion heuristic
# ---------------------
def analyze_sentiment(text: str) -> str:
    t = text.lower()
    panic_words = ["urgent", "panic", "danger", "alert", "shutdown", "stop", "kill", "dead", "deadly"]
    fear_words = ["worry", "scared", "afraid", "concerned"]
    score = sum(1 for w in panic_words if w in t)
    fscore = sum(1 for w in fear_words if w in t)
    if score >= 2:
        return "panic"
    if score == 1 or fscore >= 1:
        return "fear"
    if any(w in t for w in ["sad", "angry", "hate"]):
        return "anger"
    return "neutral"

# ---------------------
# Nova: verdict and confidence generator (simple rules)
# ---------------------
def generate_verdict(claim: str, claim_type: str, evidence: list, sentiment: str):
    """
    Basic rules:
    - If evidence contains authoritative domains (IMD/nta/mohfw), we mark UNVERIFIED (needs checking)
      with medium confidence.
    - If no evidence found, treat as FAKE with high confidence (for demo).
    These rules are intentionally conservative and easy to replace with RAG+LLM.
    """
    # If we found a gov source -> treat as UNVERIFIED (we still want human check)
    authoritative = {"imd.gov.in", "pib.gov.in", "nta.ac.in", "mohfw.gov.in", "indianrail.gov.in"}
    found_auth = any(ev.get("source") in authoritative for ev in evidence)
    if found_auth:
        status = "UNVERIFIED"
        confidence = 65
    elif len(evidence) > 0:
        status = "UNVERIFIED"
        confidence = 55
    else:
        status = "FAKE"
        confidence = 88

    # adjust confidence slightly based on sentiment (panic -> lower confidence)
    if sentiment == "panic":
        confidence = max(40, confidence - 10)
    summary = f"Summary: claim appears {status.lower()}. Confidence {confidence}%."
    return status, confidence, summary

# ---------------------
# Panic Index: small heuristic mapping
# ---------------------
def compute_panic_index(text: str, sentiment: str, confidence: int):
    # Panic index is a mapping by region in demo form; here we return example for Mumbai & Students
    base = confidence / 100.0
    if "mumbai" in text.lower() or "local" in text.lower():
        return {"mumbai": round(min(1.0, base + (0.2 if sentiment == "panic" else 0)), 2)}
    if "neet" in text.lower() or "exam" in text.lower():
        return {"students": round(min(1.0, base + 0.25), 2)}
    return {"general": round(base, 2)}
