# app/schemas/recommendation_schema.py
from datetime import datetime
from pydantic import BaseModel


class MovieResult(BaseModel):
    title:       str
    year:        int | None = None
    genre:       str | None = None
    description: str


class RecommendationRequest(BaseModel):
    mood:     str | None = None
    language: str = 'pt'


class RecommendationResponse(BaseModel):
    movies:           list[MovieResult]
    cached:           bool = False
    created_at:       datetime | None = None
    next_available_at: datetime | None = None  # created_at + 24h — usado no countdown do frontend