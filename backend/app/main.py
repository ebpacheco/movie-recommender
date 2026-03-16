# app/main.py
import asyncio
from contextlib import asynccontextmanager

from app.routers import password_reset_router
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.database import Base, engine
from app.routers import auth_router, user_router, recommendation_router
from app.routers import translation_router, admin_router
from app.services.cleanup_service import run_cleanup_loop

# Importa os models para o SQLAlchemy registrá-los antes de criar as tabelas
import app.models.user_model                # noqa
import app.models.profile_model             # noqa
import app.models.recommendation_model      # noqa
import app.models.reset_token_model         # noqa
import app.models.email_verification_model  # noqa

Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(run_cleanup_loop())
    yield
    task.cancel()


app = FastAPI(
    title       = "Movie Recommender API",
    description = "API de recomendação de filmes com IA",
    version     = "1.0.0",
    lifespan    = lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins     = settings.allowed_origins,
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

        if field == "email":
            messages.append("E-mail inválido")
        elif field == "cpf":
            messages.append("CPF inválido")
        elif field == "password":
            # Repassa a mensagem do validator de força de senha
            messages.append(msg.replace("Value error, ", ""))
        elif field == "name":
            messages.append("Nome inválido")
        elif field == "birth_date":
            messages.append(msg.replace("Value error, ", ""))
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
app.include_router(translation_router.router,    prefix=PREFIX)
app.include_router(password_reset_router.router, prefix=PREFIX)
app.include_router(admin_router.router,          prefix=PREFIX)


@app.get("/health")
def health():
    return {"status": "ok"}