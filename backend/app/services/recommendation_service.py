# app/services/recommendation_service.py
from uuid import UUID
from datetime import timedelta

from fastapi import HTTPException, status

from app.models.recommendation_model import Recommendation
from app.models.user_model import UserRole
from app.repositories.recommendation_repository import RecommendationRepository
from app.repositories.interfaces.i_user_repository import IProfileRepository
from app.providers.interfaces.i_ai_provider import IAIProvider
from app.builders.interfaces.i_prompt_builder import IPromptBuilder

CACHE_HOURS = 12


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
        # Admin não recebe next_available_at — pode gerar a qualquer momento
        next_at = None if is_admin else rec.created_at + timedelta(hours=CACHE_HOURS)
        return {
            "movies":            rec.response,
            "cached":            cached,
            "created_at":        rec.created_at,
            "next_available_at": next_at,
        }

    def get_cached(self, user_id: UUID) -> dict | None:
        """Retorna a recomendação em cache das últimas 12h, ou None."""
        profile = self.profile_repo.find_by_user_id(user_id)
        if not profile:
            return None

        # Admin nunca retorna cache no GET /today — sempre pode gerar novo
        if profile.user.role == UserRole.admin:
            return None

        rec = self.recommendation_repo.find_within_12h(user_id)
        if not rec:
            return None
        return self._to_response(rec, cached=True, is_admin=False)

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
        movies = self.ai_provider.get_recommendations(prompt)

        rec = Recommendation(user_id=user_id, prompt_used=prompt, response=movies)
        rec = self.recommendation_repo.upsert(rec)

        return self._to_response(rec, cached=False, is_admin=is_admin)