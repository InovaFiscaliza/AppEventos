"""Verifica a consulta e a interpretação do retorno do eFiscaliza."""

import base64
import io
import json
from pathlib import Path
from unittest.mock import Mock

import pytest

from src.utils import api_efiscaliza


@pytest.mark.parametrize("entrada", ["fiscal-teste", " user = fiscal-teste ", '"user": "fiscal-teste"'])
def test_consultar_acao_usa_basic_e_le_responsavel_e_participantes(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, entrada: str
) -> None:
    """Consulta por GET e distingue o responsável dos demais fiscais da equipe.

    Args:
        monkeypatch (pytest.MonkeyPatch): Substitui o cliente HTTP e a credencial.
        tmp_path (Path): Pasta para armazenar o usuário fictício.
        entrada (str): Conteúdo do arquivo de credencial em um formato aceito.

    Returns:
        None.
    """
    credencial = tmp_path / "credencial"
    credencial.write_text(entrada + "\n", encoding="utf-8-sig")
    monkeypatch.setattr(api_efiscaliza, "_ARQUIVO_CREDENCIAL", credencial)
    monkeypatch.delenv("EFISCALIZA_CA_FILE", raising=False)
    payload = {
        "resultado": {"sucesso": True},
        "acaoInspecao": [{
            "coInspecAcao": {"value": "ACAO_2026_00162"},
            "noFiscalResponsavel": {
                "value": [{"Id": "71", "Label": "Responsável selecionado"}],
                "possible_values": [
                    {"Id": "71", "Label": "Responsável selecionado"},
                    {"Id": "72", "Label": "Outro fiscal"},
                ],
            },
        }],
    }
    cliente = Mock()
    cliente.open.return_value = io.BytesIO(json.dumps(payload).encode())
    monkeypatch.setattr(api_efiscaliza, "build_opener", Mock(return_value=cliente))

    acao = api_efiscaliza.consultar_acao(248368)

    pedido = cliente.open.call_args.args[0]
    assert pedido.get_method() == "GET"
    assert pedido.full_url.endswith("/acoes/248368")
    esquema, valor = pedido.get_header("Authorization").split()
    assert esquema == "Basic"
    assert base64.b64decode(valor) == b"fiscal-teste:"
    assert acao == api_efiscaliza.AcaoFiscalizacao(
        "ACAO_2026_00162", ("Responsável selecionado",), ("Outro fiscal",)
    )


def test_resposta_explicita_de_acao_inexistente() -> None:
    """Distingue a ação inexistente de um código textual encontrado.

    Args:
        None.

    Returns:
        None.
    """
    assert api_efiscaliza._interpretar_resposta({
        "acaoInspecao": [],
        "resultado": {"sucesso": False, "mensagem": "Nenhuma ação de inspeção encontrada."},
    }) is None
