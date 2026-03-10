# app/services/recommendation_service.py
from uuid import UUID
from datetime import date
from fastapi import HTTPException, status

from app.models.recommendation_model import Recommendation
from app.models.user_model import UserRole
from app.repositories.interfaces.i_user_repository import IProfileRepository
from app.repositories.interfaces.i_recommendation_repository import IRecommendationRepository
from app.providers.interfaces.i_ai_provider import IAIProvider
from app.builders.interfaces.i_prompt_builder import IPromptBuilder


DAILY_LIMITS = {
    UserRole.free:    1,
    UserRole.premium: 3,
    UserRole.admin:   None,  # ilimitado
}


class RecommendationService:

    def __init__(
        self,
        profile_repo:        IProfileRepository,
        recommendation_repo: IRecommendationRepository,
        ai_provider:         IAIProvider,
        prompt_builder:      IPromptBuilder,
    ):
        self.profile_repo        = profile_repo
        self.recommendation_repo = recommendation_repo
        self.ai_provider         = ai_provider
        self.prompt_builder      = prompt_builder

    def generate(
        self,
        user_id:      UUID,
        extra_prompt: str | None = None,
        language:     str = 'pt',
    ) -> Recommendation:
        profile = self.profile_repo.find_by_user_id(user_id)
        if not profile:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Perfil não encontrado")

        # Verifica limite diário baseado no role do usuário
        user  = profile.user
        limit = DAILY_LIMITS.get(user.role)

        if limit is not None:
            today = date.today()
            count = self.recommendation_repo.count_by_user_and_date(user_id, today)
            if count >= limit:
                role_names = {
                    UserRole.free:    "gratuito",
                    UserRole.premium: "premium",
                }
                raise HTTPException(
                    status.HTTP_429_TOO_MANY_REQUESTS,
                    f"Limite diário atingido. Usuários {role_names[user.role]} podem solicitar "
                    f"{limit} recomendação{'ões' if limit > 1 else ''} por dia.",
                )

        prompt = self.prompt_builder.build(profile, extra_prompt, language)
        movies = self.ai_provider.get_recommendations(prompt)

        recommendation = Recommendation(
            user_id     = user_id,
            prompt_used = prompt,
            response    = movies,
        )
        return self.recommendation_repo.save(recommendation)

    def list_by_user(self, user_id: UUID) -> list[Recommendation]:
        return self.recommendation_repo.find_all_by_user_id(user_id)

    def get_by_id(self, recommendation_id: UUID, user_id: UUID) -> Recommendation:
        rec = self.recommendation_repo.find_by_id(recommendation_id)
        if not rec:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Recomendação não encontrada")
        if rec.user_id != user_id:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Acesso negado")
        return rec