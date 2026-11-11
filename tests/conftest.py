"""Configuração comum dos testes."""

import pytest

from app.services import usuarios as servico_usuarios

UNIDADES_TESTE = [
    {"sigla": "GR01", "nome": "Gerência Regional no Estado de São Paulo"},
    {
        "sigla": "GR02",
        "nome": "Gerência Regional nos Estados do Rio de Janeiro e Espírito Santo",
    },
    {"sigla": "UO00.1", "nome": "Unidade Operacional do Distrito Federal"},
]


@pytest.fixture(autouse=True)
def lista_isolada(monkeypatch: pytest.MonkeyPatch) -> list[dict]:
    """Troca o acesso a TB_FISCAL por uma lista em memória, começando vazia."""
    lista: list[dict] = []

    def incluir(nome: str, unidade: str, papeis: set[str]) -> None:
        lista.append(
            {
                "nome": nome,
                "unidade": unidade,
                "coordenacao": int("coordenacao" in papeis),
                "abordagem": int("abordagem" in papeis),
                "monitoracao": int("monitoracao" in papeis),
            }
        )

    monkeypatch.setattr(servico_usuarios, "existe_usuario", lambda: bool(lista))
    monkeypatch.setattr(servico_usuarios, "listar_usuarios", lambda: list(lista))
    monkeypatch.setattr(servico_usuarios, "listar_unidades", lambda: UNIDADES_TESTE)
    monkeypatch.setattr(servico_usuarios, "incluir_usuario", incluir)
    return lista
