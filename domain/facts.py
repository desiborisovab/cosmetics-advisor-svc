from typing import Dict, Any, List, Optional

class FactsBuilder:
    """
    Assembles the minimal 'facts' payload from INPUT ONLY
    """
    def build(self,
              brand: Optional[str],
              product: Optional[str],
              profile_text: str,
              tokens: List[str]) -> Dict[str, Any]:
        return {
            "brand": brand or "",
            "product_name": product or "",
            "profile_text": profile_text,
            "ingredients": [{"input": t} for t in tokens],  # raw as provided
            # Helpful for Gemini: a joined label string as context
            "ingredients_label": ", ".join(tokens),
        }
