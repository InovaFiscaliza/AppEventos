"""Configuracao principal da aplicacao web."""

import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

# A execução por arquivo adiciona src/, em vez da raiz do projeto, ao sys.path.
if __name__ == "__main__" and not __package__:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.config import SESSION_SECRET
from src.web.routers import cadastro, evento, index

APP_DIR = Path(__file__).resolve().parent

app = FastAPI(title="AppGrandesEventos")
# Cookie assinado guarda quem fez login; same_site="lax" barra POST vindo de outros sites.
app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET, same_site="lax")
app.mount("/static", StaticFiles(directory=APP_DIR / "web" / "static"), name="static")
app.include_router(index.router)
app.include_router(cadastro.router)
app.include_router(evento.router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8080)
