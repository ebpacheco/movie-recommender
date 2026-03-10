# app/providers/gemini_provider.py
import json
import re
from google import genai
from google.genai import types

from app.providers.interfaces.i_ai_provider import IAIProvider
from app.core.config import settings


class GeminiProvider(IAIProvider):

    SYSTEM_PROMPT = """
    Você é um especialista em cinema. Retorne APENAS um JSON válido com uma lista de filmes.
    Formato exato:
    [
      {
        "title": "Nome do Filme",
        "year": 1994,
        "genre": "Drama",
        "description": "Breve descrição personalizada de por que este filme combina com o usuário."
      }
    ]
    Retorne exatamente 5 filmes. Sem texto adicional, apenas o JSON.
    """

    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)

    def get_recommendations(self, prompt: str) -> list[dict]:
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=self.SYSTEM_PROMPT,
                temperature=0.8,
            )
        )

        text = response.text.strip()

        if text.startswith("```"):
            text = text.replace("```json", "").replace("```", "").strip()

        match = re.search(r"\[.*\]", text, re.DOTALL)
        if match:
            text = match.group(0)

        return json.loads(text)