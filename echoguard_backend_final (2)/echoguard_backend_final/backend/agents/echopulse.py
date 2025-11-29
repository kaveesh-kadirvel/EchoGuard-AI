def analyze_sentiment(text: str):

    panic_words = ["urgent", "panic", "danger", "alert", "shutdown"]
    fear_words = ["worry", "fear", "scared"]

    t = text.lower()
    if any(w in t for w in panic_words):
        return "panic"
    if any(w in t for w in fear_words):
        return "fear"
    return "neutral"
