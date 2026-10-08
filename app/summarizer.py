import re


def summarize(text: str, max_sentences: int = 3) -> str:
    """Simple extractive summarizer: score sentences by word frequency."""
    if not text or not text.strip():
        return ""

    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    sentences = [s.strip() for s in sentences if s.strip()]

    if len(sentences) <= max_sentences:
        return " ".join(sentences)

    words = re.findall(r"\b[a-zA-Z']+\b", text.lower())
    freq: dict[str, int] = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1

    scored = []
    for idx, s in enumerate(sentences):
        s_words = re.findall(r"\b[a-zA-Z']+\b", s.lower())
        score = sum(freq.get(w, 0) for w in s_words)
        scored.append((score, idx, s))

    top = sorted(scored, key=lambda x: x[0], reverse=True)[:max_sentences]
    top_sorted = sorted(top, key=lambda x: x[1])
    return " ".join(s for _, _, s in top_sorted)