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
    movies:            list[MovieResult]
    message:           str | None = None
    cached:            bool = False
    created_at:        datetime | None = None
    next_available_at: datetime | None = None