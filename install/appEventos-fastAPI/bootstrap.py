"""Aplicação inicial para verificar o runtime antes de montar a API do appEventos."""

from fastapi import FastAPI

app = FastAPI(title="appEventos", version="0.1.0")


@app.get("/")
def index() -> dict[str, str]:
    """Retorna a identificação inicial da API.

    Returns:
        dict[str, str]: Chaves obrigatórias `application` (nome da aplicação)
            e `docs` (caminho da documentação interativa), ambas strings.
    """
    return {"application": "appEventos", "docs": "/docs"}


@app.get("/health")
def health() -> dict[str, str]:
    """Indica que o processo HTTP está respondendo.

    Returns:
        dict[str, str]: Chave obrigatória `status`, string com valor `ok`.
    """
    return {"status": "ok"}
