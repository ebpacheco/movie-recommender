# app/core/session_cache.py
"""
Cache de sessão em memória por usuário.
Populado no login/register, usado para leitura rápida de perfil
sem hit no banco de dados a cada requisição.
"""
from typing import Optional
from uuid import UUID

from app.core.interfaces.i_session_cache import ISessionCache


class SessionCache(ISessionCache):

    def __init__(self) -> None:
        self._cache: dict[str, dict] = {}

    def set_session(self, user_id: UUID, data: dict) -> None:
        """Salva ou sobrescreve a sessão completa do usuário."""
        self._cache[str(user_id)] = data

    def get_session(self, user_id: UUID) -> Optional[dict]:
        """Retorna a sessão do usuário ou None se não existir."""
        return self._cache.get(str(user_id))

    def update_session(self, user_id: UUID, **kwargs) -> None:
        """Atualiza campos específicos da sessão sem sobrescrever o resto."""
        key = str(user_id)
        if key in self._cache:
            self._cache[key].update(kwargs)

    def update_profile_session(self, user_id: UUID, profile: dict) -> None:
        """Atualiza apenas o sub-dicionário de perfil na sessão."""
        key = str(user_id)
        if key in self._cache:
            self._cache[key]["profile"] = profile

    def clear_session(self, user_id: UUID) -> None:
        """Remove a sessão do usuário (logout)."""
        self._cache.pop(str(user_id), None)

    def has_session(self, user_id: UUID) -> bool:
        return str(user_id) in self._cache


# Singleton de módulo — compatibilidade com código existente
session_cache = SessionCache()

# Atalhos funcionais para não quebrar imports existentes
def set_session(user_id: UUID, data: dict) -> None:
    session_cache.set_session(user_id, data)

def get_session(user_id: UUID) -> Optional[dict]:
    return session_cache.get_session(user_id)

def update_session(user_id: UUID, **kwargs) -> None:
    session_cache.update_session(user_id, **kwargs)

def update_profile_session(user_id: UUID, profile: dict) -> None:
    session_cache.update_profile_session(user_id, profile)

def clear_session(user_id: UUID) -> None:
    session_cache.clear_session(user_id)

def has_session(user_id: UUID) -> bool:
    return session_cache.has_session(user_id)
