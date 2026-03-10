# app/providers/gemini_provider.py
import json
import re
from google import genai
from google.genai import types

from app.providers.interfaces.i_ai_provider import IAIProvider
from app.core.config import settings


class GeminiProvider(IAIProvider):

    SYSTEM_PROMPT = """
You are a cinema expert. Return ONLY a valid JSON array with exactly 6 movies.
The movies must be ordered from most recommended to least recommended.
The first is the best match, the last is a wildcard suggestion.

Required format:
[
  {
    "title": "Original movie title",
    "year": 1994,
    "genre": "Genre in the user's language",
    "description": "Brief personalized description in the user's language explaining why this movie matches."
  }
]

Rules:
- Return exactly 6 movies
- Write genre and description in the language specified in the prompt
- Keep the original movie title (do not translate titles)
- No extra text, only the JSON array
"""

    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)

    def get_recommendations(self, prompt: str) -> list[dict]:
        response = self.client.models.generate_content(
            model="gemini-2.0-flash-lite",
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