"""Pagina inicial da aplicacao."""

from pathlib import Path

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.config import USUARIO_CADASTRO
from app.services import usuarios as servico_usuarios

router = APIRouter()
templates = Jinja2Templates(
    directory=Path(__file__).resolve().parent.parent / "templates"
)


def renderizar_menu(
    request: Request, erro: str | None = None, status_code: int = 200
) -> HTMLResponse:
    """Monta a tela de login com a lista de usuários."""
    return templates.TemplateResponse(
        request=request,
        name="menu.html",
        context={
            "usuarios": servico_usuarios.listar_usuarios(),
            # "Cadastrar Usuário" só aparece enquanto não houver nenhum usuário.
            "usuario_cadastro": (
                None if servico_usuarios.existe_usuario() else USUARIO_CADASTRO
            ),
            "erro": erro,
        },
        status_code=status_code,
    )


@router.get("/", response_class=HTMLResponse)
async def menu(request: Request) -> HTMLResponse:
    """Exibe a pagina inicial."""
    return renderizar_menu(request)


@router.post("/entrar", name="entrar", response_model=None)
async def entrar(
    request: Request,
    usuario: str = Form(""),
    senha: str = Form(""),
) -> HTMLResponse | RedirectResponse:
    """Libera a tela de cadastro para o usuário administrativo."""
    # Com usuário cadastrado a opção some da tela, então o login dela também é recusado.
    if usuario != USUARIO_CADASTRO or servico_usuarios.existe_usuario():
        return renderizar_menu(request, "Login ainda não configurado.", 400)
    if not servico_usuarios.senha_cadastro_confere(senha):
        return renderizar_menu(request, "Senha inválida.", 401)

    # Esta chave é o que cadastro_liberado() confere em /usuarios.
    request.session["usuario"] = USUARIO_CADASTRO
    return RedirectResponse(url=request.url_for("usuarios"), status_code=303)


@router.get("/sair", name="sair")
async def sair(request: Request) -> RedirectResponse:
    """Encerra a sessão e volta ao login."""
    request.session.clear()
    return RedirectResponse(url=request.url_for("menu"), status_code=303)
