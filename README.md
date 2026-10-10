# US7 — Clear Error Messages

## What we did
Made all error responses look the same.

Before (two different shapes):
- 400 → {"detail": {"error": "...", "detail": "..."}}
- 422 → {"detail": [{"loc": [...], "msg": "...", ...}]}

After (one shape for both):
- 400 → {"detail": {"error": "...", "detail": "..."}}
- 422 → {"error": "validation_error", "detail": "..."}

Clients now parse errors the same way.

## Files
- app/main.py — exception handler
- tests/test_error_shape.py — 4 tests

## Improvement
Before: clients had to write two different parsers.

After: one parser handles all errors.
