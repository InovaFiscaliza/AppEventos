"""Testes da pagina inicial."""

import re
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit
from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient

from src.modules.fiscais import persistencia
from src.main import app
from src.modules.eventos.acesso import AcessoEventos, EventoHandler
from src.modules.sessao import sessao_fiscal
from src.web.routers import evento


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
def client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    """Cria um cliente HTTP para os testes."""
    monkeypatch.setattr(evento, "listar_fiscais_para_evento", lambda: [])
    return TestClient(app)


def test_index_exibe_pagina_inicial(client: TestClient) -> None:
    """A pagina inicial deve renderizar o template."""
    response = client.get("/")

    assert response.status_code == 200
    assert response.template.name == "index.html"
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
        "/static/css/style.css",
    ]
    assert len(pagina.scripts) == 1

    for endereco in pagina.folhas_estilo:
        css = client.get(endereco)
        assert css.status_code == 200
        assert css.headers["content-type"].startswith("text/css")

    folha = pagina.folhas_estilo[-1]
    caminhos_fontes = re.findall(r'url\("([^"]+\.woff2)"\)', client.get(folha).text)
    assert len(caminhos_fontes) == 4
    for caminho in caminhos_fontes:
        fonte = client.get(urljoin(folha, caminho))
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


def test_index_nao_aceita_post(client: TestClient) -> None:
    """A pagina inicial aceita apenas os metodos definidos pela rota."""
    response = client.post("/")

    assert response.status_code == 405
    assert "GET" in response.headers["allow"]


@pytest.mark.parametrize("caminho", ["/usuarios", "/entrar", "/entrar/anatel", "/sair", "/api/usuarios/login-evento"])
@pytest.mark.parametrize("metodo", ["GET", "POST"])
def test_rotas_do_cadastro_manual_foram_removidas(
    client: TestClient, caminho: str, metodo: str
) -> None:
    assert client.request(metodo, caminho).status_code == 404


def test_links_de_volta_apontam_para_o_index(client: TestClient) -> None:
    novo_evento = client.get("/eventos/novo")
    assert 'href="http://testserver/">Cancelar</a>' in novo_evento.text


@pytest.mark.parametrize("papel", ["admin", "developer"])
def test_contexto_de_eventos_respeita_o_perfil(
    client: TestClient, monkeypatch: pytest.MonkeyPatch, papel: str
) -> None:
    """Verifica vínculos, troca de perfil e revogação de acesso ao evento.

    Args:
        client (TestClient): Cliente HTTP da aplicação.
        monkeypatch (pytest.MonkeyPatch): Substitui a autenticação e as leituras do banco.
        papel (str): Papel global ativo atribuído ao fiscal.

    Returns:
        None.
    """
    assert client.post("/contexto", data={"perfil": papel}).status_code == 401
    monkeypatch.setattr(persistencia, "sincronizar_fiscal", Mock(return_value=42))
    client.headers.update({"X-User-Name": "Fiscal Teste", "X-User-Email": "fiscal@example.test"})
    papeis = [{"NA_ROLE": papel}]
    vinculados = [
        {"ID_EVENTO": 1, "NO_EVENTO": "Evento da equipe", "IC_COORDENACAO": 0},
        {"ID_EVENTO": 2, "NO_EVENTO": "Evento coordenado", "IC_COORDENACAO": 1},
    ]
    externo = {"ID_EVENTO": 3, "NO_EVENTO": "Evento externo", "IC_COORDENACAO": None}

    def consultar(banco, consulta, parametros):
        assert parametros[0] == 42
        if '"TB_FISCAL_ROLE"' in consulta.as_string():
            assert '"IS_ACTIVE"' in consulta.as_string()
            return papeis
        return [*vinculados, externo] if parametros[1] else vinculados

    monkeypatch.setattr(EventoHandler, "_select_raw", consultar)

    pagina = client.get("/")
    assert "Evento da equipe" in pagina.text
    assert "Evento coordenado" in pagina.text
    assert "Evento externo" not in pagina.text
    assert client.post("/contexto", data={"id_evento": 3}).status_code == 403
    assert client.post("/contexto", data={"id_evento": 1}).status_code == 200
    assert 'value="1" selected' in client.get("/").text
    assert 'value="1" selected' not in client.post("/contexto", data={"id_evento": ""}).text
    assert 'value="1" selected' in client.post("/contexto", data={"id_evento": 1}).text

    pagina = client.post("/contexto", data={"perfil": "coordenador"})
    assert "Evento coordenado" in pagina.text
    assert "Evento da equipe" not in pagina.text
    assert 'value="1" selected' not in pagina.text
    assert client.post("/contexto", data={"id_evento": 1}).status_code == 403

    pagina = client.post("/contexto", data={"perfil": papel})
    assert "Evento externo" in pagina.text
    assert 'value="3" selected' in client.post("/contexto", data={"id_evento": 3}).text

    papeis.clear()
    pagina = client.get("/")
    assert "Evento externo" not in pagina.text
    assert f'name="perfil" value="{papel}"' not in pagina.text
    assert client.post("/contexto", data={"perfil": papel}).status_code == 403
    assert client.post("/contexto", data={"id_evento": 3}).status_code == 403


def test_index_sincroniza_identidade_dos_cabecalhos(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Verifica a normalização e a sessão criada pelos cabeçalhos do RF.Fusion.

    Args:
        client (TestClient): Cliente HTTP da aplicação.
        monkeypatch (pytest.MonkeyPatch): Substitui o cadastro e a consulta de acesso.

    Returns:
        None.
    """
    sincronizar = Mock(return_value=42)
    monkeypatch.setattr(persistencia, "sincronizar_fiscal", sincronizar)
    eventos = [{"ID_EVENTO": 1, "NO_EVENTO": "Evento autorizado"}]
    consultar = Mock(return_value=AcessoEventos({"fiscal": "Fiscal"}, "fiscal", eventos))
    monkeypatch.setattr(sessao_fiscal, "consultar_acesso_eventos", consultar)
    assert client.get("/", headers={"X-User-Name": "Fiscal"}).status_code == 200
    sincronizar.assert_not_called()

    resposta = client.get("/", headers={
        "X-User-Name": "Fiscal César".encode(),
        "X-User-Email": "  FISCAL@example.test  ",
        "X-User-Job-Title": "Servidor",
        "X-User-Department": "Fiscalizacao",
        "X-User-Location": "Brasília".encode(),
        "X-User-Avatar-Url": "https://example.test/avatar.png",
    })

    assert resposta.status_code == 200
    assert resposta.headers["cache-control"] == "no-store"
    assert "Fiscal César" in resposta.text
    assert "Evento autorizado" in resposta.text
    assert "Cabeçalhos recebidos" not in resposta.text
    sincronizar.assert_called_once_with({
        "email": "fiscal@example.test",
        "nome": "Fiscal César",
        "cargo": "Servidor",
        "departamento": "Fiscalizacao",
        "local": "Brasília",
        "avatar_url": "https://example.test/avatar.png",
    })
    consultar.assert_called_once_with(42, "fiscal")

    assert client.post("/contexto", data={"id_evento": 1}).status_code == 401


def test_troca_de_identidade_limpa_evento_ativo(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Evita reutilizar a seleção entre identidades no mesmo navegador.

    Args:
        client (TestClient): Cliente HTTP da aplicação.
        monkeypatch (pytest.MonkeyPatch): Substitui as consultas do banco.

    Returns:
        None.
    """
    monkeypatch.setattr(
        persistencia, "sincronizar_fiscal",
        lambda perfil: 42 if perfil["email"] == "primeiro@example.test" else 43,
    )
    acesso = AcessoEventos(
        {"fiscal": "Fiscal"}, "fiscal", [{"ID_EVENTO": 1, "NO_EVENTO": "Evento compartilhado"}]
    )
    monkeypatch.setattr(sessao_fiscal, "consultar_acesso_eventos", Mock(return_value=acesso))
    client.headers.update({"X-User-Name": "Primeiro", "X-User-Email": "primeiro@example.test"})
    assert 'value="1" selected' in client.post("/contexto", data={"id_evento": 1}).text
    client.headers.update({"X-User-Name": "Segundo", "X-User-Email": "segundo@example.test"})
    resposta = client.get("/")
    assert "Segundo" in resposta.text
    assert 'value="1" selected' not in resposta.text
