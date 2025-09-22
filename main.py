from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import init_config
from app.controllers import AnalyzeController, build_router
from domain.facts import FactsBuilder
from services.gemini import GeminiClient

CFG = init_config()

api = FastAPI(title="Cosmetics Advisor (model-driven)", version="1.0.0")

if CFG.cors_allowed_origins:
    api.add_middleware(
        CORSMiddleware,
        allow_origins=CFG.cors_allowed_origins,
        allow_methods=["POST", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization", "X-Request-ID"],
    )

facts_builder = FactsBuilder()
gemini = GeminiClient(
    model=CFG.model,
    max_retries=CFG.max_retries,
    backoff_s=CFG.retry_backoff_s,
)
controller = AnalyzeController(facts_builder, gemini)
api.include_router(build_router(controller))
