<div align="center">

<img src="https://img.shields.io/badge/CineMagIA-🎬-ff6b35?style=for-the-badge&labelColor=0d0d0d" alt="CineMagIA" />

# 🎬 CineMagIA

### *O filme certo para como você está agora*

<p>
  Em vez de rolar infinitamente pelo catálogo da sua assinatura,<br/>
  você conta como foi o seu dia — e a IA encontra o filme perfeito para aquele momento.
</p>

<br/>

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Vue](https://img.shields.io/badge/Vue-3.4-42b883?style=flat-square&logo=vue.js&logoColor=white)](https://vuejs.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=flat-square&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Gemini](https://img.shields.io/badge/Google_Gemini-2.5_Flash-8E75B2?style=flat-square&logo=google&logoColor=white)](https://deepmind.google/technologies/gemini/)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=flat-square)](LICENSE)

<br/>

[**✨ Demo ao Vivo**](https://cinemagia.fun)

<br/>

</div>

---

## 📸 Visão Geral

> Projeto fullstack desenvolvido do zero com foco em boas práticas de engenharia de software, aplicando princípios **SOLID** e arquitetura em camadas inspirada no modelo Spring Boot, adaptada para o ecossistema Python/FastAPI.

A CineMagIA resolve um problema real: a paralisia de escolha. Em vez de um sistema de filtros frios, a IA lê o seu **humor** — *"foi um dia pesado, quero algo leve"* — e entrega uma recomendação genuinamente personalizada para aquele momento.

---

## ✨ Funcionalidades

<table>
<tr>
<td width="50%">

**🔐 Autenticação & Segurança**
- Login com JWT + verificação de e-mail
- reCAPTCHA v3 em login e cadastro
- Recuperação de senha via token (1h)
- Conformidade com LGPD

</td>
<td width="50%">

**🎭 Perfil Inteligente**
- Gêneros, filmes, atores e diretores favoritos
- Seleção de plataformas de streaming
- Autosave com debounce (sem clique manual)
- Bloqueio dinâmico de perfil incompleto

</td>
</tr>
<tr>
<td>

**🤖 Recomendação por IA**
- Leitura de humor em linguagem natural
- Mensagem empática personalizada
- Cache por sessão (experiência consistente)
- Provedor configurável: Gemini ou OpenAI

</td>
<td>

**🌍 Experiência Completa**
- Interface em PT, EN e ES
- Tradução automática ao trocar idioma
- Pôsteres, ratings e trailers (TMDB + OMDb)
- Player de trailer embutido via YouTube

</td>
</tr>
<tr>
<td colspan="2">

**👑 Painel Admin** — CRUD completo de usuários com paginação. Admins bypassam o cache e podem gerar novas recomendações a qualquer momento.

</td>
</tr>
</table>

---

## 🏗️ Arquitetura

```
routers → services → repositories → models
                   → providers   (Gemini / OpenAI / Resend / SMTP / SES)
                   → builders    (prompt)
```

| Camada | Responsabilidade |
|---|---|
| **Routers** | Recebe requisições HTTP, valida e delega para services |
| **Services** | Lógica de negócio e regras da aplicação |
| **Repositories** | Acesso ao banco via SQLAlchemy + interfaces |
| **Models** | Entidades ORM: `User`, `Profile`, `Recommendation`, `ResetToken`, `EmailVerification` |
| **Schemas** | Validação entrada/saída com Pydantic (DTOs) |
| **Providers** | Abstrações de IA (`IAIProvider`) e e-mail (`IEmailProvider`) |
| **Builders** | Construção dos prompts enviados à IA (`IPromptBuilder`) |

### Princípios SOLID aplicados

| | Princípio | Aplicação |
|---|---|---|
| **S** | Single Responsibility | `User`, `Profile` e `Recommendation` são modelos separados e independentes |
| **O** | Open/Closed | Novos provedores de IA ou e-mail sem alterar código existente |
| **L** | Liskov Substitution | `GeminiProvider` e `OpenAIProvider` são 100% intercambiáveis via `IAIProvider` |
| **I** | Interface Segregation | Interfaces separadas: `IUserRepository`, `IAIProvider`, `IEmailProvider`, `IPromptBuilder`... |
| **D** | Dependency Inversion | Dependências injetadas via `Depends()` do FastAPI — zero acoplamento direto |

---

## 🤖 Como a IA funciona

```
humor do usuário (texto livre)
        ↓
MoviePromptBuilder          # monta o prompt com perfil + mood + idioma
        ↓
GeminiProvider / OpenAIProvider   # chama gemini-2.5-flash-lite ou gpt-4o
        ↓
{ message, movies[] }       # objeto JSON com mensagem empática + lista de filmes
        ↓
useMovieEnrich (TMDB)       # valida disponibilidade nas plataformas do usuário
        ↓
filmes confirmados          # exibe apenas os que passaram no hard filter
```

O cache é salvo no banco junto com a mensagem e o idioma — o usuário vê exatamente a mesma experiência ao retornar na sessão.

---

## 🛠️ Stack Tecnológico

**Backend**

![Python](https://img.shields.io/badge/-Python_3.13-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/-FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/-PostgreSQL_16-4169E1?style=flat-square&logo=postgresql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/-SQLAlchemy_2-red?style=flat-square)
![JWT](https://img.shields.io/badge/-JWT-000000?style=flat-square&logo=json-web-tokens)
![Alembic](https://img.shields.io/badge/-Alembic-gray?style=flat-square)

**Frontend**

![Vue](https://img.shields.io/badge/-Vue_3.4-42b883?style=flat-square&logo=vue.js&logoColor=white)
![Vite](https://img.shields.io/badge/-Vite_5-646CFF?style=flat-square&logo=vite&logoColor=white)
![Pinia](https://img.shields.io/badge/-Pinia_2-FFD859?style=flat-square)
![Axios](https://img.shields.io/badge/-Axios-5A29E4?style=flat-square&logo=axios)
![Vue I18n](https://img.shields.io/badge/-Vue_I18n_9_(PT/EN/ES)-42b883?style=flat-square)

**APIs & Serviços**

| Serviço | Uso |
|---|---|
| **Google Gemini** (`gemini-2.5-flash-lite`) | Recomendações, mensagem empática e tradução |
| **OpenAI** (`gpt-4o`) | Alternativa configurável via variável de ambiente |
| **TMDB** | Pôsteres, trailers, fotos, provedores de streaming por país |
| **OMDb** | Ratings IMDb e Rotten Tomatoes |
| **YouTube Embed** | Player de trailers integrado no app |
| **Resend / SMTP / AWS SES** | E-mail transacional (configurável) |

**Infraestrutura**

![Cloudflare](https://img.shields.io/badge/-Cloudflare_Workers_(frontend)-F38020?style=flat-square&logo=cloudflare&logoColor=white)
![Render](https://img.shields.io/badge/-Render_(backend)-46E3B7?style=flat-square&logo=render&logoColor=black)
![Neon](https://img.shields.io/badge/-Neon_(database)-00E599?style=flat-square&logo=neon&logoColor=black)
![Hostinger](https://img.shields.io/badge/-Hostinger_(cinemagia.fun)-673DE6?style=flat-square)

---

## 📁 Estrutura do Projeto

```
movie-recommender/
├── backend/
│   ├── app/
│   │   ├── builders/        # IPromptBuilder + MoviePromptBuilder
│   │   ├── core/            # Config (pydantic-settings) + SessionCache
│   │   ├── models/          # User, Profile, Recommendation, ResetToken, EmailVerification
│   │   ├── providers/       # IAIProvider, IEmailProvider + implementações
│   │   │                    # (Gemini, OpenAI, Resend, SMTP, SES)
│   │   ├── repositories/    # Acesso ao banco + interfaces
│   │   ├── routers/         # auth, user, recommendation, admin,
│   │   │                    # password_reset, translation
│   │   ├── schemas/         # DTOs Pydantic
│   │   ├── services/        # auth, user, profile, recommendation, email,
│   │   │                    # password_reset, translation, recaptcha, cleanup
│   │   ├── database.py
│   │   ├── dependencies.py  # Injeção de dependências (factory functions)
│   │   └── main.py
│   ├── alembic/             # Migrations
│   └── requirements.txt
│
└── frontend/
    └── src/
        ├── components/      # NavBar, MovieCard, TrailerModal, AutocompleteInput,
        │                    # RecommendationHistory, UserDropdown...
        ├── composables/     # useRecommendations, useTrailer, useMovieEnrich,
        │                    # useProfileAutosave, useAdminUsers...
        ├── constants/       # genres.js, countries.js
        ├── i18n/            # pt.json, en.json, es.json
        ├── router/          # Vue Router + auth guard
        ├── services/        # api.js (Axios + JWT), tmdb.js, omdb.js,
        │                    # youtube.js, translate.js
        ├── stores/          # Pinia: auth, profile, recommendations, streaming
        └── views/           # Login, Register, Recommendations, Profile,
                             # UserPreferences, Admin, Account, ForgotPassword,
                             # ResetPassword, VerifyEmail, Terms, Privacy
```

---

## 🚀 Como Executar Localmente

### Pré-requisitos

- Python 3.13+ · Node.js 18+ · PostgreSQL (ou Docker)

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/movie-recommender.git
cd movie-recommender
```

### 2. Configure as variáveis de ambiente

```bash
# Backend
cd backend
cp .env.example .env

# Frontend
cd ../frontend
cp .env.example .env
```

### 3. Suba o backend

```bash
cd backend
python -m venv venv
source venv/bin/activate      # Linux/Mac
# venv\Scripts\activate       # Windows

pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
# 📖 Docs disponíveis em http://localhost:8000/docs
```

### 4. Suba o frontend

```bash
cd ../frontend
npm install
npm run dev
# 🌐 App disponível em http://localhost:5173
```

---

## 🔑 Variáveis de Ambiente

### Backend `backend/.env`

```env
# Banco de dados (produção: Neon | local: PostgreSQL)
DATABASE_URL=postgresql://user:password@ep-xxx.sa-east-1.aws.neon.tech/neondb?sslmode=require

SECRET_KEY=sua-chave-secreta-jwt
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# Provedor de IA: gemini | openai
AI_PROVIDER=gemini
GEMINI_API_KEY=sua-chave-gemini
OPENAI_API_KEY=sua-chave-openai     # opcional

# Provedor de e-mail: resend | smtp | ses
EMAIL_PROVIDER=resend
EMAIL_FROM=noreply@cinemagia.fun
RESEND_API_KEY=re_xxxxxxxxxxxx

# SMTP (se EMAIL_PROVIDER=smtp)
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=user@example.com
SMTP_PASSWORD=senha

# AWS SES (se EMAIL_PROVIDER=ses)
AWS_REGION=us-east-1
AWS_ACCESS_KEY=sua-access-key
AWS_SECRET_KEY=sua-secret-key

FRONTEND_URL=https://cinemagia.fun
RECAPTCHA_SECRET_KEY=sua-chave-recaptcha
APP_ENV=development
```

### Frontend `frontend/.env`

```env
VITE_API_URL=https://seu-backend.onrender.com
VITE_TMDB_TOKEN=seu-token-tmdb
VITE_OMDB_API_KEY=sua-chave-omdb
VITE_RECAPTCHA_SITE_KEY=sua-chave-recaptcha
VITE_APP_NAME=CineMagIA
```

---
