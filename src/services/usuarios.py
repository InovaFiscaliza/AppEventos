"""Cadastro de usuários gravado em TB_FISCAL, com os papéis permitidos."""

import hashlib
import hmac

from sqlalchemy import text

from app.config import SENHA_CADASTRO_SHA256
from app.services.db import engine


def existe_usuario() -> bool:
    """Indica se já há algum usuário cadastrado."""
    with engine.connect() as conexao:
        return bool(
            conexao.execute(text("SELECT EXISTS (SELECT 1 FROM TB_FISCAL)")).scalar()
        )


def listar_usuarios() -> list[dict]:
    """Retorna os usuários e seus papéis em ordem alfabética de nome."""
    with engine.connect() as conexao:
        linhas = conexao.execute(
            text(
                "SELECT NO_FISCAL AS nome, SG_UNIDADE_EXECUTANTE AS unidade, "
                "IC_COORDENACAO AS coordenacao, IC_ABORDAGEM AS abordagem, "
                "IC_MONITORACAO AS monitoracao "
                "FROM TB_FISCAL ORDER BY lower(NO_FISCAL)"
            )
        ).mappings()
        return [dict(linha) for linha in linhas]


def listar_unidades() -> list[dict[str, str]]:
    """Retorna as unidades executantes cadastradas, por sigla."""
    with engine.connect() as conexao:
        linhas = conexao.execute(
            text(
                "SELECT SG_UNIDADE_EXECUTANTE AS sigla, NO_UNIDADE_EXECUTANTE AS nome "
                "FROM TB_UNIDADE_EXECUTANTE ORDER BY SG_UNIDADE_EXECUTANTE"
            )
        ).mappings()
        return [dict(linha) for linha in linhas]


def incluir_usuario(nome: str, unidade: str, papeis: set[str]) -> None:
    """Grava o usuário em TB_FISCAL; papéis não marcados ficam 0."""
    with engine.begin() as conexao:
        conexao.execute(
            text(
                "INSERT INTO TB_FISCAL (NO_FISCAL, SG_UNIDADE_EXECUTANTE, "
                "IC_COORDENACAO, IC_ABORDAGEM, IC_MONITORACAO) "
                "VALUES (:nome, :unidade, :coordenacao, :abordagem, :monitoracao)"
            ),
            {
                "nome": nome,
                "unidade": unidade,
                "coordenacao": int("coordenacao" in papeis),
                "abordagem": int("abordagem" in papeis),
                "monitoracao": int("monitoracao" in papeis),
            },
        )


def senha_cadastro_confere(senha: str) -> bool:
    """Compara a senha informada com a do usuário "Cadastrar Usuário"."""
    informada = hashlib.sha256(senha.encode()).hexdigest()
    # compare_digest leva o mesmo tempo para qualquer senha, evitando ataque de tempo.
    return hmac.compare_digest(informada, SENHA_CADASTRO_SHA256)
