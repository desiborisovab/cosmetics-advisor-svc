# app/schemas.py
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, model_validator
import re

SEPARATORS = r"[,\n;/]"      # split on commas, newlines, semicolons, slashes
MAX_INGREDIENTS = 256

class AnalyzeRequest(BaseModel):
    # Single input field your UI sends
    inci: str = Field(..., description="Raw INCI label string, e.g. 'Water, Niacinamide, Fragrance'")
    profile_text: str = Field(..., description="e.g., 'dry skin, acne'")
    brand: Optional[str] = ""
    product: Optional[str] = ""

    # Internal, derived list (kept out of OpenAPI/response)
    tokens: List[str] = Field(default_factory=list, exclude=True)

    @model_validator(mode="after")
    def _normalize(self):
        if not self.inci or not self.inci.strip():
            raise ValueError("inci must not be empty")

        # Split, trim, drop empties
        raw_parts = re.split(SEPARATORS, self.inci)
        toks = [t.strip() for t in raw_parts if t and t.strip()]

        if not toks:
            raise ValueError("No recognizable ingredients parsed from 'inci'.")

        if len(toks) > MAX_INGREDIENTS:
            raise ValueError(f"Too many ingredients (>{MAX_INGREDIENTS}).")

        self.tokens = toks
        return self
class AnalyzeResponse(BaseModel):
    facts: Dict[str, Any]
    report: str
