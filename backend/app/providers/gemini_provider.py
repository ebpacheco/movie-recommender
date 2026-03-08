import json
import re
from google import genai

from app.providers.interfaces.i_ai_provider import IAIProvider
from app.core.config import settings


class GeminiProvider(IAIProvider):

    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)

    def get_recommendations(self, prompt: str) -> list[dict]:
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt + "\n\nResponda APENAS com JSON válido."
        )

        text = response.text.strip()

        # Remove markdown se vier
        if text.startswith("```"):
            text = text.replace("```json", "").replace("```", "").strip()

        # Extrai somente a lista JSON
        match = re.search(r"\[.*\]", text, re.DOTALL)
        if match:
            text = match.group(0)

        return json.loads(text)