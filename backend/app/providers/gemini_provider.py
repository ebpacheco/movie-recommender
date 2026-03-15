# app/providers/gemini_provider.py
import json
import re
from google import genai
from google.genai import types

from app.providers.interfaces.i_ai_provider import IAIProvider
from app.core.config import settings


class GeminiProvider(IAIProvider):

    SYSTEM_PROMPT = """
You are a cinema expert. Return ONLY a valid JSON object with exactly two fields: "message" and "movies".

Required format:
{
  "message": "A short, empathetic message in the user's language (2-4 sentences)",
  "movies": [
    {
      "title": "Original movie title",
      "year": 1994,
      "genre": "Genre in the user's language",
      "description": "Brief personalized description in the user's language explaining why this movie matches."
    }
  ]
}

Rules:
- Return exactly 10 movies in the "movies" array
- Write message, genre and description in the language specified in the prompt
- Keep the original movie title (do not translate titles)
- No extra text outside the JSON object, no markdown, no ```json
"""

    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)

    def get_recommendations(self, prompt: str) -> dict:
        response = self.client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=self.SYSTEM_PROMPT,
                temperature=0.8,
            )
        )

        text = response.text.strip()

        # Remove markdown code fences se existirem
        if text.startswith("```"):
            text = re.sub(r"^```[a-z]*\n?", "", text)
            text = re.sub(r"\n?```$", "", text)
            text = text.strip()

        # Tenta parsear como objeto {message, movies}
        try:
            parsed = json.loads(text)
            if isinstance(parsed, dict) and "movies" in parsed:
                return parsed
            # Formato legado: array direto
            if isinstance(parsed, list):
                return {"message": None, "movies": parsed}
        except json.JSONDecodeError:
            pass

        # Fallback: extrai objeto JSON do texto
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            try:
                parsed = json.loads(match.group(0))
                if isinstance(parsed, dict):
                    return parsed
            except json.JSONDecodeError:
                pass

        # Último recurso: tenta extrair só o array
        match = re.search(r"\[.*\]", text, re.DOTALL)
        if match:
            return {"message": None, "movies": json.loads(match.group(0))}

        return {"message": None, "movies": []}