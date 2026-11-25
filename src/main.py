"""Configuracao principal da aplicacao web."""

import sys
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

# A execução por arquivo adiciona src/, em vez da raiz do projeto, ao sys.path.
if __name__ == "__main__" and not __package__:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.config import SESSION_SECRET
from src.routers import evento, login

APP_DIR = Path(__file__).resolve().parent

app = FastAPI(title="AppGrandesEventos")
# Cookie assinado guarda quem fez login; same_site="lax" barra POST vindo de outros sites.
app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET, same_site="lax")
app.mount("/static", StaticFiles(directory=APP_DIR / "static"), name="static")
# Sem prefix: a rota "/" de app/routers/login.py (linha 38) vira a pagina inicial.
app.include_router(login.router)
app.include_router(evento.router)


@app.exception_handler(RequestValidationError)
async def erro_de_validacao(request: Request, erro: RequestValidationError):
    if request.scope.get("endpoint") is login.receber_perfil_rf_fusion:
        resposta = login.renderizar_login(
            request, "O RF.Fusion enviou um formulário de login incompleto ou inválido.", 422
        )
        resposta.headers["Cache-Control"] = "no-store"
        return resposta
    return await request_validation_exception_handler(request, erro)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8080)

# login anatel
# https://fiscalizacao.anatel.gov.br/rffusion/api/users/login_eventos
# https://appsnet/acesso/
