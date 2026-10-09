# Test Suite

Two test files cover all functionality of the AI Summarizer API.

## `test_summarizer.py` (3 tests) — US1

Tests the core summarization logic in `app/summarizer.py`.

- `test_returns_short_text_unchanged` — input with ≤3 sentences is returned unchanged
- `test_summarizes_longer_text` — input with >3 sentences is reduced
- `test_empty_text_returns_empty_string` — empty or whitespace input returns `""`

## `test_validation.py` (7 tests) — US2

Tests the input validation in `app/main.py`.

- `test_valid_input_returns_200` — happy path returns 200 with a summary
- `test_empty_string_returns_400` — empty text rejected with `empty_input`
- `test_whitespace_only_returns_400` — whitespace rejected with `empty_input`
- `test_missing_text_field_returns_422` — Pydantic rejects missing field
- `test_non_string_text_returns_422` — Pydantic rejects non-string type
- `test_over_length_returns_400` — text >5000 chars rejected with `input_too_long`
- `test_exactly_max_length_returns_200` — boundary case at 5000 chars passes

## How to run

    pytest -v

All 10 tests should pass in under 1 second.

## Test strategy

- **Unit-level:** `test_summarizer.py` calls the `summarize()` function directly.
- **Integration-level:** `test_validation.py` uses FastAPI's `TestClient` to
  exercise the full HTTP stack (routing → validation → response).