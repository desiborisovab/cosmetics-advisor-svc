# Create a README.md file for the user's project and save it for download

readme = r"""# Cosmetics Advisor (FastAPI + Google Gemini)

A small, production-minded FastAPI service that takes a single **INCI** text input (ingredient label) plus a **user skin profile**, sends a cleanly-structured prompt to **Google Gemini**, and returns a human-readable analysis.

The design is intentionally traditional: clear separation of **app** (HTTP/controllers/schemas), **domain** (core logic/data shaping), **services** (external I/O), and **configs** (YAML-based runtime settings). No hardcoded domain rules; the model does the reasoning.

---

## Table of Contents
- [Features](#features)
- [Architecture](#architecture)
- [Directory Layout](#directory-layout)
- [Prerequisites](#prerequisites)
- [Setup & Run](#setup--run)
- [Configuration](#configuration)
- [Environment Variables](#environment-variables)
- [API](#api)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Notes on Production](#notes-on-production)
- [License](#license)

---

## Features

- **Single input**: one text field `inci` (e.g., `"Water, Niacinamide, Fragrance"`).  
- **Model-driven**: Gemini provides explanations, cautions, and overall advice.  
- **Clean validation**: Pydantic v2 validates & normalizes inputs (splits, trims, caps size).  
- **OpenAPI docs**: Auto-generated Swagger UI and ReDoc.  
- **Config-first**: model name, retries, CORS, and logging controlled via YAML.  
- **Gemini Key**: reads Gemini key from environment.  
- **CORS-ready**: for browser clients during local dev or hosted front-ends.  

---

## Architecture

**Flow**  
1. Client calls `POST /analyze` with JSON containing `inci`, `profile_text`, and optional `brand`/`product`.  
2. Pydantic model splits/cleans the `inci` string into an internal list `tokens`.  
3. Controller builds a minimal `facts` dict (brand/product/profile/ingredients).  
4. `GeminiClient.explain(facts)` sends a single-prompt request to Gemini.  
5. Response returns `{ "facts": {...}, "report": "..." }` to the client.

**Key idea**: the service is **data-agnostic**—no synonym maps, no rule files. All domain knowledge is delegated to Gemini.

---

## Directory Layout

