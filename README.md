# US2 — Input Validation

## What we did
The app now rejects bad input with a clear message.

Rules:
- Empty text → error 400, says "empty_input"
- Only spaces → error 400, says "empty_input"
- Over 5000 characters → error 400, says "input_too_long"
- Missing field → error 422
- Wrong type (a number instead of text) → error 422

## Files
- app/main.py — added the rules
- tests/test_validation.py — 7 tests

## Improvement
Before: the app accepted empty text silently.
After: it tells you exactly what's wrong.
