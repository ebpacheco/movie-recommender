# app/providers/resend_provider.py
import logging
import resend

from app.providers.interfaces.i_email_provider import IEmailProvider

logger = logging.getLogger(__name__)


class ResendProvider(IEmailProvider):

    def __init__(self, api_key: str, from_email: str) -> None:
        self.from_email  = from_email
        resend.api_key   = api_key

    def send(self, to: str, subject: str, html: str) -> None:
        params: resend.Emails.SendParams = {
            "from":    self.from_email,
            "to":      [to],
            "subject": subject,
            "html":    html,
        }
        result = resend.Emails.send(params)
        logger.info(f"[Resend] E-mail enviado para {to} — id {result.get('id')}")
