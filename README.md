# 🎬 Movie Recommender

Aplicação de recomendação de filmes com IA (OpenAI), FastAPI, PostgreSQL e Vue.js.

---

## Stack

| Camada      | Tecnologia                        |
|-------------|-----------------------------------|
| Front-end   | Vue 3 + Vite + Pinia + Vue Router |
| Back-end    | Python 3.11 + FastAPI             |
| Banco       | PostgreSQL 16                     |
| ORM         | SQLAlchemy 2                      |
| Auth        | JWT (python-jose + passlib)       |
| IA          | OpenAI API (gpt-4o-mini)          |

---

## Como rodar localmente

### 1. Banco de dados (Docker)
```bash
cd backend
docker-compose up -d
```

### 2. Back-end
```bash
cd backend

# Criar e ativar ambiente virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
cp .env.example .env
# Edite o .env com sua OPENAI_API_KEY e demais configurações

# Rodar o servidor
uvicorn app.main:app --reload
```

A API estará disponível em: http://localhost:8000
Documentação automática: http://localhost:8000/docs

### 3. Front-end
```bash
cd frontend
npm install
npm run dev
```

O front estará disponível em: http://localhost:5173

---

## Estrutura do Back-end

```
app/
├── core/           # Configurações (variáveis de ambiente)
├── models/         # Entidades ORM (SQLAlchemy)
├── schemas/        # Contratos de entrada/saída (Pydantic)
├── repositories/   # Acesso ao banco (SRP + ISP)
│   └── interfaces/ # Abstrações (DIP)
├── services/       # Regras de negócio
├── routers/        # Endpoints HTTP
├── providers/      # Integrações externas (OpenAI)
│   └── interfaces/ # Abstrações (LSP + DIP)
├── builders/       # Construtores de prompt (OCP)
│   └── interfaces/
├── dependencies.py # Injeção de dependências (FastAPI DI)
├── database.py     # Sessão do banco
└── main.py         # Entry point
```

## Endpoints

| Método | Rota                          | Descrição                  |
|--------|-------------------------------|----------------------------|
| POST   | /api/v1/auth/register         | Cadastro de usuário        |
| POST   | /api/v1/auth/login            | Login, retorna JWT         |
| GET    | /api/v1/users/me              | Dados do usuário logado    |
| GET    | /api/v1/users/me/profile      | Preferências do usuário    |
| PUT    | /api/v1/users/me/profile      | Atualiza preferências      |
| POST   | /api/v1/recommendations       | Gera recomendações com IA  |
| GET    | /api/v1/recommendations       | Lista histórico            |
| GET    | /api/v1/recommendations/{id}  | Detalha uma recomendação   |
