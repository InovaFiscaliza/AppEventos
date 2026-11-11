"""Testes do cadastro de usuários; o banco é simulado em conftest.py."""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client() -> TestClient:
    """Cria um cliente HTTP já autenticado como "Cadastrar Usuário"."""
    # lista_isolada (autouse) roda antes, então o login ocorre com a lista vazia.
    cliente = TestClient(app)
    cliente.post(
        "/entrar",
        data={"usuario": "Cadastrar Usuário", "senha": "5000"},
        follow_redirects=False,
    )
    return cliente


def test_menu_sem_usuarios_oferece_cadastrar_usuario() -> None:
    """Sem nenhum usuário, o login deve oferecer "Cadastrar Usuário"."""
    response = TestClient(app).get("/")

    assert ">Cadastrar Usuário</option>" in response.text


def test_menu_com_usuarios_oculta_cadastrar_usuario(
    lista_isolada: list[dict[str, str]],
) -> None:
    """Com usuário cadastrado, a opção some e o login dela é recusado."""
    lista_isolada.append({"nome": "Fiscal Teste 1", "unidade": "GR01"})
    cliente = TestClient(app)

    menu = cliente.get("/")
    login = cliente.post(
        "/entrar", data={"usuario": "Cadastrar Usuário", "senha": "5000"}
    )

    assert "Fiscal Teste 1 (GR01)" in menu.text
    assert "Cadastrar Usuário" not in menu.text
    assert login.status_code == 400
    assert cliente.get("/usuarios", follow_redirects=False).status_code == 303


def test_login_com_senha_correta_abre_cadastro() -> None:
    """A senha 5000 deve liberar a tela de cadastro."""
    cliente = TestClient(app)
    response = cliente.post(
        "/entrar",
        data={"usuario": "Cadastrar Usuário", "senha": "5000"},
        follow_redirects=False,
    )

    assert response.status_code == 303
    assert response.headers["location"].endswith("/usuarios")
    assert cliente.get("/usuarios").status_code == 200


@pytest.mark.parametrize(
    ("dados", "status", "mensagem"),
    [
        ({"usuario": "Cadastrar Usuário", "senha": "1234"}, 401, "Senha inválida."),
        (
            {"usuario": "Fiscal Teste 1", "senha": "5000"},
            400,
            "Login ainda não configurado.",
        ),
    ],
)
def test_login_invalido(dados: dict[str, str], status: int, mensagem: str) -> None:
    """Senha errada ou outro usuário não liberam o cadastro."""
    cliente = TestClient(app)
    response = cliente.post("/entrar", data=dados)

    assert response.status_code == status
    assert mensagem in response.text
    assert cliente.get("/usuarios", follow_redirects=False).status_code == 303


def test_cadastro_exige_login(lista_isolada: list[dict[str, str]]) -> None:
    """Sem sessão, a tela e a inclusão voltam ao login."""
    cliente = TestClient(app)

    tela = cliente.get("/usuarios", follow_redirects=False)
    inclusao = cliente.post(
        "/usuarios", data={"nome": "Intruso", "unidade": "GR09"}, follow_redirects=False
    )

    assert tela.status_code == 303
    assert inclusao.status_code == 303
    assert lista_isolada == []


def test_sair_encerra_sessao(client: TestClient) -> None:
    """Depois de sair, o cadastro volta a exigir login."""
    client.get("/sair", follow_redirects=False)

    assert client.get("/usuarios", follow_redirects=False).status_code == 303


def test_pagina_lista_usuarios(client: TestClient, lista_isolada: list[dict]) -> None:
    """A tela deve exibir a tabela com papéis e o formulário de inclusão."""
    lista_isolada.append(
        {
            "nome": "Fiscal Teste 1",
            "unidade": "GR01",
            "coordenacao": 1,
            "abordagem": 0,
            "monitoracao": 1,
        }
    )
    response = client.get("/usuarios")

    assert response.status_code == 200
    assert "Novo Usuário" in response.text
    assert "<td>Fiscal Teste 1</td>" in response.text
    assert "<td>Coordenação, Monitoração</td>" in response.text
    assert 'id="nome"' in response.text
    assert '<option value="GR01"' in response.text
    assert "Papéis permitidos" in response.text
    assert 'value="abordagem"' in response.text


def test_incluir_usuario(client: TestClient, lista_isolada: list[dict]) -> None:
    """Um usuário válido deve ser gravado com os papéis marcados."""
    response = client.post(
        "/usuarios",
        data={
            "nome": "  Maria Silva ",
            "unidade": "GR02",
            "papeis": ["coordenacao", "abordagem", "invalido"],
        },
        follow_redirects=False,
    )

    assert response.status_code == 303
    assert response.headers["location"].endswith("/usuarios")
    assert lista_isolada == [
        {
            "nome": "Maria Silva",
            "unidade": "GR02",
            "coordenacao": 1,
            "abordagem": 1,
            "monitoracao": 0,
        }
    ]


@pytest.mark.parametrize(
    ("dados", "mensagem"),
    [
        ({"nome": " ", "unidade": "GR01"}, "Informe o nome do usuário."),
        ({"nome": "Maria", "unidade": ""}, "Selecione a unidade executante."),
        ({"nome": "Maria", "unidade": "GR99"}, "Selecione a unidade executante."),
    ],
)
def test_incluir_usuario_invalido(
    client: TestClient,
    lista_isolada: list[dict],
    dados: dict[str, str],
    mensagem: str,
) -> None:
    """Dados inválidos devem voltar ao formulário sem incluir."""
    response = client.post("/usuarios", data=dados)

    assert response.status_code == 400
    assert mensagem in response.text
    assert lista_isolada == []
