# app/services/recommendation_service.py
import json
import re
from uuid import UUID
from datetime import timedelta, timezone

from fastapi import HTTPException, status

from app.models.recommendation_model import Recommendation
from app.models.user_model import UserRole
from app.repositories.recommendation_repository import RecommendationRepository
from app.repositories.interfaces.i_user_repository import IProfileRepository
from app.providers.interfaces.i_ai_provider import IAIProvider
from app.builders.interfaces.i_prompt_builder import IPromptBuilder

CACHE_HOURS = 3


class RecommendationService:

    def __init__(
        self,
        profile_repo:        IProfileRepository,
        recommendation_repo: RecommendationRepository,
        ai_provider:         IAIProvider,
        prompt_builder:      IPromptBuilder,
    ):
        self.profile_repo        = profile_repo
        self.recommendation_repo = recommendation_repo
        self.ai_provider         = ai_provider
        self.prompt_builder      = prompt_builder

    def _to_response(self, rec: Recommendation, cached: bool, is_admin: bool = False) -> dict:
        next_at = None if is_admin else rec.created_at.replace(tzinfo=timezone.utc) + timedelta(hours=CACHE_HOURS)
        return {
            "movies":            rec.response,
            "message":           getattr(rec, 'message', None),
            "language":          getattr(rec, 'language', 'pt'),
            "cached":            cached,
            "created_at":        rec.created_at,
            "next_available_at": next_at,
        }

    def get_cached(self, user_id: UUID) -> dict | None:
        profile = self.profile_repo.find_by_user_id(user_id)
        if not profile:
            return None

        if profile.user.role == UserRole.admin:
            return None

        rec = self.recommendation_repo.find_within_12h(user_id)
        if not rec:
            return None
        return self._to_response(rec, cached=True, is_admin=False)

    def _parse_ai_response(self, raw) -> tuple[list, str | None]:
        """
        Extrai (movies, message) da resposta da IA.
        Suporta o novo formato {message, movies} e o formato legado [array].
        """
        if isinstance(raw, dict):
            return raw.get('movies', []), raw.get('message')
        if isinstance(raw, list):
            return raw, None
        try:
            parsed = json.loads(raw) if isinstance(raw, str) else raw
            if isinstance(parsed, dict):
                return parsed.get('movies', []), parsed.get('message')
            if isinstance(parsed, list):
                return parsed, None
        except Exception:
            pass
        return [], None

    def _parse_raw_text(self, text: str) -> dict:
        """Parses accumulated streaming text into a structured dict."""
        text = text.strip()
        if text.startswith("```"):
            text = re.sub(r"^```[a-z]*\n?", "", text)
            text = re.sub(r"\n?```$", "", text)
            text = text.strip()
        try:
            parsed = json.loads(text)
            if isinstance(parsed, dict) and "movies" in parsed:
                return parsed
            if isinstance(parsed, list):
                return {"message": None, "movies": parsed}
        except json.JSONDecodeError:
            pass
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            try:
                parsed = json.loads(match.group(0))
                if isinstance(parsed, dict):
                    return parsed
            except json.JSONDecodeError:
                pass
        match = re.search(r"\[.*\]", text, re.DOTALL)
        if match:
            try:
                return {"message": None, "movies": json.loads(match.group(0))}
            except json.JSONDecodeError:
                pass
        return {"message": None, "movies": []}

    def generate_stream(self, user_id: UUID, mood: str | None, language: str):
        """
        Returns a generator that streams raw Gemini text chunks and then
        yields a final sentinel line: \\n__RESULT__\\n{json}\\n
        The setup code (auth/cache) runs eagerly before the generator starts.
        """
        profile = self.profile_repo.find_by_user_id(user_id)
        if not profile:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Perfil não encontrado")

        is_admin = profile.user.role == UserRole.admin
        self.recommendation_repo.delete_expired()

        if not is_admin:
            cached = self.recommendation_repo.find_within_12h(user_id)
            if cached:
                result = self._to_response(cached, cached=True, is_admin=False)

                def _cached():
                    yield f'\n__RESULT__\n{json.dumps(result, default=str)}\n'

                return _cached()

        prompt = self.prompt_builder.build(profile, None, language, mood)

        def _stream():
            full_text = ''
            for chunk in self.ai_provider.stream_recommendations(prompt):
                full_text += chunk
                yield chunk

            raw            = self._parse_raw_text(full_text)
            movies, message = self._parse_ai_response(raw)

            rec          = Recommendation(user_id=user_id, prompt_used=prompt, response=movies)
            rec.message  = message
            rec.language = language
            rec          = self.recommendation_repo.upsert(rec)

            result = self._to_response(rec, cached=False, is_admin=is_admin)
            yield f'\n__RESULT__\n{json.dumps(result, default=str)}\n'

        return _stream()

    def generate(
        self,
        user_id:  UUID,
        mood:     str | None = None,
        language: str = 'pt',
    ) -> dict:
        profile = self.profile_repo.find_by_user_id(user_id)
        if not profile:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Perfil não encontrado")

        is_admin = profile.user.role == UserRole.admin

        self.recommendation_repo.delete_expired()

        if not is_admin:
            cached = self.recommendation_repo.find_within_12h(user_id)
            if cached:
                return self._to_response(cached, cached=True, is_admin=False)

        prompt = self.prompt_builder.build(profile, None, language, mood)
        print("\n" + "="*60)
        print("PROMPT ENVIADO PARA A IA:")
        print("="*60)
        print(prompt)
        print("="*60 + "\n")

        raw            = self.ai_provider.get_recommendations(prompt)
        movies, message = self._parse_ai_response(raw)

        rec          = Recommendation(user_id=user_id, prompt_used=prompt, response=movies)
        rec.message  = message
        rec.language = language
        rec          = self.recommendation_repo.upsert(rec)

        return self._to_response(rec, cached=False, is_admin=is_admin)