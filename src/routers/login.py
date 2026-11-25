"""Pagina inicial da aplicacao."""

from hmac import compare_digest
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from src.config import ANATEL_PROXY_TOKEN, URL_ACESSO_ANATEL
from src.services.users import perfil_anatel
from src.services.users import usuarios as servico_usuarios

router = APIRouter()
templates = Jinja2Templates(
    directory=Path(__file__).resolve().parent.parent / "templates",
    context_processors=[perfil_anatel.contexto_perfil_cabecalho],
)
templates.env.globals["url_acesso_anatel"] = URL_ACESSO_ANATEL


class FormularioRFFusion(BaseModel):
    NA_USER_EMAIL: str = Field(max_length=254)
    NA_USER_NAME: str = Field(max_length=200)
    NA_DEPARTMENT: str | None = Field(default=None, max_length=200)
    NA_JOB_TITLE: str | None = Field(default=None, max_length=200)
    NA_LOCATION: str | None = Field(default=None, max_length=200)


def renderizar_login(
    request: Request,
    erro: str | None = None,
    status_code: int = 200,
) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={"erro": erro},
        status_code=status_code,
        headers={"Cache-Control": "no-store"},
    )


@router.get("/", response_class=HTMLResponse, response_model=None)
def login(request: Request) -> HTMLResponse | RedirectResponse:
    """Exibe a página inicial e aproveita a sessão corporativa existente."""
    if request.session.get("id_fiscal"):
        return renderizar_login(request)

    if not request.session.get("login_automatico_desativado"):
        return iniciar_sessao_anatel(request, interativo=False)
    return renderizar_login(request)


@router.get("/entrar/anatel", name="entrar_anatel", response_model=None)
def entrar_anatel(request: Request) -> HTMLResponse | RedirectResponse:
    """Confirma a sessão corporativa e sincroniza o fiscal autenticado."""
    return iniciar_sessao_anatel(request, interativo=True)


def iniciar_sessao_anatel(
    request: Request, *, interativo: bool
) -> HTMLResponse | RedirectResponse:
    cabecalho = request.headers.get("x-user-profile")
    token = request.headers.get("x-appeventos-proxy-token", "")
    if not (
        cabecalho
        and ANATEL_PROXY_TOKEN
        and compare_digest(token.encode(), ANATEL_PROXY_TOKEN.encode())
    ):
        if URL_ACESSO_ANATEL and interativo:
            return RedirectResponse(
                URL_ACESSO_ANATEL, status_code=303, headers={"Cache-Control": "no-store"}
            )
        if interativo:
            return renderizar_login(request, "Acesso Anatel indisponível.", 503)
        return renderizar_login(request)

    try:
        perfil = perfil_anatel.interpretar_perfil(cabecalho)
    except perfil_anatel.PerfilInvalido:
        return renderizar_login(request, "Perfil Anatel inválido.", 502)

    gravar_sessao_fiscal(request, perfil)
    if interativo:
        return RedirectResponse(url=request.url_for("login"), status_code=303)
    return renderizar_login(request)


def gravar_sessao_fiscal(request: Request, perfil: dict) -> None:
    fiscal = servico_usuarios.sincronizar_fiscal(perfil)
    request.session.clear()
    request.session["id_fiscal"] = fiscal
    request.session["perfil_anatel"] = {
        campo: perfil[campo] for campo in ("nome", "cargo", "departamento")
    }


@router.post(
    "/api/usuarios/login-evento",
    status_code=303,
    response_class=RedirectResponse,
)
def receber_perfil_rf_fusion(
    request: Request,
    formulario: Annotated[FormularioRFFusion, Form()],
) -> RedirectResponse:
    """Cadastra o perfil recebido e redireciona o navegador."""
    try:
        perfil = perfil_anatel.validar_perfil(formulario.model_dump())
    except perfil_anatel.PerfilInvalido as erro:
        raise HTTPException(400, "Perfil do RF.Fusion inválido.") from erro

    servico_usuarios.cadastrar_fiscal(perfil)

    caminho = request.url_for("login").path
    resposta = RedirectResponse(caminho, status_code=303, headers={"Cache-Control": "no-store"})
    resposta.set_cookie(
        perfil_anatel.COOKIE_PREVIA,
        perfil_anatel.previas_rf_fusion.dumps({"nome": perfil["nome"]}),
        max_age=perfil_anatel.PRAZO_PREVIA,
        path=caminho,
        httponly=True,
        secure=request.url.scheme == "https",
        samesite="lax",
    )
    return resposta


@router.get("/sair", name="sair")
async def sair(request: Request) -> RedirectResponse:
    """Encerra a sessão e volta ao login."""
    request.session.clear()
    request.session["login_automatico_desativado"] = True
    destino = request.url_for("login").path
    resposta = RedirectResponse(destino, status_code=303)
    resposta.delete_cookie(perfil_anatel.COOKIE_PREVIA, path=destino)
    return resposta
