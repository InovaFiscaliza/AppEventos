"""Verifica a persistência do login com o driver PostgreSQL simulado."""

from unittest.mock import MagicMock

import pytest
from psycopg.pq import TransactionStatus

from src.db import dbHandlerBase
from src.services.users import usuarios


@pytest.mark.parametrize("retornou_id", [True, False])
def test_sincronizacao_retorna_id_e_fecha_transacao(monkeypatch, retornou_id):
    conexao = MagicMock(closed=False, broken=False)
    conexao.info.transaction_status = TransactionStatus.IDLE
    cursor = conexao.cursor.return_value.__enter__.return_value
    fiscal = [{"ID_FISCAL": 42}]
    cursor.fetchall.side_effect = [fiscal] if retornou_id else [[], fiscal]
    monkeypatch.setattr(dbHandlerBase.psycopg.Connection, "connect", MagicMock(return_value=conexao))
    monkeypatch.setattr(usuarios, "conninfo", lambda: "dbname=teste")

    assert usuarios.sincronizar_fiscal({
        "email": "Fiscal@example.test",
        "nome": "Fiscal Teste",
        "departamento": None,
        "cargo": "Cargo",
        "local": "Local",
    }) == 42

    primeira_consulta = cursor.execute.call_args_list[0]
    sql_gravacao, parametros = primeira_consulta.args
    assert 'INSERT INTO "SC_EVENTOS"."TB_FISCAL"' in sql_gravacao.as_string()
    assert 'ON CONFLICT (lower("NA_FISCAL_EMAIL"))' in sql_gravacao.as_string()
    assert 'IS DISTINCT FROM' in sql_gravacao.as_string()
    assert parametros == ("Fiscal@example.test", "Fiscal Teste", None, "Cargo", "Local")
    assert cursor.execute.call_count == (1 if retornou_id else 2)
    if not retornou_id:
        sql_busca, parametros = cursor.execute.call_args.args
        assert 'WHERE lower("NA_FISCAL_EMAIL") = lower(%s)' in sql_busca.as_string()
        assert parametros == ("Fiscal@example.test",)
    conexao.commit.assert_called_once()
    conexao.close.assert_called_once()
