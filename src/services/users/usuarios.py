"""Cadastro e sincronização de fiscais."""

from contextlib import closing
from typing import cast

from psycopg import sql

from src.db.dbHandlerBase import DbHandler
from src.services.users.db import conninfo
from src.utils.logging_utils import log


class FiscalHandler(DbHandler):
    """Operações de cadastro no esquema de eventos."""

    def __init__(self) -> None:
        super().__init__(
            "SC_EVENTOS",
            log("appeventos_db", verbose={"error": True}, target_screen=True),
            conninfo=conninfo(),
            reuse_connection=False,
        )

    def cadastrar_fiscal(self, perfil: dict) -> None:
        """Insere um perfil recebido e preserva registros já cadastrados."""
        self._insert_row(
            "TB_FISCAL",
            {
                "NA_FISCAL_EMAIL": perfil["email"],
                "NO_FISCAL": perfil["nome"],
                "NA_DEPARTMENT": perfil["departamento"],
                "NA_JOB_TITLE": perfil["cargo"],
                "NA_LOCATION": perfil["local"],
            },
            skip_duplicates=True,
        )

    def sincronizar_fiscal(self, perfil: dict) -> int:
        """Insere ou atualiza o perfil corporativo identificado pelo e-mail."""
        tabela = self._table_identifier("TB_FISCAL")
        with self._unit_of_work():
            linhas = self._select_raw(sql.SQL("""
                INSERT INTO {} AS fiscal
                    ("NA_FISCAL_EMAIL", "NO_FISCAL", "NA_DEPARTMENT", "NA_JOB_TITLE", "NA_LOCATION")
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (lower("NA_FISCAL_EMAIL")) DO UPDATE SET
                    "NA_FISCAL_EMAIL" = EXCLUDED."NA_FISCAL_EMAIL",
                    "NO_FISCAL" = EXCLUDED."NO_FISCAL",
                    "NA_DEPARTMENT" = EXCLUDED."NA_DEPARTMENT",
                    "NA_JOB_TITLE" = EXCLUDED."NA_JOB_TITLE",
                    "NA_LOCATION" = EXCLUDED."NA_LOCATION",
                    "DT_UPDATED_AT" = now()
                WHERE (fiscal."NA_FISCAL_EMAIL", fiscal."NO_FISCAL", fiscal."NA_DEPARTMENT",
                       fiscal."NA_JOB_TITLE", fiscal."NA_LOCATION")
                    IS DISTINCT FROM
                      (EXCLUDED."NA_FISCAL_EMAIL", EXCLUDED."NO_FISCAL", EXCLUDED."NA_DEPARTMENT",
                       EXCLUDED."NA_JOB_TITLE", EXCLUDED."NA_LOCATION")
                RETURNING "ID_FISCAL"
            """).format(tabela), (
                perfil["email"], perfil["nome"], perfil["departamento"],
                perfil["cargo"], perfil["local"],
            ))
            if not linhas:
                linhas = self._select_raw(sql.SQL("""
                    SELECT "ID_FISCAL" FROM {}
                    WHERE lower("NA_FISCAL_EMAIL") = lower(%s)
                """).format(tabela), (perfil["email"],))
            return cast(int, linhas[0]["ID_FISCAL"])


def sincronizar_fiscal(perfil: dict) -> int:
    with closing(FiscalHandler()) as handler:
        return handler.sincronizar_fiscal(perfil)


def cadastrar_fiscal(perfil: dict) -> None:
    with closing(FiscalHandler()) as handler:
        handler.cadastrar_fiscal(perfil)
