"""Testes da pagina inicial."""

from html.parser import HTMLParser

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.routers import login


class EstruturaPagina(HTMLParser):
    """Reune os elementos importantes do HTML renderizado."""

    def __init__(self) -> None:
        super().__init__()
        self.idioma: str | None = None
        self.elementos: list[str] = []
        self.folhas_estilo: list[str] = []
        self.scripts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        atributos = dict(attrs)
        self.elementos.append(tag)
        if tag == "html":
            self.idioma = atributos.get("lang")
        elif tag == "link" and atributos.get("rel") == "stylesheet":
            endereco = atributos.get("href")
            if endereco:
                self.folhas_estilo.append(endereco)
        elif tag == "script":
            endereco = atributos.get("src")
            if endereco:
                self.scripts.append(endereco)


@pytest.fixture
def client() -> TestClient:
    """Cria um cliente HTTP para os testes."""
    return TestClient(app)


def test_login_exibe_pagina_inicial(client: TestClient) -> None:
    """A pagina inicial deve renderizar o template."""
    response = client.get("/")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    assert "AppEventos" in response.text
    assert "/static/Anatel.png" in response.text
    assert 'alt="Anatel"' in response.text
    assert "Faça login para iniciar o trabalho no evento." in response.text
    assert 'id="evento"' in response.text
    assert 'id="usuario"' in response.text
    assert 'id="senha"' in response.text
    assert 'id="perfil"' in response.text
    assert "Login ainda não configurado." in response.text

    pagina = EstruturaPagina()
    pagina.feed(response.text)
    assert pagina.idioma == "pt-BR"
    assert {"html", "head", "body"}.issubset(pagina.elementos)


def test_arquivos_estaticos_do_template_estao_disponiveis(client: TestClient) -> None:
    """Os enderecos do HTML devem servir CSS e JavaScript."""
    pagina = EstruturaPagina()
    pagina.feed(client.get("/").text)

    assert len(pagina.folhas_estilo) == 1
    assert len(pagina.scripts) == 1

    css = client.get(pagina.folhas_estilo[0])
    script = client.get(pagina.scripts[0])
    assert css.status_code == 200
    assert css.headers["content-type"].startswith("text/css")
    assert script.status_code == 200
    assert "javascript" in script.headers["content-type"]
    logo = client.get("/static/Anatel.png")
    assert logo.status_code == 200
    assert logo.headers["content-type"] == "image/png"


@pytest.mark.parametrize("caminho", ["/pagina-inexistente", "/static/inexistente.css"])
def test_caminhos_inexistentes_retornam_404(client: TestClient, caminho: str) -> None:
    """Rotas e arquivos desconhecidos nao devem retornar a pagina inicial."""
    assert client.get(caminho).status_code == 404


def test_login_consulta_usuario_anatel_sem_desviar(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    """O / mostra o login direto e entrega ao navegador o endereço do RF Fusion."""
    url = "https://fiscalizacao.anatel.gov.br/rffusion/api/users/me"
    monkeypatch.setitem(login.templates.env.globals, "url_acesso_anatel", url)

    response = client.get("/", follow_redirects=False)

    assert response.status_code == 200
    assert response.template.name == "login.html"
    assert f'data-url-usuario-anatel="{url}"' in response.text
    assert 'id="usuario-anatel-ausente"' in response.text


def test_login_nao_aceita_post(client: TestClient) -> None:
    """A pagina inicial aceita apenas os metodos definidos pela rota."""
    response = client.post("/")

    assert response.status_code == 405
    assert "GET" in response.headers["allow"]


def test_pagina_inicial_usa_template_login(client: TestClient) -> None:
    """A rota / deve renderizar login.html com o formulário apontando para /entrar."""
    response = client.get("/")

    assert response.template.name == "login.html"
    assert "<title>Login - AppEventos</title>" in response.text
    assert 'action="http://testserver/entrar"' in response.text


@pytest.mark.parametrize(
    ("dados", "status"),
    [
        ({"usuario": "Cadastrar Usuário", "senha": "1234"}, 401),
        ({"usuario": "Outro", "senha": "5000"}, 400),
    ],
)
def test_erro_de_login_renderiza_template_login(
    client: TestClient, dados: dict[str, str], status: int
) -> None:
    """Falhas em /entrar devem reapresentar login.html com o alerta."""
    response = client.post("/entrar", data=dados)

    assert response.status_code == status
    assert response.template.name == "login.html"
    assert 'role="alert"' in response.text


def test_entrar_nao_aceita_get(client: TestClient) -> None:
    """/entrar só recebe o envio do formulário."""
    assert client.get("/entrar").status_code == 405


@pytest.mark.parametrize(
    ("metodo", "caminho"),
    [("get", "/sair"), ("get", "/usuarios"), ("post", "/usuarios")],
)
def test_rotas_que_voltam_ao_login(
    client: TestClient, metodo: str, caminho: str
) -> None:
    """Saída e acesso sem sessão devem redirecionar para a tela de login."""
    response = client.request(metodo.upper(), caminho, follow_redirects=False)

    assert response.status_code == 303
    assert response.headers["location"].endswith("/")
    assert client.get(response.headers["location"]).template.name == "login.html"


def test_links_de_volta_apontam_para_login(client: TestClient) -> None:
    """Os links "Cancelar" e "Início" devem levar à tela de login."""
    novo_evento = client.get("/eventos/novo")
    client.post("/entrar", data={"usuario": "Cadastrar Usuário", "senha": "5000"})
    usuarios = client.get("/usuarios")

    assert 'href="http://testserver/">Cancelar</a>' in novo_evento.text
    assert 'href="http://testserver/">Início</a>' in usuarios.text
