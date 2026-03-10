# app/routers/translation_router.py
from fastapi import APIRouter, Depends

from app.dependencies import get_current_user_id
from app.schemas.translation_schema import TranslationRequest, TranslationResponse
from app.services.translation_service import TranslationService

router = APIRouter(prefix="/translate", tags=["Translation"])


@router.post("", response_model=TranslationResponse)
def translate_movies(
    data: TranslationRequest,
    _:    str = Depends(get_current_user_id),
):
    service = TranslationService()
    translated = service.translate(data.movies, data.language)
    return {"movies": translated}