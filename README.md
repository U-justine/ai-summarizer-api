# US8 — Docker

## What we did
Put the whole app in a box (a Docker image) so it runs the same
way on any computer — Windows, Mac, Linux, your laptop, or a server.

## Files
- Dockerfile — the recipe
- .dockerignore — files to skip
- README.md — updated instructions

## How to use
    docker build -t ai-summarizer-api .
    docker run -p 8000:8000 ai-summarizer-api

Then open http://127.0.0.1:8000/docs

## Improvement
Before: "works on my machine" — could break on other computers.

After: same app, same behavior, anywhere Docker runs.

