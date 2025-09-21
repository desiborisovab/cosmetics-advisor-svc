# services/gemini.py
from google import genai
from google.genai import types

class GeminiClient:
    def __init__(self, model: str, max_retries: int = 2, backoff_s: float = 0.5):
        self.client = genai.Client()
        self.model = model
        self.max_retries = max_retries
        self.backoff_s = backoff_s

    def explain(self, facts: dict) -> str:
        system = (
            "You are a careful cosmetics ingredient advisor. "
            "Explain each ingredient plainly; call out acne triggers, "
            "note suitability for dry/oily/sensitive skin, and suggest safer alternatives."
        )

        # Build the single user prompt string from your facts
        ingredients = ", ".join(i["input"] for i in facts.get("ingredients", []))
        profile = facts.get("profile_text", "")
        brand = facts.get("brand", "")
        product = facts.get("product_name", "")

        prompt = (
            f"Product: {brand} {product}\n"
            f"User profile: {profile}\n"
            f"Ingredients: {ingredients}\n\n"
            "Return a concise, helpful analysis."
        )

        resp = self.client.models.generate_content(
            model=self.model,                 # e.g. "gemini-1.5-flash" or "gemini-2.0-flash"
            contents=prompt,                  # <-- just a string
            config=types.GenerateContentConfig(
                system_instruction=system     # <-- pass system prompt here
            ),
        )
        return resp.text or ""
