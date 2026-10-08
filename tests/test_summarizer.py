from app.summarizer import summarize


def test_returns_short_text_unchanged():
    text = "One sentence only."
    assert summarize(text) == "One sentence only."


def test_summarizes_longer_text():
    text = (
        "Python is a programming language. "
        "Python is used widely. "
        "Python is great for data. "
        "It is also good for web."
    )
    result = summarize(text, max_sentences=2)
    assert isinstance(result, str)
    assert len(result) > 0


def test_empty_text_returns_empty_string():
    assert summarize("") == ""
    assert summarize("   ") == ""