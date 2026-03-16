# app/providers/resend_provider.py
import json
import logging
import urllib.request
import urllib.error

from app.providers.interfaces.i_email_provider import IEmailProvider

logger = logging.getLogger(__name__)

API_URL = "https://api.resend.com/emails"


class ResendProvider(IEmailProvider):

    def __init__(self, api_key: str, from_email: str) -> None:
        self.api_key    = api_key
        self.from_email = from_email

    def send(self, to: str, subject: str, html: str) -> None:
        payload = json.dumps({
            "from":    self.from_email,
            "to":      [to],
            "subject": subject,
            "html":    html,
        }).encode("utf-8")

        req = urllib.request.Request(
            API_URL,
            data    = payload,
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type":  "application/json",
            },
            method = "POST",
        )

        try:
            with urllib.request.urlopen(req) as resp:
                logger.info(f"[Resend] E-mail enviado para {to} — status {resp.status}")
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            logger.error(f"[Resend] Erro HTTP {e.code} ao enviar para {to}: {body}")
            raise
