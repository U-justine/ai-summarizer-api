# US1 — Summarization

## What we did
Built an endpoint that takes long text and gives back a shorter version.

Example:
- Send: "Python is a language. Python is used widely. Python is popular."
- Get back: "Python is a language. Python is used widely."

## How it works
The app counts which words appear most often, then picks the 3 sentences
with the most popular words. That's the summary.

## Files
- app/main.py — the endpoint
- app/summarizer.py — the logic
- tests/test_summarizer.py — 3 tests

## Improvement
Before: no app existed.
After: working endpoint that returns a summary.
