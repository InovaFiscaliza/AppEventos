"""Exibe a navegação de cadastro e as páginas dos formulários em preparação."""

from pathlib import Path

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from src.modules.sessao import sessao_fiscal

router = APIRouter(dependencies=[Depends(sessao_fiscal.sincronizar_sessao_rf_fusion)])
templates = Jinja2Templates(
    directory=Path(__file__).resolve().parent.parent / "templates",
    context_processors=[sessao_fiscal.contexto_perfil_cabecalho],
)


@router.get("/cadastro", response_class=HTMLResponse, name="cadastro")
@router.get("/cadastro/teste-e-etiquetagem", response_class=HTMLResponse, name="cadastro_teste_etiquetagem")
@router.get("/cadastro/incidente", response_class=HTMLResponse, name="cadastro_incidente")
@router.get("/cadastro/emissao-suspeita", response_class=HTMLResponse, name="cadastro_emissao_suspeita")
def exibir_cadastro(request: Request) -> HTMLResponse:
    """Exibe o menu e indica o tipo selecionado, quando houver.

    Args:
        request (Request): Requisição da página inicial ou de um tipo de cadastro.

    Returns:
        HTMLResponse: Menu de cadastro com a página selecionada.
    """
    rota = request.scope["route"].path
    tipo = rota.removeprefix("/cadastro").lstrip("/")
    return templates.TemplateResponse(
        request=request, name="cadastro/base.html", context={"tipo_cadastro": tipo}
    )
