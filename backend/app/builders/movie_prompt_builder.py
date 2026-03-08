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

        return "\n".join(parts)
