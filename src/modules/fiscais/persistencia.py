"""Cadastro e sincronização de fiscais."""

from contextlib import closing
from typing import cast

from psycopg import sql

from src.infra.db_handler import DbHandler, DbRow
from src.infra.logging_utils import log
from src.infra.postgres import conninfo


class FiscalHandler(DbHandler):
    """Operações de cadastro no esquema de eventos."""

    def __init__(self) -> None:
        super().__init__(
            "SC_EVENTOS",
            log("appeventos_db", verbose={"error": True}, target_screen=True),
            conninfo=conninfo(),
            reuse_connection=False,
        )

    def listar_fiscais_para_evento(self) -> list[DbRow]:
        """Lista os fiscais disponíveis no seletor de responsável.

        Args:
            None.

        Returns:
            list[DbRow]: Identificadores e nomes em ordem alfabética.
        """
        return self._select_batch(
            "TB_FISCAL",
            columns=("ID_FISCAL", "NO_FISCAL"),
            order_by=(("NO_FISCAL", "ASC"), ("ID_FISCAL", "ASC")),
        )

    def sincronizar_fiscal(self, perfil: dict) -> int:
        """Insere ou atualiza o fiscal identificado pelo e-mail do RF.Fusion.

        Args:
            perfil (dict): Nome e e-mail validados e dados opcionais de cargo,
                departamento, local e avatar.

        Returns:
            int: Identificador do fiscal cadastrado ou já existente.

        Raises:
            psycopg.Error: Se a sincronização no banco falhar.
        """
        tabela = self._table_identifier("TB_FISCAL")
        with self._unit_of_work():
            linhas = self._select_raw(sql.SQL("""
                INSERT INTO {} AS fiscal
                    ("NA_FISCAL_EMAIL", "NO_FISCAL", "NA_DEPARTMENT", "NA_JOB_TITLE", "NA_LOCATION",
                     "NA_URL_PROFILE_IMG")
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (lower("NA_FISCAL_EMAIL")) DO UPDATE SET
                    "NA_FISCAL_EMAIL" = EXCLUDED."NA_FISCAL_EMAIL",
                    "NO_FISCAL" = EXCLUDED."NO_FISCAL",
                    "NA_DEPARTMENT" = EXCLUDED."NA_DEPARTMENT",
                    "NA_JOB_TITLE" = EXCLUDED."NA_JOB_TITLE",
                    "NA_LOCATION" = EXCLUDED."NA_LOCATION",
                    "NA_URL_PROFILE_IMG" = EXCLUDED."NA_URL_PROFILE_IMG",
                    "DT_UPDATED_AT" = now()
                WHERE (fiscal."NA_FISCAL_EMAIL", fiscal."NO_FISCAL", fiscal."NA_DEPARTMENT",
                       fiscal."NA_JOB_TITLE", fiscal."NA_LOCATION", fiscal."NA_URL_PROFILE_IMG")
                    IS DISTINCT FROM
                      (EXCLUDED."NA_FISCAL_EMAIL", EXCLUDED."NO_FISCAL", EXCLUDED."NA_DEPARTMENT",
                       EXCLUDED."NA_JOB_TITLE", EXCLUDED."NA_LOCATION", EXCLUDED."NA_URL_PROFILE_IMG")
                RETURNING "ID_FISCAL"
            """).format(tabela), (
                perfil["email"], perfil["nome"], perfil["departamento"],
                perfil["cargo"], perfil["local"], perfil.get("avatar_url"),
            ))
            if not linhas:
                linhas = self._select_raw(sql.SQL("""
                    SELECT "ID_FISCAL" FROM {}
                    WHERE lower("NA_FISCAL_EMAIL") = lower(%s)
                """).format(tabela), (perfil["email"],))
            return cast(int, linhas[0]["ID_FISCAL"])


def listar_fiscais_para_evento() -> list[DbRow]:
    """Retorna os fiscais disponíveis para compor a equipe do evento.

    Args:
        None.

    Returns:
        list[DbRow]: IDs e nomes em ordem alfabética. Pode ser vazia.

    Raises:
        psycopg.Error: Se a consulta ao PostgreSQL falhar.
    """
    with closing(FiscalHandler()) as handler:
        return handler.listar_fiscais_para_evento()


def sincronizar_fiscal(perfil: dict) -> int:
    """Sincroniza uma identidade do RF.Fusion e libera a sessão do banco.

    Args:
        perfil (dict): Dados de identidade normalizados.

    Returns:
        int: Identificador do fiscal.

    Raises:
        psycopg.Error: Se a sincronização no banco falhar.
    """
    with closing(FiscalHandler()) as handler:
        return handler.sincronizar_fiscal(perfil)

