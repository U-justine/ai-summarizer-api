# US4 — CI Pipeline

## What we did
Set up GitHub Actions so every push runs our tests automatically.

Every time you push code:
1. GitHub starts a fresh Linux machine
2. Installs the app's dependencies
3. Runs all 19 tests
4. Shows ✅ if they pass, ❌ if they fail

## File
- .github/workflows/ci.yml

## See it in action
https://github.com/U-justine/ai-summarizer-api/actions

## Improvement
Before: we had to remember to run tests manually.
After: tests run on every push, no effort needed.
