"""Localiza a ação de fiscalização e associa os fiscais já cadastrados."""

from collections import defaultdict
from collections.abc import Iterable
from unicodedata import category, normalize

from src.infra.db_handler import DbRow
from src.utils.api_efiscaliza import AcaoFiscalizacao


def _normalizar_nome(nome: str) -> str:
    letras = "".join(c for c in normalize("NFD", nome.casefold()) if category(c) != "Mn")
    return " ".join(letras.split())


def sugerir_equipe(
    acao: AcaoFiscalizacao, fiscais: Iterable[DbRow]
) -> tuple[int | None, list[int]]:
    """Encontra os fiscais locais correspondentes às seleções da ação.

    Os IDs do eFiscaliza pertencem a outro sistema. São usados somente os
    nomes com correspondência única no cadastro local.

    Args:
        acao (AcaoFiscalizacao): Ação retornada pelo eFiscaliza.
        fiscais (Iterable[DbRow]): Registros locais com ID_FISCAL e NO_FISCAL.

    Returns:
        tuple[int | None, list[int]]: ID do único responsável encontrado, se
            houver, e IDs dos participantes encontrados, sem duplicatas.
    """
    por_nome: dict[str, list[int]] = defaultdict(list)
    for fiscal in fiscais:
        por_nome[_normalizar_nome(str(fiscal["NO_FISCAL"]))].append(int(fiscal["ID_FISCAL"]))

    def ids(nomes: tuple[str, ...]) -> list[int]:
        encontrados = (por_nome.get(_normalizar_nome(nome), []) for nome in nomes)
        return list(dict.fromkeys(opcoes[0] for opcoes in encontrados if len(opcoes) == 1))

    responsaveis = ids(acao.responsaveis)
    responsavel = responsaveis[0] if len(acao.responsaveis) == len(responsaveis) == 1 else None
    return responsavel, [fiscal for fiscal in ids(acao.participantes) if fiscal != responsavel]
