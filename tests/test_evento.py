"""Testes do cadastro de eventos."""

import re
from decimal import Decimal
from unittest.mock import MagicMock, Mock, call
from urllib.parse import urljoin

import pytest
from fastapi.testclient import TestClient
from psycopg import Connection
from psycopg.errors import ForeignKeyViolation
from psycopg.pq import DiagnosticField, TransactionStatus

from src.modules.eventos import cadastro
from src.main import app
from src.web.routers import evento


@pytest.fixture
def client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    """Cria um cliente HTTP para os testes."""
    monkeypatch.setattr(
        evento, "listar_fiscais_para_evento",
        lambda: [
            {"ID_FISCAL": 7, "NO_FISCAL": "Fiscal de teste"},
            {"ID_FISCAL": 8, "NO_FISCAL": "Fiscal da equipe"},
        ],
    )
    return TestClient(app)


@pytest.fixture
def conexao(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    """Simula a sessão PostgreSQL usada pelo DbHandler.

    Args:
        monkeypatch (pytest.MonkeyPatch): Substitui a abertura da sessão real.

    Returns:
        MagicMock: Sessão simulada com cursor que devolve o ID do evento.
    """
    sessao = MagicMock(spec=Connection)
    sessao.closed = sessao.broken = False
    sessao.info.transaction_status = TransactionStatus.IDLE
    cursor = sessao.cursor.return_value.__enter__.return_value
    cursor.fetchone.return_value = {"ID_EVENTO": 42}
    cursor.rowcount = 2
    monkeypatch.setattr(Connection, "connect", Mock(return_value=sessao))
    return sessao


def test_index_oferece_criar_evento(client: TestClient) -> None:
    """O seletor de evento deve levar ao formulário de criação."""
    response = client.get("/")

    assert "+ Criar Evento" in response.text
    assert 'data-url="http://testserver/cadastro/evento"' in response.text


def test_formulario_de_novo_evento(client: TestClient) -> None:
    """O formulário deve exibir os campos do evento."""
    response = client.get("/cadastro/evento")

    assert response.status_code == 200
    assert 'id="nome"' in response.text
    assert 'id="data_inicio"' in response.text
    assert 'id="data_fim"' in response.text
    assert '<option value="7">' in response.text
    assert "Fiscal de teste" in response.text
    assert 'action="http://testserver/cadastro/evento"' in response.text
    assert 'id="buscar-fiscal-evento"' in response.text
    assert 'id="confirmacao-evento"' in response.text


def test_modulo_cadastro_navega_entre_opcoes(client: TestClient) -> None:
    """Verifica as opções, a ordem e o estado ativo da navegação de cadastro.

    Args:
        client (TestClient): Cliente HTTP da aplicação.

    Returns:
        None.
    """
    opcoes = ("evento", "teste-e-etiquetagem", "incidente", "emissao-suspeita")
    inicio = client.get("/cadastro")
    assert inicio.status_code == 200
    assert 'aria-label="Início"' in inicio.text
    assert 'id="formulario-evento"' not in inicio.text
    links = [f'href="http://testserver/cadastro/{opcao}"' for opcao in opcoes]
    posicoes = [inicio.text.index(link) for link in links]
    assert posicoes == sorted(posicoes)

    for opcao, link in zip(opcoes, links):
        pagina = client.get(f"/cadastro/{opcao}")
        assert pagina.status_code == 200
        assert f'{link} aria-current="page"' in " ".join(pagina.text.split())
        assert ('id="nome"' in pagina.text) == (opcao == "evento")

    assert client.get("/cadastro/desconhecido").status_code == 404


@pytest.mark.parametrize("caminho", ["/cadastro/evento", "/eventos/novo"])
def test_salvar_evento_grava_e_redireciona(
    client: TestClient, conexao: MagicMock, caminho: str
) -> None:
    """Um evento válido deve ser gravado e voltar à página inicial."""
    response = client.post(
        caminho,
        data={"nome": "  Carnaval 2027 ", "data_inicio": "2027-02-06", "data_fim": ""},
        follow_redirects=False,
    )

    assert response.status_code == 303
    destino = response.headers["location"]
    assert urljoin("https://example.test" + caminho, destino) == "https://example.test/"
    base_publica = "https://example.test/rffusion/eventos"
    assert urljoin(base_publica + caminho, destino) == base_publica + "/"
    cursor = conexao.cursor.return_value.__enter__.return_value
    consulta, parametros = cursor.execute.call_args.args
    assert consulta.as_string().endswith('RETURNING "ID_EVENTO"')
    assert parametros[0] == "Carnaval 2027"
    assert str(parametros[1]) == "2027-02-06"
    assert parametros[2] is None
    conexao.commit.assert_called_once_with()


def test_salvar_evento_associa_municipio_e_fiscal(
    client: TestClient, conexao: MagicMock, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Verifica a gravação do município calculado e do vínculo de coordenação.

    Args:
        client (TestClient): Cliente HTTP da aplicação.
        conexao (MagicMock): Sessão simulada que registra as inserções.
        monkeypatch (pytest.MonkeyPatch): Substitui a consulta geográfica.

    Returns:
        None.
    """
    identificar = Mock(return_value={"codigo": 5300108, "nome": "Brasília", "uf": "DF"})
    monkeypatch.setattr(cadastro, "identificar_municipio", identificar)

    response = client.post(
        "/eventos/novo",
        data={
            "nome": "Evento de teste",
            "latitude": "-15.7939",
            "longitude": "-47.8828",
            "municipio": "3550308",
            "id_fiscal_responsavel": "7",
            "ids_fiscais": ["8", "7", "8"],
            "teste_etiquetagem": "1",
            "observacao": "Observação do evento.",
        },
        follow_redirects=False,
    )

    assert response.status_code == 303
    identificar.assert_called_once_with(-15.7939, -47.8828)
    cursor = conexao.cursor.return_value.__enter__.return_value
    assert cursor.execute.call_args.args[1][3:9] == (
        Decimal("-15.793900"), Decimal("-47.882800"), 5300108, 7, 1, "Observação do evento."
    )
    consulta, vinculos = cursor.executemany.call_args.args
    assert vinculos == [(42, 7, 1), (42, 8, 0)]
    assert conexao.mock_calls.index(call.cursor().__enter__().executemany(consulta, vinculos)) < (
        conexao.mock_calls.index(call.commit())
    )
    conexao.commit.assert_called_once_with()


def test_salvar_evento_com_equipe_e_sem_responsavel(
    client: TestClient, conexao: MagicMock
) -> None:
    """Verifica que fiscais podem integrar a equipe sem assumir coordenação.

    Args:
        client (TestClient): Cliente HTTP da aplicação.
        conexao (MagicMock): Sessão simulada que registra as inserções.

    Returns:
        None.
    """
    response = client.post(
        "/cadastro/evento",
        data={"nome": "Evento de teste", "ids_fiscais": ["7", "8"]},
        follow_redirects=False,
    )

    assert response.status_code == 303
    cursor = conexao.cursor.return_value.__enter__.return_value
    assert cursor.executemany.call_args.args[1] == [(42, 7, 0), (42, 8, 0)]


def test_evento_com_coordenadas_sem_municipio_nao_grava(
    client: TestClient, conexao: MagicMock, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Verifica que um ponto sem município volta ao formulário para correção.

    Args:
        client (TestClient): Cliente HTTP da aplicação.
        conexao (MagicMock): Sessão simulada que registra as inserções.
        monkeypatch (pytest.MonkeyPatch): Faz a consulta geográfica retornar None.

    Returns:
        None.
    """
    monkeypatch.setattr(cadastro, "identificar_municipio", Mock(return_value=None))

    response = client.post(
        "/eventos/novo",
        data={"nome": "Evento de teste", "latitude": "0", "longitude": "0", "ids_fiscais": "8"},
    )

    assert response.status_code == 400
    assert "Não foi possível identificar um município único" in response.text
    assert 'id="evento-form-erro"' in response.text
    assert 'name="ids_fiscais" value="8"' in response.text
    conexao.cursor.assert_not_called()


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
    client: TestClient, conexao: MagicMock, dados: dict, mensagem: str
) -> None:
    """Dados inválidos devem voltar ao formulário sem gravar."""
    response = client.post("/eventos/novo", data=dados)

    assert response.status_code == 400
    assert mensagem in response.text
    conexao.cursor.assert_not_called()



def test_falha_no_vinculo_reverte_evento(client: TestClient, conexao: MagicMock) -> None:
    """Verifica o rollback quando um fiscal da equipe não existe.

    Args:
        client (TestClient): Cliente HTTP da aplicação.
        conexao (MagicMock): Sessão simulada que registra a transação.

    Returns:
        None.
    """
    cursor = conexao.cursor.return_value.__enter__.return_value
    erro = ForeignKeyViolation(
        info={DiagnosticField.CONSTRAINT_NAME: b"FK_TB_EVENTO_FISCAL_TB_FISCAL"}
    )
    cursor.executemany.side_effect = erro

    resposta = client.post("/cadastro/evento", data={"nome": "Evento", "ids_fiscais": "7"})

    assert resposta.status_code == 400
    assert "Um dos fiscais da equipe não está mais disponível." in resposta.text
    cursor.execute.assert_called_once()
    conexao.rollback.assert_called_once_with()
    conexao.commit.assert_not_called()
    conexao.close.assert_called_once_with()



@pytest.mark.parametrize("caminho", ["/cadastro/evento", "/eventos/novo"])
def test_consulta_municipio_preserva_prefixo_publico(
    client: TestClient, monkeypatch: pytest.MonkeyPatch, caminho: str
) -> None:
    """Verifica o endereço da consulta quando o proxy retira o prefixo público.

    Args:
        client (TestClient): Cliente que recebe o formulário do FastAPI.
        monkeypatch (pytest.MonkeyPatch): Substitui a consulta geográfica.
        caminho (str): Rota interna que renderiza o formulário.

    Returns:
        None.
    """
    municipio = {"codigo": 5300108, "nome": "Brasília", "uf": "DF"}
    identificar = Mock(return_value=municipio)
    monkeypatch.setattr(evento, "identificar_municipio", identificar)
    formulario = client.get(caminho)
    assert formulario.status_code == 200
    consulta = re.search(r'data-consulta-url="([^"]+)"', formulario.text)
    assert consulta is not None
    prefixo = "https://example.test/rffusion/eventos"
    url_publica = urljoin(prefixo + caminho, consulta[1])
    assert url_publica == prefixo + "/eventos/municipio"

    resposta = client.get(
        url_publica.removeprefix(prefixo), params={"latitude": -15.7939, "longitude": -47.8828}
    )
    assert resposta.status_code == 200
    assert resposta.json() == municipio
    identificar.assert_called_once_with(-15.7939, -47.8828)


def test_consulta_e_salva_acao_validada(
    client: TestClient, conexao: MagicMock, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Valida a ação, sugere a equipe e persiste os códigos confirmados.

    Args:
        client (TestClient): Cliente HTTP da aplicação.
        conexao (MagicMock): Sessão simulada que captura a gravação.
        monkeypatch (pytest.MonkeyPatch): Substitui a integração externa.

    Returns:
        None.
    """
    consulta = Mock(return_value=evento.api_efiscaliza.AcaoFiscalizacao(
        "ACAO_2026_00162", ("FISCAL DE TESTE",), ("Fiscal da equipe",),
    ))
    monkeypatch.setattr(evento.api_efiscaliza, "consultar_acao", consulta)

    formulario = client.get("/cadastro/evento")
    assert 'data-acao-url="../eventos/acao-fiscalizacao"' in formulario.text
    resposta = client.get("/eventos/acao-fiscalizacao", params={"codigo": 248368})
    assert resposta.json() == {
        "identificador": "ACAO_2026_00162",
        "responsavel": 7,
        "participantes": [8],
        "equipe_incompleta": False,
    }

    resposta = client.post(
        "/cadastro/evento",
        data={
            "nome": "Evento com ação", "codigo_acao": "248368",
            "id_fiscal_responsavel": "7", "ids_fiscais": ["8"],
            "TX_ACAO_FISCALIZACAO": "valor enviado pelo navegador",
        },
        follow_redirects=False,
    )

    assert resposta.status_code == 303
    assert consulta.call_args_list == [call(248368), call(248368)]
    cursor = conexao.cursor.return_value.__enter__.return_value
    assert cursor.execute.call_args.args[1][-2:] == (248368, "ACAO_2026_00162")
    assert cursor.executemany.call_args.args[1] == [(42, 7, 1), (42, 8, 0)]


def test_acao_inexistente_impede_gravacao(
    client: TestClient, conexao: MagicMock, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Mantém o formulário preenchido quando a ação informada não existe.

    Args:
        client (TestClient): Cliente HTTP da aplicação.
        conexao (MagicMock): Sessão simulada que registra tentativas de gravação.
        monkeypatch (pytest.MonkeyPatch): Simula ação inexistente no eFiscaliza.

    Returns:
        None.
    """
    monkeypatch.setattr(evento.api_efiscaliza, "consultar_acao", Mock(return_value=None))

    assert client.get("/eventos/acao-fiscalizacao", params={"codigo": 999}).status_code == 404
    resposta = client.post("/cadastro/evento", data={"nome": "Evento de teste", "codigo_acao": "999"})

    assert resposta.status_code == 400
    assert 'value="999"' in resposta.text
    assert "Nenhuma ação de inspeção encontrada para esse código." in resposta.text
    conexao.cursor.assert_not_called()
