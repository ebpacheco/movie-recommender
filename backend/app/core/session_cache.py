# app/core/session_cache.py
"""
Cache de sessão em memória por usuário.
Populado no login/register, usado para leitura rápida de perfil
sem hit no banco de dados a cada requisição.
"""
from uuid import UUID
from typing import Optional

_cache: dict[str, dict] = {}


def set_session(user_id: UUID, data: dict) -> None:
    """Salva ou sobrescreve a sessão completa do usuário."""
    _cache[str(user_id)] = data


def get_session(user_id: UUID) -> Optional[dict]:
    """Retorna a sessão do usuário ou None se não existir."""
    return _cache.get(str(user_id))


def update_session(user_id: UUID, **kwargs) -> None:
    """Atualiza campos específicos da sessão sem sobrescrever o resto."""
    key = str(user_id)
    if key in _cache:
        _cache[key].update(kwargs)


def update_profile_session(user_id: UUID, profile: dict) -> None:
    """Atualiza apenas o sub-dicionário de perfil na sessão."""
    key = str(user_id)
    if key in _cache:
        _cache[key]["profile"] = profile


def clear_session(user_id: UUID) -> None:
    """Remove a sessão do usuário (logout)."""
    _cache.pop(str(user_id), None)


def has_session(user_id: UUID) -> bool:
    return str(user_id) in _cache