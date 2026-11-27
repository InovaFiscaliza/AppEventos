"""Sessão fiscal vinculada à identidade do RF.Fusion."""

from fastapi import HTTPException, Request
from psycopg import Error

from src.modules.eventos.acesso import consultar_acesso_eventos
from src.modules.fiscais import acesso_corporativo, persistencia


def sincronizar_sessao_rf_fusion(request: Request) -> None:
    """Vincula a sessão ao fiscal identificado no cabeçalho da requisição.

    Args:
        request (Request): Requisição encaminhada pelo F5.

    Returns:
        None.

    Raises:
        HTTPException: Com status 503 quando o cadastro do fiscal falhar.
    """
    perfil = acesso_corporativo.ler_perfil_rf_fusion(request.headers)
    if perfil is None:
        request.session.clear()
        return

    try:
        fiscal = persistencia.sincronizar_fiscal(perfil)
    except Error as erro:
        request.session.clear()
        raise HTTPException(503, "Não foi possível sincronizar o fiscal.") from erro

    if request.session.get("identidade_rf_fusion") != perfil["email"] or (
        request.session.get("id_fiscal") != fiscal
    ):
        request.session.clear()
    request.session["identidade_rf_fusion"] = perfil["email"]
    request.session["id_fiscal"] = fiscal
    request.session["perfil_anatel"] = {
        campo: perfil[campo] for campo in ("nome", "cargo", "departamento")
    }


def contexto_perfil_cabecalho(request: Request) -> dict:
    """Monta o cabeçalho com perfil e eventos autorizados para a sessão.

    Args:
        request (Request): Requisição usada para ler a sessão do fiscal.

    Returns:
        dict: Perfil visível, opções autorizadas e evento ativo.
    """
    perfil = request.session.get("perfil_anatel")
    contexto = {"perfil_cabecalho": perfil}
    id_fiscal = request.session.get("id_fiscal")
    if id_fiscal is None:
        return contexto
    try:
        acesso = consultar_acesso_eventos(id_fiscal, request.session.get("perfil_ativo", "fiscal"))
    except Error:
        return {**contexto, "eventos_indisponiveis": True}

    id_evento = request.session.get("id_evento")
    if not any(evento["ID_EVENTO"] == id_evento for evento in acesso.eventos):
        id_evento = None
    return {**contexto, "acesso_eventos": acesso, "evento_ativo": id_evento}
