# AI Summarizer API

I built a small REST API that takes text and returns a short summary.
This project was made for the Amalitech Agile & DevOps assessment.

---

## Why I built this

I wanted to build something small but complete — an API that turns long
text into a short summary. The goal wasn't to build a big product. The goal
was to show how I work: planning in sprints, writing tests, setting up CI,
and packaging for deployment.

---

## What I used

- Python 3.11+
- FastAPI + Pydantic + uvicorn
- pytest + httpx for tests
- GitHub Actions for CI
- Docker for packaging

---

## My backlog

I planned 8 user stories across 2 sprints (24 points total).

| ID    | Story                        | Type    | Pts | Priority | Sprint |
|-------|------------------------------|---------|-----|----------|--------|
| US1   | AI Text Summarization        | User    | 5   | Highest  | 1      |
| US2   | Input Validation             | User    | 3   | High     | 1      |
| US3   | Automated Tests              | Enabler | 3   | High     | 1      |
| US4   | CI Pipeline                  | Enabler | 3   | High     | 1      |
| US5   | Health Endpoint              | Enabler | 2   | Medium   | 2      |
| US6   | Application Logging          | Enabler | 3   | Medium   | 2      |
| US7   | Clear Error Messages         | User    | 2   | Medium   | 2      |
| US8   | Docker & Deployment          | Infra   | 3   | Low      | 2      |
|       | **Total**                    |         |**24**|         |        |

---

## How I split the work

### Sprint 1 — Core API & CI (14 points)

My goal for Sprint 1 was to get a working `/summarize` endpoint with
validation, tests, and a CI pipeline.

- US1 — AI Text Summarization (5)
- US2 — Input Validation (3)
- US3 — Automated Tests (3)
- US4 — CI Pipeline (3)

### Sprint 2 — Monitoring & Deployment (10 points)

My goal for Sprint 2 was to make the app production-ready: health checks,
logging, unified errors, and Docker packaging.

- US5 — Health Endpoint (2)
- US6 — Application Logging (3)
- US7 — Clear Error Messages (2)
- US8 — Docker & Deployment (3)

---

## My definition of Done

I only marked a story as Done when all of these were true:

- Code committed with a `GL-N:` prefix in the message
- Unit tests written and passing
- CI green on the branch
- No secrets committed
- README updated if behavior changed
- Acceptance criteria verified

---

## How to run it locally

    python -m venv .venv
    .venv\Scripts\activate          # Windows
    source .venv/bin/activate       # macOS / Linux

    pip install -r requirements.txt
    uvicorn app.main:app --reload

Then I open http://127.0.0.1:8000/docs to test it.

---

## How to run it with Docker

    docker build -t ai-summarizer-api .
    docker run -p 8000:8000 ai-summarizer-api

Then I open http://127.0.0.1:8000/docs

---

## My endpoints

| Method | Path         | What it does        |
|--------|--------------|---------------------|
| GET    | `/`          | Service info        |
| GET    | `/health`    | Liveness check      |
| POST   | `/summarize` | Summarize text      |

### Example

I send this:

    curl -X POST http://127.0.0.1:8000/summarize \
      -H "Content-Type: application/json" \
      -d "{\"text\": \"Python is a language. Python is used widely. Python is popular.\"}"

I get back:

    {"summary": "Python is a language. Python is used widely."}

### Validation rules I added (US2)

- `text` must be a string → 400 `invalid_input`
- `text` must not be empty or whitespace-only → 400 `empty_input`
- `text` must be at most 5000 characters → 400 `input_too_long`
- Missing `text` field → 422 (Pydantic)
- Wrong type → 422 (Pydantic)

### Error shape I standardized (US7)

All errors now look the same:

    {"error": "...", "detail": "..."}

---

## My tests

    pytest -v

I wrote 19 tests across 5 files — all passing.

| File                     | Tests | What it covers                |
|--------------------------|-------|-------------------------------|
| `test_summarizer.py`     | 3     | Summarizer logic              |
| `test_validation.py`     | 7     | Input validation (400 / 422)  |
| `test_health.py`         | 3     | `/health` endpoint            |
| `test_logging.py`        | 2     | Logging middleware            |
| `test_error_shape.py`    | 4     | Unified error format          |

---

## My CI setup

Every time I push to `main` or a `GL-*` branch, GitHub runs my full test
suite automatically.

- Workflow file: `.github/workflows/ci.yml`
- Runs on: GitHub Actions (Ubuntu + Python 3.11)
- Status: https://github.com/U-justine/ai-summarizer-api/actions

---

## My monitoring setup

- `GET /health` — a small endpoint that tells monitoring tools the app is alive
- A logging middleware that logs every request
- Log format:
  `YYYY-MM-DD HH:MM:SS | INFO | METHOD PATH -> STATUS (ms)`

---

## Project structure

    ai-summarizer-api/
    ├── .github/
    │   └── workflows/
    │       └── ci.yml              # my CI workflow
    ├── app/
    │   ├── __init__.py
    │   ├── main.py                 # FastAPI app + endpoints
    │   └── summarizer.py           # my summarization logic
    ├── docs/                       # per-story documentation
    ├── tests/
    │   ├── __init__.py
    │   ├── README.md
    │   ├── test_error_shape.py
    │   ├── test_health.py
    │   ├── test_logging.py
    │   ├── test_summarizer.py
    │   └── test_validation.py
    ├── .dockerignore
    ├── .gitignore
    ├── Dockerfile
    ├── README.md
    └── requirements.txt

---

## Where to find my work

- GitHub: https://github.com/U-justine/ai-summarizer-api
- Jira board: [https://amali-tech.atlassian.net/jira/software/projects/GL/boards](https://amali-tech.atlassian.net/jira/for-you?tab=workedon)
- Jira list: https://amali-tech.atlassian.net/jira/software/projects/GL/list
- CI runs: https://github.com/U-justine/ai-summarizer-api/actions

---

## Note

This is an internal assessment project for Amalitech Agile & DevOps training.
