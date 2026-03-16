# app/routers/recommendation_router.py
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse

from app.dependencies import get_recommendation_service, get_current_user_id
from app.schemas.recommendation_schema import RecommendationRequest, RecommendationResponse
from app.services.recommendation_service import RecommendationService

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


@router.get("/latest", response_model=RecommendationResponse)
def get_latest(
    user_id: UUID                  = Depends(get_current_user_id),
    service: RecommendationService = Depends(get_recommendation_service),
):
    """Retorna a recomendação em cache das últimas 12h, se existir."""
    cached = service.get_cached(user_id)
    if not cached:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Nenhuma recomendação nas últimas 24h")
    return cached


@router.post("", response_model=RecommendationResponse, status_code=200)
def create(
    data:    RecommendationRequest,
    user_id: UUID                  = Depends(get_current_user_id),
    service: RecommendationService = Depends(get_recommendation_service),
):
    """Gera nova recomendação ou retorna o cache das últimas 12h."""
    return service.generate(user_id, data.mood, data.language)


@router.post("/stream", status_code=200)
def stream_create(
    data:    RecommendationRequest,
    user_id: UUID                  = Depends(get_current_user_id),
    service: RecommendationService = Depends(get_recommendation_service),
):
    """Streaming: mantém conexão viva enquanto o Gemini gera. Envia __RESULT__ no final."""
    gen = service.generate_stream(user_id, data.mood, data.language)
    return StreamingResponse(gen, media_type="text/plain")