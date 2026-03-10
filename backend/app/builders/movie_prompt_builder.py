# app/builders/movie_prompt_builder.py
from app.models.profile_model import Profile
from app.builders.interfaces.i_prompt_builder import IPromptBuilder


LANGUAGE_NAMES = {
    'pt': 'português brasileiro',
    'en': 'English',
    'es': 'español',
}

# Limites máximos usados na construção do prompt
PROMPT_LIMITS = {
    'genres':    3,
    'movies':    3,
    'actors':    5,
    'directors': 3,
}


class MoviePromptBuilder(IPromptBuilder):

    def build(
        self,
        profile:       Profile,
        extra_context: str | None = None,
        language:      str = 'pt',
    ) -> str:
        lang_name = LANGUAGE_NAMES.get(language, 'português brasileiro')

        # Aplica limites defensivamente
        # Suporta tanto strings simples quanto objetos {name, id, image} do autocomplete
        def names(lst, limit):
            items = (lst or [])[:limit]
            return [i['name'] if isinstance(i, dict) else i for i in items]

        genres    = names(profile.favorite_genres,    PROMPT_LIMITS['genres'])
        movies    = names(profile.favorite_movies,    PROMPT_LIMITS['movies'])
        actors    = names(profile.favorite_actors,    PROMPT_LIMITS['actors'])
        directors = names(profile.favorite_directors, PROMPT_LIMITS['directors'])

        parts = ["Recomende 6 filmes para um usuário com as seguintes preferências:"]

        if genres:
            parts.append(f"- Gêneros favoritos: {', '.join(genres)}")

        if movies:
            parts.append(f"- Filmes favoritos (use como referência de estilo/gosto, NÃO os inclua na lista): {', '.join(movies)}")

        if actors:
            parts.append(f"- Atores favoritos: {', '.join(actors)}")

        if directors:
            parts.append(f"- Diretores favoritos: {', '.join(directors)}")

        if not any([genres, movies, actors, directors]):
            parts.append("- Sem preferências específicas: recomende filmes variados e populares")

        if extra_context:
            parts.append(f"- Pedido específico do usuário: {extra_context}")

        if movies:
            parts.append("- NÃO repita os filmes favoritos listados acima na recomendação")

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