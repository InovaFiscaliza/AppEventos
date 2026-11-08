"""Cadastro de eventos."""

from datetime import date
from pathlib import Path

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import text

from app.services.db import engine

router = APIRouter(prefix="/eventos")
templates = Jinja2Templates(
    directory=Path(__file__).resolve().parent.parent / "templates"
)


@router.get("/novo", response_class=HTMLResponse, name="novo_evento")
async def novo_evento(request: Request) -> HTMLResponse:
    """Exibe o formulário de criação de evento."""
    return templates.TemplateResponse(request=request, name="evento_novo.html")


def converter_data(valor: str) -> date | None:
    """Converte a data do formulário; campo vazio vira None."""
    return date.fromisoformat(valor) if valor else None


@router.post("/novo", name="salvar_evento", response_model=None)
async def salvar_evento(
    request: Request,
    nome: str = Form(""),
    data_inicio: str = Form(""),
    data_fim: str = Form(""),
) -> HTMLResponse | RedirectResponse:
    """Grava o novo evento e volta para o login."""
    nome = nome.strip()
    inicio = converter_data(data_inicio)
    fim = converter_data(data_fim)

    erro = None
    if not nome:
        erro = "Informe o nome do evento."
    elif inicio and fim and fim < inicio:
        erro = "A data de fim não pode ser anterior à data de início."

    if erro:
        return templates.TemplateResponse(
            request=request,
            name="evento_novo.html",
            context={
                "erro": erro,
                "nome": nome,
                "data_inicio": data_inicio,
                "data_fim": data_fim,
            },
            status_code=400,
        )

    with engine.begin() as conexao:
        conexao.execute(
            text(
                "INSERT INTO TB_EVENTO (NO_EVENTO, DT_INICIO, DT_FIM) "
                "VALUES (:nome, :inicio, :fim)"
            ),
            {"nome": nome, "inicio": inicio, "fim": fim},
        )
    return RedirectResponse(url="/", status_code=303)
