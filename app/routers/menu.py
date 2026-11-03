"""Pagina inicial da aplicacao."""

from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(
    directory=Path(__file__).resolve().parent.parent / "templates"
)


@router.get("/", response_class=HTMLResponse)
async def menu(request: Request) -> HTMLResponse:
    """Exibe a pagina inicial."""
    return templates.TemplateResponse(request=request, name="menu.html")
