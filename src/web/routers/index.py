"""Página inicial e seleção do contexto do AppEventos."""

from pathlib import Path

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from psycopg import Error

from src.modules.sessao import sessao_fiscal

router = APIRouter(dependencies=[Depends(sessao_fiscal.sincronizar_sessao_rf_fusion)])
templates = Jinja2Templates(
    directory=Path(__file__).resolve().parent.parent / "templates",
    context_processors=[sessao_fiscal.contexto_perfil_cabecalho],
)


@router.get("/", response_class=HTMLResponse, name="index")
def index(request: Request) -> HTMLResponse:
    """Exibe a página inicial com o contexto da identidade do RF.Fusion.

    Args:
        request (Request): Requisição com a sessão fiscal já sincronizada.

    Returns:
        HTMLResponse: Página inicial com o cabeçalho de eventos e perfis.
    """
    return templates.TemplateResponse(
        request=request, name="index.html", headers={"Cache-Control": "no-store"}
    )


@router.post("/contexto", name="selecionar_contexto")
def selecionar_contexto(
    request: Request,
    perfil: str | None = Form(None),
    id_evento: int | None = Form(None),
) -> RedirectResponse:
    """Atualiza o perfil ou o evento selecionado na sessão autenticada.

    Args:
        request (Request): Requisição que contém a sessão do fiscal.
        perfil (str | None): Perfil solicitado no menu do usuário.
        id_evento (int | None): Evento solicitado no seletor. Vazio limpa a seleção.

    Returns:
        RedirectResponse: Redirecionamento à página inicial após a seleção.

    Raises:
        HTTPException: Com status 401 sem sessão, 403 sem acesso ou 503
            se a autorização não puder ser consultada.
    """
    id_fiscal = request.session.get("id_fiscal")
    if id_fiscal is None:
        raise HTTPException(401, "Entre para selecionar um perfil ou evento.")

    perfil_solicitado = perfil if perfil is not None else request.session.get("perfil_ativo", "fiscal")
    try:
        acesso = sessao_fiscal.consultar_acesso_eventos(id_fiscal, perfil_solicitado)
    except Error as erro:
        raise HTTPException(503, "Não foi possível consultar o acesso aos eventos.") from erro

    if perfil is not None and perfil != acesso.perfil:
        raise HTTPException(403, "Perfil indisponível.")
    eventos_permitidos = {evento["ID_EVENTO"] for evento in acesso.eventos}
    if id_evento is not None and id_evento not in eventos_permitidos:
        raise HTTPException(403, "Evento indisponível neste perfil.")

    request.session["perfil_ativo"] = acesso.perfil
    selecionado = request.session.get("id_evento") if perfil is not None else id_evento
    if selecionado in eventos_permitidos:
        request.session["id_evento"] = selecionado
    else:
        request.session.pop("id_evento", None)
    return RedirectResponse(request.url_for("index"), status_code=303)
