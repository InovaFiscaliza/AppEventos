"""Configuracao principal da aplicacao web."""

from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routers import evento, menu

APP_DIR = Path(__file__).resolve().parent

app = FastAPI(title="AppGrandesEventos")
app.mount("/static", StaticFiles(directory=APP_DIR / "static"), name="static")
app.include_router(menu.router)
app.include_router(evento.router)
