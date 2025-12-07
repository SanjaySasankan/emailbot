def build_sentiment_prompt(text: str) -> str:
    return f"""
    You are a sentiment analysis engine. Analyze the following email message.

    Return STRICT JSON:
    - sentiment
    - score
    - emotion
    - tone
    - analysis

    Message:
    \"\"\"{text}\"\"\"
    """

def mock_sentiment_analyzer(text: str):
    prompt = build_sentiment_prompt(text)

    # Simple keyword-based mock logic
    text_lower = text.lower()

    if "frustrat" in text_lower or "urgent" in text_lower or "failed" in text_lower:
        sentiment = "negative"
        score = -0.7
        emotion = "frustrated"
        tone = "urgent"
    elif "thank" in text_lower or "excellent" in text_lower:
        sentiment = "positive"
        score = 0.7
        emotion = "happy"
        tone = "polite"
    else:
        sentiment = "neutral"
        score = 0.0
        emotion = "calm"
        tone = "neutral"

    return {
        "model": "mock-gpt-sentiment",
        "prompt_used": prompt.strip(),
        "sentiment": sentiment,
        "score": score,
        "emotion": emotion,
        "tone": tone,
        "analysis": "Mock output: sentiment determined by keywords."
    }
