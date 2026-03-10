# app/schemas/translation_schema.py
from pydantic import BaseModel


class MovieToTranslate(BaseModel):
    title: str
    year:  int | None = None
    genre: str | None = None


class TranslationRequest(BaseModel):
    movies:   list[MovieToTranslate]
    language: str = 'pt'


class MovieTranslated(BaseModel):
    title:       str
    year:        int | None = None
    genre:       str | None = None
    description: str


class TranslationResponse(BaseModel):
    movies: list[MovieTranslated]