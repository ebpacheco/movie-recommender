# app/providers/ses_provider.py
import logging

from app.core.config import settings
from app.providers.interfaces.i_email_provider import IEmailProvider

logger = logging.getLogger(__name__)


class SesProvider(IEmailProvider):

    def send(self, to: str, subject: str, html: str) -> None:
        try:
            import boto3
        except ImportError:
            raise RuntimeError("boto3 não instalado. Execute: pip install boto3")

        client = boto3.client(
            "ses",
            region_name           = settings.AWS_REGION,
            aws_access_key_id     = settings.AWS_ACCESS_KEY,
            aws_secret_access_key = settings.AWS_SECRET_KEY,
        )

        client.send_email(
            Source      = settings.EMAIL_FROM,
            Destination = {"ToAddresses": [to]},
            Message     = {
                "Subject": {"Data": subject, "Charset": "UTF-8"},
                "Body":    {"Html": {"Data": html, "Charset": "UTF-8"}},
            },
        )
        logger.info(f"[SES] E-mail enviado para {to}")
