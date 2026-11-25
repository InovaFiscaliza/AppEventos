"""Validação do perfil corporativo entregue pelo proxy."""

import json

from fastapi import Request
from itsdangerous import BadData, URLSafeTimedSerializer

from src.config import SESSION_SECRET

COOKIE_PREVIA = "rf_fusion_previa"
PRAZO_PREVIA = 8 * 60 * 60
previas_rf_fusion = URLSafeTimedSerializer(SESSION_SECRET, salt="rf-fusion-previa")


def contexto_perfil_cabecalho(request: Request) -> dict:
    perfil = request.session.get("perfil_anatel")
    if not perfil:
        try:
            perfil = previas_rf_fusion.loads(
                request.cookies.get(COOKIE_PREVIA, ""), max_age=PRAZO_PREVIA
            )
        except BadData:
            perfil = None
    return {"perfil_cabecalho": perfil}


class PerfilInvalido(ValueError):
    """O cabeçalho do proxy não contém um perfil válido."""


def interpretar_perfil(cabecalho: str) -> dict:
    """Extrai os campos utilizados no cadastro de fiscais."""
    try:
        dados = json.loads(cabecalho)
    except ValueError as erro:
        raise PerfilInvalido from erro

    return validar_perfil(dados)


def validar_perfil(dados: object) -> dict:
    campos = {
        "email": "NA_USER_EMAIL",
        "nome": "NA_USER_NAME",
        "departamento": "NA_DEPARTMENT",
        "cargo": "NA_JOB_TITLE",
        "local": "NA_LOCATION",
    }
    if not isinstance(dados, dict) or not set(campos.values()) <= dados.keys():
        raise PerfilInvalido
    perfil = {campo: dados[origem] for campo, origem in campos.items()}
    if any(
        valor is not None and (not isinstance(valor, str) or "\0" in valor)
        for valor in perfil.values()
    ):
        raise PerfilInvalido
    nome = (perfil["nome"] or "").strip()
    email = (perfil["email"] or "").strip()
    if not nome or len(nome) > 200 or not email or len(email) > 254:
        raise PerfilInvalido
    perfil["nome"] = nome
    perfil["email"] = email
    return perfil
