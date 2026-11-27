"""Identifica o município de um ponto em duas etapas.

O serviço geográfico do Ibama fornece os códigos IBGE dos polígonos que
intersectam o ponto. A tabela TB_MUNICIPIO confirma quais desses códigos estão
cadastrados no AppEventos e fornece o nome e a UF para exibição.
"""

from typing import cast

from src.infra.db_handler import DbHandler
from src.infra.logging_utils import log
from src.infra.postgres import conninfo
from src.utils.api_municipios import localizar_codigos


def buscar_municipio_unico(codigos: list[int]) -> dict[str, int | str] | None:
    """Identifica uma única correspondência no cadastro de municípios.

    Args:
        codigos (list[int]): Códigos IBGE retornados pelo serviço geográfico.

    Returns:
        dict[str, int | str] | None: Registro com `codigo`, `nome` e `uf`
            quando há uma única correspondência em TB_MUNICIPIO. Retorna None
            quando não há correspondência ou quando há mais de uma.

    Raises:
        psycopg.Error: Se a conexão com o PostgreSQL ou a consulta falhar.
    """
    # A conexão é aberta sob demanda e liberada ao fim da leitura.
    banco = DbHandler(
        "SC_EVENTOS",
        log("appeventos_db", verbose={"error": True}, target_screen=True),
        conninfo=conninfo(),
        reuse_connection=False,
    )
    # Duas linhas bastam para detectar uma correspondência ambígua.
    municipios = banco._select_batch(
        "TB_MUNICIPIO",
        where={"CO_MUNICIPIO_IBGE__in": codigos},
        columns={
            "codigo": ("TB_MUNICIPIO", "CO_MUNICIPIO_IBGE"),
            "nome": ("TB_MUNICIPIO", "NO_MUNICIPIO"),
            "uf": ("TB_MUNICIPIO", "SG_UF"),
        },
        limit=2,
    )
    return cast(dict[str, int | str], municipios[0]) if len(municipios) == 1 else None


def identificar_municipio(latitude: float, longitude: float) -> dict[str, int | str] | None:
    """Identifica o município cadastrado que contém as coordenadas.

    Args:
        latitude (float): Latitude em graus decimais.
        longitude (float): Longitude em graus decimais.

    Returns:
        dict[str, int | str] | None: Código IBGE, nome e UF se a correspondência
            for única. Retorna None se o ponto estiver fora da malha ou for ambíguo.

    Raises:
        ValueError: Se uma coordenada estiver fora do intervalo válido.
        RuntimeError: Se a consulta ao Ibama falhar.
        psycopg.Error: Se a consulta ao cadastro falhar.
    """
    codigos = localizar_codigos(latitude, longitude)
    return buscar_municipio_unico(codigos) if codigos else None
