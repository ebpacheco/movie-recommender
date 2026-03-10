# app/services/translation_service.py
import json
import re
from google import genai
from google.genai import types

from app.core.config import settings
from app.schemas.translation_schema import MovieToTranslate

LANGUAGE_NAMES = {
    'pt': 'português brasileiro',
    'en': 'English',
    'es': 'español',
}

SYSTEM_PROMPT = """
You are a cinema expert. Given a list of movies, return ONLY a valid JSON array
with a personalized description and translated genre for each movie.

Keep the exact same order and same titles as received.
Write description and genre in the language specified in the prompt.

Required format:
[
  {
    "title": "Exact same title as received",
    "year": 1994,
    "genre": "Genre in requested language",
    "description": "Brief description of why this movie is worth watching, in the requested language."
  }
]

Rules:
- Same number of movies as input, same order
- Do NOT translate or change the title
- No extra text, only the JSON array
"""


class TranslationService:

    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)

    def translate(self, movies: list[MovieToTranslate], language: str) -> list[dict]:
        lang_name = LANGUAGE_NAMES.get(language, 'português brasileiro')

        movies_list = "\n".join(
            f'- "{m.title}" ({m.year or "?"}) — genre: {m.genre or "unknown"}'
            for m in movies
        )

        prompt = (
            f"Translate the descriptions and genres of the following movies to {lang_name}.\n\n"
            f"{movies_list}"
        )

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.4,
            )
        )

        text = response.text.strip()

        if text.startswith("```"):
            text = text.replace("```json", "").replace("```", "").strip()

        match = re.search(r"\[.*\]", text, re.DOTALL)
        if match:
            text = match.group(0)

        return json.loads(text)