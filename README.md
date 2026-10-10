# AI Summarizer API

A small REST API that accepts text and returns a concise summary.

## Overview

This service exposes a `POST /summarize` endpoint that extracts the most important
sentences from the input text using word-frequency scoring.

Built with **FastAPI** and **Python**.

## Requirements

- Python 3.11+
- pip

## Install

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt

## Run with Docker

If you have Docker installed, you can build and run the service as a container.

Build the image:

    docker build -t ai-summarizer-api .

Run the container:

    docker run -p 8000:8000 ai-summarizer-api

Then open http://127.0.0.1:8000/docs in your browser.