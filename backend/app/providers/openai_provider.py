# app/providers/openai_provider.py
import json
from openai import OpenAI

from app.core.config import settings
from app.providers.interfaces.i_ai_provider import IAIProvider


class OpenAIProvider(IAIProvider):

    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model  = "gpt-4o-mini"

    def get_recommendations(self, prompt: str) -> list[dict]:
        system_prompt = """
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

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": prompt},
            ],
            temperature=0.8,
        )

        content = response.choices[0].message.content
        return json.loads(content)

    def stream_recommendations(self, prompt: str):
        result = self.get_recommendations(prompt)
        yield json.dumps(result)
