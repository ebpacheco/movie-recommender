# app/services/email_service.py
"""
Envio de e-mail com suporte a dois provedores:
  - SMTP  → dev/homologação  (EMAIL_PROVIDER=smtp)
  - SES   → produção         (EMAIL_PROVIDER=ses)

Variáveis de ambiente necessárias:
  Comuns:
    EMAIL_PROVIDER   = smtp | ses
    EMAIL_FROM       = noreply@seudominio.com
    FRONTEND_URL     = https://app.seudominio.com

  SMTP:
    SMTP_HOST        = smtp.gmail.com
    SMTP_PORT        = 587
    SMTP_USER        = seu@gmail.com
    SMTP_PASSWORD    = app-password-aqui

  SES:
    AWS_REGION       = us-east-1
    AWS_ACCESS_KEY   = AKIA...
    AWS_SECRET_KEY   = ...
"""
import os
import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

logger = logging.getLogger(__name__)

EMAIL_PROVIDER = os.getenv("EMAIL_PROVIDER", "smtp").lower()
EMAIL_FROM     = os.getenv("EMAIL_FROM", "noreply@cinemagic.app")
FRONTEND_URL   = os.getenv("FRONTEND_URL", "http://localhost:5173")


# ── Templates por idioma ──────────────────────────────────────────────────────

TEMPLATES = {
    "pt": {
        "subject": "Recuperação de senha — CineMAGIC",
        "body": lambda url, name: f"""
<!DOCTYPE html>
<html lang="pt">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"></head>
<body style="margin:0;padding:0;background:#08080c;font-family:'Segoe UI',sans-serif;">
  <div style="max-width:520px;margin:40px auto;background:#0f0f15;border:1px solid rgba(212,175,55,0.2);border-radius:16px;overflow:hidden;">
    <div style="background:linear-gradient(135deg,#1a1a24,#0f0f15);padding:32px 40px;border-bottom:1px solid rgba(212,175,55,0.15);text-align:center;">
      <span style="font-size:2rem;">🎬</span>
      <h1 style="color:#d4af37;font-size:1.5rem;margin:8px 0 0;letter-spacing:0.05em;">CineMAGIC</h1>
    </div>
    <div style="padding:36px 40px;">
      <h2 style="color:#e8e0d0;font-size:1.1rem;margin:0 0 12px;">Olá, {name}!</h2>
      <p style="color:#8a7a5a;font-size:0.95rem;line-height:1.6;margin:0 0 24px;">
        Recebemos uma solicitação para redefinir a senha da sua conta CineMAGIC.
        Clique no botão abaixo para criar uma nova senha.
      </p>
      <div style="text-align:center;margin:28px 0;">
        <a href="{url}" style="display:inline-block;padding:14px 32px;background:linear-gradient(135deg,#d4af37,#b8860b);color:#08080c;text-decoration:none;border-radius:10px;font-weight:600;font-size:0.95rem;letter-spacing:0.03em;">
          Redefinir minha senha
        </a>
      </div>
      <p style="color:#6b6050;font-size:0.82rem;line-height:1.6;margin:0;">
        ⏱ Este link expira em <strong style="color:#d4af37;">1 hora</strong>.<br>
        Se você não solicitou a redefinição, ignore este e-mail — sua senha permanece a mesma.
      </p>
    </div>
    <div style="padding:16px 40px;border-top:1px solid rgba(255,255,255,0.04);text-align:center;">
      <p style="color:#3a3228;font-size:0.75rem;margin:0;">© CineMAGIC · Todos os direitos reservados</p>
    </div>
  </div>
</body>
</html>
""",
    },
    "en": {
        "subject": "Password recovery — CineMAGIC",
        "body": lambda url, name: f"""
<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"></head>
<body style="margin:0;padding:0;background:#08080c;font-family:'Segoe UI',sans-serif;">
  <div style="max-width:520px;margin:40px auto;background:#0f0f15;border:1px solid rgba(212,175,55,0.2);border-radius:16px;overflow:hidden;">
    <div style="background:linear-gradient(135deg,#1a1a24,#0f0f15);padding:32px 40px;border-bottom:1px solid rgba(212,175,55,0.15);text-align:center;">
      <span style="font-size:2rem;">🎬</span>
      <h1 style="color:#d4af37;font-size:1.5rem;margin:8px 0 0;letter-spacing:0.05em;">CineMAGIC</h1>
    </div>
    <div style="padding:36px 40px;">
      <h2 style="color:#e8e0d0;font-size:1.1rem;margin:0 0 12px;">Hi, {name}!</h2>
      <p style="color:#8a7a5a;font-size:0.95rem;line-height:1.6;margin:0 0 24px;">
        We received a request to reset your CineMAGIC account password.
        Click the button below to create a new password.
      </p>
      <div style="text-align:center;margin:28px 0;">
        <a href="{url}" style="display:inline-block;padding:14px 32px;background:linear-gradient(135deg,#d4af37,#b8860b);color:#08080c;text-decoration:none;border-radius:10px;font-weight:600;font-size:0.95rem;letter-spacing:0.03em;">
          Reset my password
        </a>
      </div>
      <p style="color:#6b6050;font-size:0.82rem;line-height:1.6;margin:0;">
        ⏱ This link expires in <strong style="color:#d4af37;">1 hour</strong>.<br>
        If you didn't request this, just ignore this email — your password will stay the same.
      </p>
    </div>
    <div style="padding:16px 40px;border-top:1px solid rgba(255,255,255,0.04);text-align:center;">
      <p style="color:#3a3228;font-size:0.75rem;margin:0;">© CineMAGIC · All rights reserved</p>
    </div>
  </div>
</body>
</html>
""",
    },
    "es": {
        "subject": "Recuperación de contraseña — CineMAGIC",
        "body": lambda url, name: f"""
<!DOCTYPE html>
<html lang="es">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"></head>
<body style="margin:0;padding:0;background:#08080c;font-family:'Segoe UI',sans-serif;">
  <div style="max-width:520px;margin:40px auto;background:#0f0f15;border:1px solid rgba(212,175,55,0.2);border-radius:16px;overflow:hidden;">
    <div style="background:linear-gradient(135deg,#1a1a24,#0f0f15);padding:32px 40px;border-bottom:1px solid rgba(212,175,55,0.15);text-align:center;">
      <span style="font-size:2rem;">🎬</span>
      <h1 style="color:#d4af37;font-size:1.5rem;margin:8px 0 0;letter-spacing:0.05em;">CineMAGIC</h1>
    </div>
    <div style="padding:36px 40px;">
      <h2 style="color:#e8e0d0;font-size:1.1rem;margin:0 0 12px;">¡Hola, {name}!</h2>
      <p style="color:#8a7a5a;font-size:0.95rem;line-height:1.6;margin:0 0 24px;">
        Recibimos una solicitud para restablecer la contraseña de tu cuenta CineMAGIC.
        Haz clic en el botón para crear una nueva contraseña.
      </p>
      <div style="text-align:center;margin:28px 0;">
        <a href="{url}" style="display:inline-block;padding:14px 32px;background:linear-gradient(135deg,#d4af37,#b8860b);color:#08080c;text-decoration:none;border-radius:10px;font-weight:600;font-size:0.95rem;letter-spacing:0.03em;">
          Restablecer mi contraseña
        </a>
      </div>
      <p style="color:#6b6050;font-size:0.82rem;line-height:1.6;margin:0;">
        ⏱ Este enlace expira en <strong style="color:#d4af37;">1 hora</strong>.<br>
        Si no solicitaste esto, ignora este correo — tu contraseña seguirá siendo la misma.
      </p>
    </div>
    <div style="padding:16px 40px;border-top:1px solid rgba(255,255,255,0.04);text-align:center;">
      <p style="color:#3a3228;font-size:0.75rem;margin:0;">© CineMAGIC · Todos los derechos reservados</p>
    </div>
  </div>
</body>
</html>
""",
    },
}


def _get_template(language: str) -> dict:
    return TEMPLATES.get(language, TEMPLATES["pt"])


# ── Providers ─────────────────────────────────────────────────────────────────

def _send_smtp(to: str, subject: str, html: str) -> None:
    host     = os.getenv("SMTP_HOST", "smtp.gmail.com")
    port     = int(os.getenv("SMTP_PORT", "587"))
    user     = os.getenv("SMTP_USER", "")
    password = os.getenv("SMTP_PASSWORD", "")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = EMAIL_FROM
    msg["To"]      = to
    msg.attach(MIMEText(html, "html", "utf-8"))

    with smtplib.SMTP(host, port) as server:
        server.ehlo()
        server.starttls()
        server.login(user, password)
        server.sendmail(EMAIL_FROM, to, msg.as_string())

    logger.info(f"[SMTP] E-mail enviado para {to}")


def _send_ses(to: str, subject: str, html: str) -> None:
    try:
        import boto3
    except ImportError:
        raise RuntimeError("boto3 não instalado. Execute: pip install boto3 --break-system-packages")

    client = boto3.client(
        "ses",
        region_name          = os.getenv("AWS_REGION", "us-east-1"),
        aws_access_key_id    = os.getenv("AWS_ACCESS_KEY"),
        aws_secret_access_key= os.getenv("AWS_SECRET_KEY"),
    )

    client.send_email(
        Source      = EMAIL_FROM,
        Destination = {"ToAddresses": [to]},
        Message     = {
            "Subject": {"Data": subject, "Charset": "UTF-8"},
            "Body":    {"Html": {"Data": html, "Charset": "UTF-8"}},
        },
    )
    logger.info(f"[SES] E-mail enviado para {to}")


# ── Interface pública ─────────────────────────────────────────────────────────

def send_password_reset_email(to: str, name: str, token: str, language: str = "pt") -> None:
    """Envia o e-mail de recuperação de senha no idioma do usuário."""
    reset_url = f"{FRONTEND_URL}/reset-password?token={token}"
    template  = _get_template(language)
    subject   = template["subject"]
    html      = template["body"](reset_url, name)

    if EMAIL_PROVIDER == "ses":
        _send_ses(to, subject, html)
    else:
        _send_smtp(to, subject, html)