# app/schemas/recommendation_schema.py
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class MovieResult(BaseModel):
    title:       str
    year:        int | None = None
    genre:       str | None = None
    description: str


class RecommendationRequest(BaseModel):
    extra_prompt: str | None = None
    language:     str = 'pt'  # idioma para geração das descrições


class RecommendationResponse(BaseModel):
    id:          UUID
    movies:      list[MovieResult]
    prompt_used: str
    created_at:  datetime

    class Config:
        from_attributes = True