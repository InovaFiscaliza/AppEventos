"""Testes da pagina inicial."""

import json
from html.parser import HTMLParser
from urllib.parse import urlsplit
from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.routers import login


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
    assert '/static/img/anatel_icon.svg" alt="Anatel"' in response.text
    assert 'alt="Anatel"' in response.text
    assert 'id="evento"' in response.text

    pagina = EstruturaPagina()
    pagina.feed(response.text)
    assert pagina.idioma == "pt-BR"
    assert {"html", "head", "body"}.issubset(pagina.elementos)


def test_arquivos_estaticos_do_template_estao_disponiveis(client: TestClient) -> None:
    """Os enderecos do HTML devem servir CSS e JavaScript."""
    pagina = EstruturaPagina()
    pagina.feed(client.get("/").text)

    assert [urlsplit(url).path for url in pagina.folhas_estilo] == [
        "/static/css/AnatelReactiveTheme.AnatelReactiveTheme.css",
        "/static/css/Desempenho_CW.Desempenho.css",
        "/static/css/appeventos_base.css",
        "/static/style.css",
    ]
    assert len(pagina.scripts) == 1

    for endereco in pagina.folhas_estilo:
        css = client.get(endereco)
        assert css.status_code == 200
        assert css.headers["content-type"].startswith("text/css")

    for peso in (400, 600, 700):
        fonte = client.get(f"/static/fonts/rawline/rawline-{peso}.woff2")
        assert fonte.status_code == 200
        assert fonte.content.startswith(b"wOF2")

    script = client.get(pagina.scripts[0])
    assert script.status_code == 200
    assert "javascript" in script.headers["content-type"]
    for nome in ("anatel_icon.svg", "profile_out.svg"):
        imagem = client.get(f"/static/img/{nome}")
        assert imagem.status_code == 200
        assert imagem.headers["content-type"] == "image/svg+xml"


@pytest.mark.parametrize("caminho", ["/pagina-inexistente", "/static/inexistente.css"])
def test_caminhos_inexistentes_retornam_404(client: TestClient, caminho: str) -> None:
    """Rotas e arquivos desconhecidos nao devem retornar a pagina inicial."""
    assert client.get(caminho).status_code == 404


def test_login_oferece_acesso_anatel(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A tela de login oferece acesso ao fluxo corporativo."""
    url = "https://fiscalizacao.anatel.gov.br/rffusion/api/users/login_eventos"
    monkeypatch.setitem(login.templates.env.globals, "url_acesso_anatel", url)

    response = client.get("/", follow_redirects=False)

    assert response.status_code == 200
    assert response.template.name == "login.html"
    assert 'href="http://testserver/entrar/anatel"' in response.text


def test_login_do_rf_fusion_inicia_so_ao_clicar_no_botao(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    url = "https://fiscalizacao.anatel.gov.br/rffusion/api/users/login_eventos"
    monkeypatch.setattr(login, "URL_ACESSO_ANATEL", url)

    pagina = client.get("/", follow_redirects=False)
    assert pagina.status_code == 200
    assert "Anônimo" in pagina.text
    assert '>Login</a>' in pagina.text

    inicial = client.get("/entrar/anatel", follow_redirects=False)
    assert inicial.status_code == 303
    assert inicial.headers["location"] == url
    assert inicial.headers["cache-control"] == "no-store"

    retorno = client.get("/", follow_redirects=False)
    assert retorno.status_code == 200
    assert ">Login</a>" in retorno.text


def test_login_nao_aceita_post(client: TestClient) -> None:
    """A pagina inicial aceita apenas os metodos definidos pela rota."""
    response = client.post("/")

    assert response.status_code == 405
    assert "GET" in response.headers["allow"]


@pytest.mark.parametrize("caminho", ["/usuarios", "/entrar"])
@pytest.mark.parametrize("metodo", ["GET", "POST"])
def test_rotas_do_cadastro_manual_foram_removidas(
    client: TestClient, caminho: str, metodo: str
) -> None:
    assert client.request(metodo, caminho).status_code == 404


def test_links_de_volta_apontam_para_login(client: TestClient) -> None:
    saida = client.get("/sair", follow_redirects=False)
    assert saida.status_code == 303
    assert saida.headers["location"].endswith("/")
    assert client.get(saida.headers["location"]).template.name == "login.html"

    novo_evento = client.get("/eventos/novo")
    assert 'href="http://testserver/">Cancelar</a>' in novo_evento.text


@pytest.mark.parametrize("caminho", ["/", "/entrar/anatel"])
@pytest.mark.parametrize("token", ["token-teste", "incorreto", ""])
def test_login_sincroniza_apenas_perfil_do_proxy(
    client: TestClient, monkeypatch: pytest.MonkeyPatch, caminho: str, token: str
) -> None:
    monkeypatch.setattr(login, "ANATEL_PROXY_TOKEN", "token-teste")
    sincronizar = Mock(return_value=42)
    monkeypatch.setattr(login.servico_usuarios, "sincronizar_fiscal", sincronizar)
    resposta = client.get(caminho, follow_redirects=False, headers={
        "x-appeventos-proxy-token": token,
        "x-user-profile": json.dumps({
            "NA_USER_EMAIL": "fiscal@example.test",
            "NA_USER_NAME": "Fiscal Teste",
            "NA_DEPARTMENT": "Departamento",
            "NA_JOB_TITLE": "Cargo",
            "NA_LOCATION": "Local",
        }),
    })

    assert resposta.status_code == (200 if caminho == "/" else 303)
    if token == "token-teste":
        sincronizar.assert_called_once_with({
            "email": "fiscal@example.test",
            "nome": "Fiscal Teste",
            "departamento": "Departamento",
            "cargo": "Cargo",
            "local": "Local",
        })
        assert 'title="Fiscal Teste">Fiscal Teste</span>' in client.get("/").text
    else:
        sincronizar.assert_not_called()


def test_login_rejeita_perfil_invalido_do_proxy(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(login, "ANATEL_PROXY_TOKEN", "token-teste")
    resposta = client.get("/", headers={
        "x-appeventos-proxy-token": "token-teste",
        "x-user-profile": "invalido",
    })
    assert resposta.status_code == 502
    assert "Perfil Anatel inválido." in resposta.text


def test_formulario_cadastra_fiscal_e_mostra_perfil_na_pagina_inicial(
    client: TestClient, monkeypatch: pytest.MonkeyPatch,
) -> None:
    cadastrar = Mock()
    monkeypatch.setattr(login.servico_usuarios, "cadastrar_fiscal", cadastrar)

    resposta = client.post("/api/usuarios/login-evento", data={
        "NA_USER_EMAIL": "fiscal@example.test",
        "NA_USER_NAME": "Fiscal de São Paulo",
        "NA_DEPARTMENT": "Unidade de teste",
        "NA_JOB_TITLE": "Cargo de teste",
        "NA_LOCATION": "São Paulo, SP",
        "state": "ignorado",
        "signature": "ignorada",
    }, follow_redirects=False)

    assert resposta.status_code == 303
    assert resposta.headers["location"] == "/"
    assert "session" not in resposta.cookies
    pagina = client.get("/")
    assert pagina.status_code == 200
    assert 'title="Fiscal de São Paulo">Fiscal de São Paulo</span>' in pagina.text
    assert "FP" in pagina.text
    assert "fiscal@example.test" not in pagina.text
    assert "Fiscal de São Paulo" in client.get("/").text
    assert "Fiscal de São Paulo" in client.get("/eventos/novo").text
    assert "Anônimo" in client.get("/sair").text
    assert "Fiscal de São Paulo" not in client.get("/").text
    cadastrar.assert_called_once_with({
        "email": "fiscal@example.test",
        "nome": "Fiscal de São Paulo",
        "departamento": "Unidade de teste",
        "cargo": "Cargo de teste",
        "local": "São Paulo, SP",
    })


def test_formulario_incompleto_nao_cadastra(
    client: TestClient, monkeypatch: pytest.MonkeyPatch,
) -> None:
    cadastrar = Mock()
    monkeypatch.setattr(login.servico_usuarios, "cadastrar_fiscal", cadastrar)

    resposta = client.post(
        "/api/usuarios/login-evento", data={"NA_USER_EMAIL": "fiscal@example.test"}
    )

    assert resposta.status_code == 422
    assert not resposta.cookies
    assert "O RF.Fusion enviou um formulário de login incompleto ou inválido." in resposta.text
    assert ">Login</a>" in resposta.text
    assert "fiscal@example.test" not in resposta.text
    assert resposta.headers["cache-control"] == "no-store"
    cadastrar.assert_not_called()
