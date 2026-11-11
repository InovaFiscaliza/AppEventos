"""Constantes e configurações centralizadas."""

import os
import secrets

# Chave do cookie de sessão; sem a variável, as sessões expiram ao reiniciar o servidor.
SESSION_SECRET = os.environ.get("SESSION_SECRET") or secrets.token_hex(32)

# Usuário administrativo que libera a tela de cadastro (ver docs/usuarios-de-acesso.md).
USUARIO_CADASTRO = "Cadastrar Usuário"
# SHA-256 da senha documentada, para não manter a senha em texto no código.
SENHA_CADASTRO_SHA256 = (
    "0f8eb4b72b6e0c9e88b388eb967b49e067ef1004bf07bffc22c3acb13b43580a"
)

# Papéis permitidos do usuário (colunas IC_* de TB_FISCAL), na ordem da tela.
PAPEIS_USUARIO = {
    "coordenacao": "Coordenação",
    "abordagem": "Abordagem",
    "monitoracao": "Monitoração",
}
