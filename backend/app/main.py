# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import auth_router, user_router, recommendation_router

# Importa os models para o SQLAlchemy registrá-los antes de criar as tabelas
import app.models.user_model           # noqa
import app.models.profile_model        # noqa
import app.models.recommendation_model # noqa

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title       = "Movie Recommender API",
    description = "API de recomendação de filmes com IA",
    version     = "1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins     = ["http://localhost:5173"],  # URL do Vite em dev
    allow_credentials = True,
    allow_methods     = ["*"],
    allow_headers     = ["*"],
)

PREFIX = "/api/v1"
app.include_router(auth_router.router,           prefix=PREFIX)
app.include_router(user_router.router,           prefix=PREFIX)
app.include_router(recommendation_router.router, prefix=PREFIX)


@app.get("/health")
def health():
    return {"status": "ok"}
