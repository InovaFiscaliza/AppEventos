"""Determina os perfis disponíveis e os eventos acessíveis ao fiscal."""

from contextlib import closing
from dataclasses import dataclass
from typing import cast

from psycopg import sql

from src.infra.db_handler import DbRow
from src.modules.eventos.persistencia import EventoHandler

PERFIS_GLOBAIS = {"admin": "Administrador", "developer": "Desenvolvedor"}
PERFIS_EVENTO = {"fiscal": "Fiscal", "coordenador": "Coordenador"}


@dataclass
class AcessoEventos:
    """Reúne as opções verificadas no banco para o menu de eventos.

    Args:
        perfis (dict[str, str]): Identificadores e rótulos dos perfis disponíveis.
        perfil (str): Identificador do perfil em uso após verificar a autorização.
        eventos (list[DbRow]): IDs e nomes dos eventos acessíveis no perfil em uso.

    Returns:
        AcessoEventos: Opções disponíveis para a sessão autenticada.
    """

    perfis: dict[str, str]
    perfil: str
    eventos: list[DbRow]


def consultar_acesso_eventos(id_fiscal: int, perfil: str) -> AcessoEventos:
    """Consulta a autorização vigente para navegar pelos eventos.

    O vínculo no evento dá acesso como Fiscal. A coordenação exige o indicador
    no mesmo vínculo. Papéis globais ativos dão acesso à lista completa.

    Args:
        id_fiscal (int): Identificador do fiscal autenticado.
        perfil (str): Perfil solicitado ou armazenado na sessão.

    Returns:
        AcessoEventos: Opções atuais. Um perfil indisponível recua para Fiscal.

    Raises:
        psycopg.Error: Se a consulta ao banco falhar.
    """
    with closing(EventoHandler()) as banco:
        papeis = banco._select_raw(
            sql.SQL("""
                SELECT papel."NA_ROLE"
                FROM "SC_EVENTOS"."TB_FISCAL_ROLE" AS vinculo
                JOIN "SC_EVENTOS"."TB_ROLES" AS papel
                    ON papel."ID_ROLE" = vinculo."FK_ROLE"
                WHERE vinculo."ID_FISCAL" = %s AND vinculo."IS_ACTIVE"
            """),
            (id_fiscal,),
        )
        globais = {cast(str, papel["NA_ROLE"]) for papel in papeis}
        globais &= PERFIS_GLOBAIS.keys()
        acesso_global = perfil in globais
        eventos = banco._select_raw(
            sql.SQL("""
                SELECT evento."ID_EVENTO", evento."NO_EVENTO",
                       equipe."ID_FISCAL", equipe."IC_COORDENACAO"
                FROM "SC_EVENTOS"."TB_EVENTO" AS evento
                LEFT JOIN "SC_EVENTOS"."TB_EVENTO_FISCAL" AS equipe
                    ON equipe."ID_EVENTO" = evento."ID_EVENTO"
                    AND equipe."ID_FISCAL" = %s
                WHERE %s OR equipe."ID_FISCAL" IS NOT NULL
                ORDER BY evento."NO_EVENTO", evento."ID_EVENTO"
            """),
            (id_fiscal, acesso_global),
        )

    coordenados = [evento for evento in eventos if evento["IC_COORDENACAO"] == 1]
    perfis = {"fiscal": PERFIS_EVENTO["fiscal"]}
    if coordenados:
        perfis["coordenador"] = PERFIS_EVENTO["coordenador"]
    perfis.update({chave: rotulo for chave, rotulo in PERFIS_GLOBAIS.items() if chave in globais})
    if perfil not in perfis:
        perfil = "fiscal"
    return AcessoEventos(perfis, perfil, coordenados if perfil == "coordenador" else eventos)
