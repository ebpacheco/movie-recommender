# app/builders/interfaces/i_prompt_builder.py
from abc import ABC, abstractmethod

from app.models.profile_model import Profile


class IPromptBuilder(ABC):

    @abstractmethod
    def build(self, profile: Profile, extra_context: str | None = None) -> str:
        pass
