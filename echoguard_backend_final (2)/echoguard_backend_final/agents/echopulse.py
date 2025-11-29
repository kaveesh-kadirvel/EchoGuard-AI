def analyze_sentiment(text: str):
    panic_words = ["urgent", "scary", "panic", "danger", "alert"]
    score = sum(1 for w in panic_words if w in text.lower())

    if score >= 2:
        return "panic"
    elif score == 1:
        return "fear"
    return "neutral"
