"""Constantes e configurações centralizadas."""

import json
import os
import secrets
from pathlib import Path

_ARQUIVO_CREDENCIAIS_BANCO = Path(__file__).resolve().parent / ".secret" / ".secret_db"
try:
    _credenciais_banco = json.loads(
        _ARQUIVO_CREDENCIAIS_BANCO.read_text(encoding="utf-8")
    )
except FileNotFoundError:
    _credenciais_banco = {}

DB_CFG = {
    "address": "10.88.0.36",
    "port": 5432,
    "database": "DB_EVENTOS",
    "user": _credenciais_banco.get("user"),
    "password": _credenciais_banco.get("password"),
}

# Chave do cookie de sessão; sem a variável, as sessões expiram ao reiniciar o servidor.
SESSION_SECRET = os.environ.get("SESSION_SECRET") or secrets.token_hex(32)

# Endpoint corporativo para iniciar a autenticação.
URL_ACESSO_ANATEL = os.environ.get(
    "URL_ACESSO_ANATEL", "https://fiscalizacao.anatel.gov.br/rffusion/api/users/login_eventos"
)

# Credencial exclusiva do proxy que entrega o perfil autenticado.
ANATEL_PROXY_TOKEN = os.environ.get("ANATEL_PROXY_TOKEN", "")

# Papéis operacionais atribuídos no vínculo com o evento (TB_EVENTO_FISCAL).
PAPEIS_USUARIO = {
    "coordenacao": "Coordenação",
    "abordagem": "Abordagem",
    "monitoracao": "Monitoração",
}
