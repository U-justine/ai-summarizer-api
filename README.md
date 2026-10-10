# US6 — Logging

## What we did
The app now writes down every request in a diary.

Example line:
    2026-10-09 14:23:01 | INFO | GET /health -> 200 (0.9ms)

This shows: time, method, path, status code, and how long it took.

## Files
- app/main.py — logging setup + middleware
- tests/test_logging.py — 2 tests

## Improvement
Before: the app was silent — no way to see what happened.

After: every request is recorded. If something breaks, you can look back.
