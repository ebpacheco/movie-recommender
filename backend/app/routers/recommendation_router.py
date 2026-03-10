# app/routers/recommendation_router.py
from uuid import UUID
from fastapi import APIRouter, Depends

from app.dependencies import get_recommendation_service, get_current_user_id
from app.schemas.recommendation_schema import RecommendationRequest, RecommendationResponse
from app.services.recommendation_service import RecommendationService

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


@router.post("", response_model=RecommendationResponse, status_code=201)
def create(
    data:    RecommendationRequest,
    user_id: UUID                      = Depends(get_current_user_id),
    service: RecommendationService     = Depends(get_recommendation_service),
):
    rec = service.generate(user_id, data.extra_prompt, data.language)
    return _to_response(rec)


@router.get("", response_model=list[RecommendationResponse])
def list_all(
    user_id: UUID                  = Depends(get_current_user_id),
    service: RecommendationService = Depends(get_recommendation_service),
):
    return [_to_response(r) for r in service.list_by_user(user_id)]


@router.get("/{recommendation_id}", response_model=RecommendationResponse)
def get_one(
    recommendation_id: UUID,
    user_id: UUID                  = Depends(get_current_user_id),
    service: RecommendationService = Depends(get_recommendation_service),
):
    return _to_response(service.get_by_id(recommendation_id, user_id))


def _to_response(rec) -> dict:
    return {
        "id":          rec.id,
        "movies":      rec.response,
        "prompt_used": rec.prompt_used,
        "created_at":  rec.created_at,
    }