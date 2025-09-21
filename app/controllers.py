# app/controllers.py
from fastapi import APIRouter, HTTPException
from app.schemas import AnalyzeRequest, AnalyzeResponse
from domain.facts import FactsBuilder
from services.gemini import GeminiClient

class AnalyzeController:
    def __init__(self, facts_builder: FactsBuilder, gemini: GeminiClient):
        self.facts_builder = facts_builder
        self.gemini = gemini

    def handle(self, req: AnalyzeRequest) -> AnalyzeResponse:
        facts = self.facts_builder.build(
            brand=req.brand,
            product=req.product,
            profile_text=req.profile_text,
            tokens=req.tokens,          # <- using the new field name
        )
        try:
            report = self.gemini.explain(facts)
        except Exception:
            raise HTTPException(status_code=502, detail="Model upstream error")
        return AnalyzeResponse(facts=facts, report=report)

def build_router(controller: AnalyzeController) -> APIRouter:
    router = APIRouter()

    @router.post(
        "/analyze",
        response_model=AnalyzeResponse,
        tags=["Analysis"],
        summary="Analyze cosmetic ingredients for a user profile",
    )
    def analyze(req: AnalyzeRequest):
        return controller.handle(req)

    @router.get("/healthz")
    def health():
        return {"status": "ok", "model": controller.gemini.model}

    return router
