"""Lista e inclusão de usuários."""

from pathlib import Path

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.config import PAPEIS_USUARIO, USUARIO_CADASTRO
from app.services import usuarios as servico_usuarios

router = APIRouter(prefix="/usuarios")
templates = Jinja2Templates(
    directory=Path(__file__).resolve().parent.parent / "templates"
)


def cadastro_liberado(request: Request) -> bool:
    """Somente o usuário "Cadastrar Usuário" acessa a tela de cadastro."""
    return request.session.get("usuario") == USUARIO_CADASTRO


def renderizar_cadastro(
    request: Request, status_code: int = 200, **formulario: object
) -> HTMLResponse:
    """Monta a tela de cadastro; formulario devolve os valores digitados."""
    return templates.TemplateResponse(
        request=request,
        name="usuarios.html",
        context={
            "usuarios": servico_usuarios.listar_usuarios(),
            "unidades": servico_usuarios.listar_unidades(),
            "papeis": PAPEIS_USUARIO,
            **formulario,
        },
        status_code=status_code,
    )


@router.get("", response_class=HTMLResponse, name="usuarios", response_model=None)
async def usuarios(request: Request) -> HTMLResponse | RedirectResponse:
    """Exibe a lista de usuários e o formulário de inclusão."""
    if not cadastro_liberado(request):
        return RedirectResponse(url=request.url_for("menu"), status_code=303)
    return renderizar_cadastro(
        request, sucesso=request.session.pop("flash_success", None)
    )


@router.post("", name="salvar_usuario", response_model=None)
async def salvar_usuario(
    request: Request,
    nome: str = Form(""),
    unidade: str = Form(""),
    papeis: list[str] = Form([]),
) -> HTMLResponse | RedirectResponse:
    """Inclui o usuário e volta para a lista."""
    # O POST também é protegido: sem isso bastaria enviar o formulário direto.
    if not cadastro_liberado(request):
        return RedirectResponse(url=request.url_for("menu"), status_code=303)

    nome = nome.strip()
    unidade = unidade.strip()
    # Descarta valores fora da lista da tela, caso o formulário seja adulterado.
    papeis_marcados = set(papeis) & PAPEIS_USUARIO.keys()
    siglas = {item["sigla"] for item in servico_usuarios.listar_unidades()}

    erro = None
    if not nome:
        erro = "Informe o nome do usuário."
    elif unidade not in siglas:
        erro = "Selecione a unidade executante."

    if erro:
        return renderizar_cadastro(
            request,
            status_code=400,
            erro=erro,
            nome=nome,
            unidade=unidade,
            papeis_marcados=papeis_marcados,
        )

    servico_usuarios.incluir_usuario(nome, unidade, papeis_marcados)
    # Mensagem lida e apagada na próxima exibição da tela, após o redirecionamento.
    request.session["flash_success"] = f"Usuário {nome} cadastrado."
    return RedirectResponse(url=request.url_for("usuarios"), status_code=303)
