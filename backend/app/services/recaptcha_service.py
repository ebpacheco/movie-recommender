# app/services/recaptcha_service.py
import json
import urllib.request
import urllib.parse

from app.core.config import settings

VERIFY_URL = "https://www.google.com/recaptcha/api/siteverify"
MIN_SCORE  = 0.5


def verify_recaptcha(token: str) -> bool:
    """
    Verifica o token reCAPTCHA v3 com a API do Google.
    Retorna True se o token for válido e o score >= MIN_SCORE.
    Em desenvolvimento (sem chave configurada) sempre retorna True.
    """
    if not settings.RECAPTCHA_SECRET_KEY:
        return True

    try:
        payload = urllib.parse.urlencode({
            "secret":   settings.RECAPTCHA_SECRET_KEY,
            "response": token,
        }).encode()

        req  = urllib.request.Request(VERIFY_URL, data=payload, method="POST")
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read())

        return bool(data.get("success")) and data.get("score", 0) >= MIN_SCORE
    except Exception:
        return False
