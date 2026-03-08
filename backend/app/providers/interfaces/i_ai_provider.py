# app/providers/interfaces/i_ai_provider.py
from abc import ABC, abstractmethod


class IAIProvider(ABC):

    @abstractmethod
    def get_recommendations(self, prompt: str) -> list[dict]:
        """
        Recebe um prompt e retorna uma lista de filmes no formato:
        [{"title": "...", "year": ..., "genre": "...", "description": "..."}]
        """
        pass
