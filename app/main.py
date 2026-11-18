"""Configuracao principal da aplicacao web."""

from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from app.config import SESSION_SECRET
from app.routers import evento, login, usuario

APP_DIR = Path(__file__).resolve().parent

app = FastAPI(title="AppGrandesEventos")
# Cookie assinado guarda quem fez login; same_site="lax" barra POST vindo de outros sites.
app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET, same_site="lax")
app.mount("/static", StaticFiles(directory=APP_DIR / "static"), name="static")
# Sem prefix: a rota "/" de app/routers/login.py (linha 38) vira a pagina inicial.
app.include_router(login.router)
app.include_router(evento.router)
app.include_router(usuario.router)

# login anatel
# https://fiscalizacao.anatel.gov.br/rffusion/api/users/me
# https://appsnet/acesso/