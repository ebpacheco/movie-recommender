# app/main.py
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

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
    allow_origins     = ["http://localhost:5173"],
    allow_credentials = True,
    allow_methods     = ["*"],
    allow_headers     = ["*"],
)

# Transforma erros de validação do Pydantic em mensagens legíveis
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    messages = []
    for e in errors:
        field = e["loc"][-1] if e["loc"] else "campo"
        msg   = e["msg"]

        # Mensagens amigáveis por campo
        if field == "email":
            messages.append("E-mail inválido")
        elif field == "cpf":
            messages.append("CPF inválido")
        elif field == "password":
            messages.append("Senha inválida")
        elif field == "name":
            messages.append("Nome inválido")
        else:
            messages.append(f"{field}: {msg}")

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": " | ".join(messages)},
    )

PREFIX = "/api/v1"
app.include_router(auth_router.router,           prefix=PREFIX)
app.include_router(user_router.router,           prefix=PREFIX)
app.include_router(recommendation_router.router, prefix=PREFIX)


@app.get("/health")
def health():
    return {"status": "ok"}