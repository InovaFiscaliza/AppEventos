"""Normaliza a identidade que o F5 encaminha para o AppEventos."""

import re
from collections.abc import Mapping
from urllib.parse import urlsplit


def _texto_cabecalho(valor: str) -> str | None:
    # ASGI preserva os bytes do proxy e Starlette os apresenta como Latin-1.
    try:
        valor = valor.encode("latin-1").decode("utf-8")
    except UnicodeError:
        pass
    valor = valor.strip()
    return valor if valor and not any(ord(caractere) < 32 for caractere in valor) else None


def _url_avatar(valor: str | None) -> str | None:
    if not valor or len(valor) > 2048:
        return None
    try:
        url = urlsplit(valor)
    except ValueError:
        return None
    if url.scheme == "https" and url.hostname and not (
        url.username or url.password or url.query or url.fragment or "@" in url.netloc
    ):
        return valor
    return None


def ler_perfil_rf_fusion(cabecalhos: Mapping[str, str]) -> dict[str, str | None] | None:
    """Extrai e normaliza a identidade encaminhada nos cabeçalhos do RF.Fusion.

    Args:
        cabecalhos (Mapping[str, str]): Cabeçalhos HTTP da requisição.

    Returns:
        dict[str, str | None] | None: Perfil normalizado ou None quando
            nome ou e-mail estiverem ausentes ou inválidos.
    """
    nome = _texto_cabecalho(cabecalhos.get("x-user-name", ""))
    email = _texto_cabecalho(cabecalhos.get("x-user-email", ""))
    if not nome or len(nome) > 200 or not email or not re.fullmatch(r"[^@\s]+@[^@\s]+", email):
        return None
    email = email.lower()
    if len(email) > 254:
        return None
    return {
        "nome": nome,
        "email": email,
        "cargo": _texto_cabecalho(cabecalhos.get("x-user-job-title", "")),
        "departamento": _texto_cabecalho(cabecalhos.get("x-user-department", "")),
        "local": _texto_cabecalho(cabecalhos.get("x-user-location", "")),
        "avatar_url": _url_avatar(_texto_cabecalho(cabecalhos.get("x-user-avatar-url", ""))),
    }
