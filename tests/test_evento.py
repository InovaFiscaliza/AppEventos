"""Testes do cadastro de eventos."""

from contextlib import contextmanager

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.routers import evento


class ConexaoFalsa:
    """Guarda os comandos enviados ao banco."""

    def __init__(self) -> None:
        self.parametros: list[dict] = []

    def execute(self, _comando, parametros: dict) -> None:
        self.parametros.append(parametros)


class EngineFalsa:
    """Substitui o banco real durante os testes."""

    def __init__(self) -> None:
        self.conexao = ConexaoFalsa()

    @contextmanager
    def begin(self):
        yield self.conexao


@pytest.fixture
def client() -> TestClient:
    """Cria um cliente HTTP para os testes."""
    return TestClient(app)


@pytest.fixture
def engine_falsa(monkeypatch: pytest.MonkeyPatch) -> EngineFalsa:
    """Evita acesso ao PostgreSQL nos testes."""
    engine = EngineFalsa()
    monkeypatch.setattr(evento, "engine", engine)
    return engine


def test_menu_oferece_criar_evento(client: TestClient) -> None:
    """O seletor de evento deve levar ao formulário de criação."""
    response = client.get("/")

    assert "+ Criar Evento" in response.text
    assert '/eventos/novo"' in response.text


def test_formulario_de_novo_evento(client: TestClient) -> None:
    """O formulário deve exibir os campos do evento."""
    response = client.get("/eventos/novo")

    assert response.status_code == 200
    assert 'id="nome"' in response.text
    assert 'id="data_inicio"' in response.text
    assert 'id="data_fim"' in response.text


def test_salvar_evento_grava_e_redireciona(
    client: TestClient, engine_falsa: EngineFalsa
) -> None:
    """Um evento válido deve ser gravado e voltar ao login."""
    response = client.post(
        "/eventos/novo",
        data={"nome": "  Carnaval 2027 ", "data_inicio": "2027-02-06", "data_fim": ""},
        follow_redirects=False,
    )

    assert response.status_code == 303
    assert response.headers["location"] == "/"
    parametros = engine_falsa.conexao.parametros[0]
    assert parametros["nome"] == "Carnaval 2027"
    assert str(parametros["inicio"]) == "2027-02-06"
    assert parametros["fim"] is None


@pytest.mark.parametrize(
    ("dados", "mensagem"),
    [
        ({"nome": "   "}, "Informe o nome do evento."),
        (
            {"nome": "Moto GP", "data_inicio": "2027-03-10", "data_fim": "2027-03-01"},
            "A data de fim não pode ser anterior à data de início.",
        ),
    ],
)
def test_salvar_evento_invalido_nao_grava(
    client: TestClient, engine_falsa: EngineFalsa, dados: dict, mensagem: str
) -> None:
    """Dados inválidos devem voltar ao formulário sem gravar."""
    response = client.post("/eventos/novo", data=dados)

    assert response.status_code == 400
    assert mensagem in response.text
    assert engine_falsa.conexao.parametros == []
