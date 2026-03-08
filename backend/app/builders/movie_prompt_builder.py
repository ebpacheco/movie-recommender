# app/builders/movie_prompt_builder.py
from app.models.profile_model import Profile
from app.builders.interfaces.i_prompt_builder import IPromptBuilder


class MoviePromptBuilder(IPromptBuilder):

    def build(self, profile: Profile, extra_context: str | None = None) -> str:
        parts = ["Recomende 5 filmes para um usuário com as seguintes preferências:"]

        if profile.favorite_genres:
            parts.append(f"- Gêneros favoritos: {', '.join(profile.favorite_genres)}")

        if profile.favorite_movies:
            parts.append(f"- Filmes favoritos: {', '.join(profile.favorite_movies)}")

        if profile.favorite_actors:
            parts.append(f"- Atores favoritos: {', '.join(profile.favorite_actors)}")

        if profile.favorite_directors:
            parts.append(f"- Diretores favoritos: {', '.join(profile.favorite_directors)}")

        if extra_context:
            parts.append(f"- Contexto adicional do usuário: {extra_context}")

        parts.append("Priorize filmes que ainda não estão na lista de favoritos do usuário.")

        # 🔹 Instruções para resposta estruturada
        parts.append("""
Retorne APENAS um JSON válido.

Formato obrigatório:

[
  {
    "title": "Nome do filme",
    "year": 2000,
    "genre": "Gênero principal",
    "description": "Breve descrição do motivo da recomendação"
  }
]

Exemplo de resposta:

[
  {
    "title": "Interstellar",
    "year": 2014,
    "genre": "Sci-Fi",
    "description": "Explora conceitos científicos profundos e viagens espaciais."
  }
]

Regras:
- Retorne exatamente 5 filmes
- Não inclua explicações
- Não use ```json ou markdown
""")

        return "\n".join(parts)