# US5 — Health Check

## What we did
Added a URL that says "yes, I'm running".

    GET /health → {"status": "ok"}

Monitoring tools and servers use this to check if the app is alive.

## Files
- app/main.py — the endpoint
- tests/test_health.py — 3 tests

## Improvement
Before: no way to check if the app was alive from outside.

After: one URL tells you instantly.
