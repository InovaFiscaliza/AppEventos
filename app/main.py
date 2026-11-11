"""Configuracao principal da aplicacao web."""

from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from app.config import SESSION_SECRET
from app.routers import evento, menu, usuario

APP_DIR = Path(__file__).resolve().parent

app = FastAPI(title="AppGrandesEventos")
# Cookie assinado guarda quem fez login; same_site="lax" barra POST vindo de outros sites.
app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET, same_site="lax")
app.mount("/static", StaticFiles(directory=APP_DIR / "static"), name="static")
app.include_router(menu.router)
app.include_router(evento.router)
app.include_router(usuario.router)
