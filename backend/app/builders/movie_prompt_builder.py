# app/builders/movie_prompt_builder.py
from app.models.profile_model import Profile
from app.builders.interfaces.i_prompt_builder import IPromptBuilder


LANGUAGE_NAMES = {
    'pt': 'português brasileiro',
    'en': 'English',
    'es': 'español',
}


class MoviePromptBuilder(IPromptBuilder):

    def build(
        self,
        profile:       Profile,
        extra_context: str | None = None,
        language:      str = 'pt',
    ) -> str:
        lang_name = LANGUAGE_NAMES.get(language, 'português brasileiro')

        parts = [f"Recomende 6 filmes para um usuário com as seguintes preferências:"]

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

        parts.append(f"""
IMPORTANTE: Escreva o campo "description" de cada filme em {lang_name}.
O campo "title" deve ser o título original do filme (em inglês ou no idioma original).
O campo "genre" deve ser escrito em {lang_name}.

Retorne APENAS um JSON válido com exatamente 6 filmes, ordenados do mais recomendado para o menos.

Formato obrigatório:

[
  {{
    "title": "Nome original do filme",
    "year": 2000,
    "genre": "Gênero principal",
    "description": "Breve descrição do motivo da recomendação"
  }}
]

Regras:
- Retorne exatamente 6 filmes
- Não inclua explicações fora do JSON
- Não use ```json ou markdown
""")

        return "\n".join(parts)