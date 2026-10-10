# US3 — Automated Tests

## What we did
Wrote 19 tests that check the app works.
They run in under 1 second and catch bugs automatically.

## Test files
- test_summarizer.py (3 tests)
- test_validation.py (7 tests)
- test_health.py (3 tests)
- test_logging.py (2 tests)
- test_error_shape.py (4 tests)

## How to run
    pytest -v

## Improvement
Before: we tested by hand (slow, easy to forget).
After: one command runs all checks in 1 second.
