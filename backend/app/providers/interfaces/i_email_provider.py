# app/providers/interfaces/i_email_provider.py
from abc import ABC, abstractmethod


class IEmailProvider(ABC):

    @abstractmethod
    def send(self, to: str, subject: str, html: str) -> None:
        pass
