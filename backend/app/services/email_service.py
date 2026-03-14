# app/services/email_service.py
"""
Serviço de envio de e-mail.
Recebe um IEmailProvider via injeção de dependência (SMTP ou SES).

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
from app.core.config import settings
from app.providers.interfaces.i_email_provider import IEmailProvider


# ── Templates por idioma ──────────────────────────────────────────────────────

VERIFICATION_TEMPLATES = {
    "pt": {
        "subject": "Confirme seu e-mail — CineMagIA",
        "body": lambda url, name: f"""
<!DOCTYPE html>
<html lang="pt">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"></head>
<body style="margin:0;padding:0;background:#08080c;font-family:'Segoe UI',sans-serif;">
  <div style="max-width:520px;margin:40px auto;background:#0f0f15;border:1px solid rgba(212,175,55,0.2);border-radius:16px;overflow:hidden;">
    <div style="background:linear-gradient(135deg,#1a1a24,#0f0f15);padding:32px 40px;border-bottom:1px solid rgba(212,175,55,0.15);text-align:center;">
      <span style="font-size:2rem;">🎬</span>
      <h1 style="color:#d4af37;font-size:1.5rem;margin:8px 0 0;letter-spacing:0.05em;">CineMagIA</h1>
    </div>
    <div style="padding:36px 40px;">
      <h2 style="color:#e8e0d0;font-size:1.1rem;margin:0 0 12px;">Bem-vindo(a), {name}!</h2>
      <p style="color:#8a7a5a;font-size:0.95rem;line-height:1.6;margin:0 0 24px;">
        Obrigado por se cadastrar no CineMagIA. Clique no botão abaixo para confirmar seu e-mail e ativar sua conta.
      </p>
      <div style="text-align:center;margin:28px 0;">
        <a href="{url}" style="display:inline-block;padding:14px 32px;background:linear-gradient(135deg,#d4af37,#b8860b);color:#08080c;text-decoration:none;border-radius:10px;font-weight:600;font-size:0.95rem;letter-spacing:0.03em;">
          Confirmar meu e-mail
        </a>
      </div>
      <p style="color:#6b6050;font-size:0.82rem;line-height:1.6;margin:0;">
        ⏱ Este link expira em <strong style="color:#d4af37;">24 horas</strong>.<br>
        Se você não criou esta conta, ignore este e-mail.
      </p>
    </div>
    <div style="padding:16px 40px;border-top:1px solid rgba(255,255,255,0.04);text-align:center;">
      <p style="color:#3a3228;font-size:0.75rem;margin:0;">© CineMagIA · Todos os direitos reservados</p>
    </div>
  </div>
</body>
</html>
""",
    },
    "en": {
        "subject": "Confirm your email — CineMagIA",
        "body": lambda url, name: f"""
<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"></head>
<body style="margin:0;padding:0;background:#08080c;font-family:'Segoe UI',sans-serif;">
  <div style="max-width:520px;margin:40px auto;background:#0f0f15;border:1px solid rgba(212,175,55,0.2);border-radius:16px;overflow:hidden;">
    <div style="background:linear-gradient(135deg,#1a1a24,#0f0f15);padding:32px 40px;border-bottom:1px solid rgba(212,175,55,0.15);text-align:center;">
      <span style="font-size:2rem;">🎬</span>
      <h1 style="color:#d4af37;font-size:1.5rem;margin:8px 0 0;letter-spacing:0.05em;">CineMagIA</h1>
    </div>
    <div style="padding:36px 40px;">
      <h2 style="color:#e8e0d0;font-size:1.1rem;margin:0 0 12px;">Welcome, {name}!</h2>
      <p style="color:#8a7a5a;font-size:0.95rem;line-height:1.6;margin:0 0 24px;">
        Thank you for signing up to CineMagIA. Click the button below to confirm your email and activate your account.
      </p>
      <div style="text-align:center;margin:28px 0;">
        <a href="{url}" style="display:inline-block;padding:14px 32px;background:linear-gradient(135deg,#d4af37,#b8860b);color:#08080c;text-decoration:none;border-radius:10px;font-weight:600;font-size:0.95rem;letter-spacing:0.03em;">
          Confirm my email
        </a>
      </div>
      <p style="color:#6b6050;font-size:0.82rem;line-height:1.6;margin:0;">
        ⏱ This link expires in <strong style="color:#d4af37;">24 hours</strong>.<br>
        If you didn't create this account, you can safely ignore this email.
      </p>
    </div>
    <div style="padding:16px 40px;border-top:1px solid rgba(255,255,255,0.04);text-align:center;">
      <p style="color:#3a3228;font-size:0.75rem;margin:0;">© CineMagIA · All rights reserved</p>
    </div>
  </div>
</body>
</html>
""",
    },
    "es": {
        "subject": "Confirma tu correo — CineMagIA",
        "body": lambda url, name: f"""
<!DOCTYPE html>
<html lang="es">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"></head>
<body style="margin:0;padding:0;background:#08080c;font-family:'Segoe UI',sans-serif;">
  <div style="max-width:520px;margin:40px auto;background:#0f0f15;border:1px solid rgba(212,175,55,0.2);border-radius:16px;overflow:hidden;">
    <div style="background:linear-gradient(135deg,#1a1a24,#0f0f15);padding:32px 40px;border-bottom:1px solid rgba(212,175,55,0.15);text-align:center;">
      <span style="font-size:2rem;">🎬</span>
      <h1 style="color:#d4af37;font-size:1.5rem;margin:8px 0 0;letter-spacing:0.05em;">CineMagIA</h1>
    </div>
    <div style="padding:36px 40px;">
      <h2 style="color:#e8e0d0;font-size:1.1rem;margin:0 0 12px;">¡Bienvenido(a), {name}!</h2>
      <p style="color:#8a7a5a;font-size:0.95rem;line-height:1.6;margin:0 0 24px;">
        Gracias por registrarte en CineMagIA. Haz clic en el botón para confirmar tu correo y activar tu cuenta.
      </p>
      <div style="text-align:center;margin:28px 0;">
        <a href="{url}" style="display:inline-block;padding:14px 32px;background:linear-gradient(135deg,#d4af37,#b8860b);color:#08080c;text-decoration:none;border-radius:10px;font-weight:600;font-size:0.95rem;letter-spacing:0.03em;">
          Confirmar mi correo
        </a>
      </div>
      <p style="color:#6b6050;font-size:0.82rem;line-height:1.6;margin:0;">
        ⏱ Este enlace expira en <strong style="color:#d4af37;">24 horas</strong>.<br>
        Si no creaste esta cuenta, ignora este correo.
      </p>
    </div>
    <div style="padding:16px 40px;border-top:1px solid rgba(255,255,255,0.04);text-align:center;">
      <p style="color:#3a3228;font-size:0.75rem;margin:0;">© CineMagIA · Todos los derechos reservados</p>
    </div>
  </div>
</body>
</html>
""",
    },
}


TEMPLATES = {
    "pt": {
        "subject": "Recuperação de senha — CineMagIA",
        "body": lambda url, name: f"""
<!DOCTYPE html>
<html lang="pt">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"></head>
<body style="margin:0;padding:0;background:#08080c;font-family:'Segoe UI',sans-serif;">
  <div style="max-width:520px;margin:40px auto;background:#0f0f15;border:1px solid rgba(212,175,55,0.2);border-radius:16px;overflow:hidden;">
    <div style="background:linear-gradient(135deg,#1a1a24,#0f0f15);padding:32px 40px;border-bottom:1px solid rgba(212,175,55,0.15);text-align:center;">
      <span style="font-size:2rem;">🎬</span>
      <h1 style="color:#d4af37;font-size:1.5rem;margin:8px 0 0;letter-spacing:0.05em;">CineMagIA</h1>
    </div>
    <div style="padding:36px 40px;">
      <h2 style="color:#e8e0d0;font-size:1.1rem;margin:0 0 12px;">Olá, {name}!</h2>
      <p style="color:#8a7a5a;font-size:0.95rem;line-height:1.6;margin:0 0 24px;">
        Recebemos uma solicitação para redefinir a senha da sua conta CineMagIA.
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
      <p style="color:#3a3228;font-size:0.75rem;margin:0;">© CineMagIA · Todos os direitos reservados</p>
    </div>
  </div>
</body>
</html>
""",
    },
    "en": {
        "subject": "Password recovery — CineMagIA",
        "body": lambda url, name: f"""
<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"></head>
<body style="margin:0;padding:0;background:#08080c;font-family:'Segoe UI',sans-serif;">
  <div style="max-width:520px;margin:40px auto;background:#0f0f15;border:1px solid rgba(212,175,55,0.2);border-radius:16px;overflow:hidden;">
    <div style="background:linear-gradient(135deg,#1a1a24,#0f0f15);padding:32px 40px;border-bottom:1px solid rgba(212,175,55,0.15);text-align:center;">
      <span style="font-size:2rem;">🎬</span>
      <h1 style="color:#d4af37;font-size:1.5rem;margin:8px 0 0;letter-spacing:0.05em;">CineMagIA</h1>
    </div>
    <div style="padding:36px 40px;">
      <h2 style="color:#e8e0d0;font-size:1.1rem;margin:0 0 12px;">Hi, {name}!</h2>
      <p style="color:#8a7a5a;font-size:0.95rem;line-height:1.6;margin:0 0 24px;">
        We received a request to reset your CineMagIA account password.
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
      <p style="color:#3a3228;font-size:0.75rem;margin:0;">© CineMagIA · All rights reserved</p>
    </div>
  </div>
</body>
</html>
""",
    },
    "es": {
        "subject": "Recuperación de contraseña — CineMagIA",
        "body": lambda url, name: f"""
<!DOCTYPE html>
<html lang="es">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"></head>
<body style="margin:0;padding:0;background:#08080c;font-family:'Segoe UI',sans-serif;">
  <div style="max-width:520px;margin:40px auto;background:#0f0f15;border:1px solid rgba(212,175,55,0.2);border-radius:16px;overflow:hidden;">
    <div style="background:linear-gradient(135deg,#1a1a24,#0f0f15);padding:32px 40px;border-bottom:1px solid rgba(212,175,55,0.15);text-align:center;">
      <span style="font-size:2rem;">🎬</span>
      <h1 style="color:#d4af37;font-size:1.5rem;margin:8px 0 0;letter-spacing:0.05em;">CineMagIA</h1>
    </div>
    <div style="padding:36px 40px;">
      <h2 style="color:#e8e0d0;font-size:1.1rem;margin:0 0 12px;">¡Hola, {name}!</h2>
      <p style="color:#8a7a5a;font-size:0.95rem;line-height:1.6;margin:0 0 24px;">
        Recibimos una solicitud para restablecer la contraseña de tu cuenta CineMagIA.
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
      <p style="color:#3a3228;font-size:0.75rem;margin:0;">© CineMagIA · Todos los derechos reservados</p>
    </div>
  </div>
</body>
</html>
""",
    },
}


def _get_template(language: str) -> dict:
    return TEMPLATES.get(language, TEMPLATES["pt"])


def _get_verification_template(language: str) -> dict:
    return VERIFICATION_TEMPLATES.get(language, VERIFICATION_TEMPLATES["pt"])


# ── Serviço ───────────────────────────────────────────────────────────────────

class EmailService:

    def __init__(self, provider: IEmailProvider) -> None:
        self.provider = provider

    def send_password_reset_email(
        self,
        to:       str,
        name:     str,
        token:    str,
        language: str = "pt",
    ) -> None:
        """Envia o e-mail de recuperação de senha no idioma do usuário."""
        reset_url = f"{settings.FRONTEND_URL}/reset-password?token={token}"
        template  = _get_template(language)
        self.provider.send(to, template["subject"], template["body"](reset_url, name))

    def send_email_verification(
        self,
        to:       str,
        name:     str,
        token:    str,
        language: str = "pt",
    ) -> None:
        """Envia o e-mail de confirmação de cadastro no idioma do usuário."""
        verify_url = f"{settings.FRONTEND_URL}/verify-email?token={token}"
        template   = _get_verification_template(language)
        self.provider.send(to, template["subject"], template["body"](verify_url, name))
