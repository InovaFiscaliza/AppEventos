"""Consulta ações de fiscalização na API interna do eFiscaliza.

O módulo lê uma credencial local, faz a requisição por HTTPS e extrai o
identificador textual da ação e os nomes selecionados de seus fiscais.
"""

import base64
import json
import os
import ssl
from dataclasses import dataclass
from http.client import HTTPException
from pathlib import Path
from urllib.request import HTTPRedirectHandler, HTTPSHandler, Request, build_opener

_URL_ACOES = "https://appsnet.anatel.gov.br/eFiscaliza_API/rest/servico/acoes/"
_ARQUIVO_CREDENCIAL = Path(__file__).resolve().parents[1] / ".secret" / ".secret_efiscaliza"


@dataclass(frozen=True)
class AcaoFiscalizacao:
    """Reúne os dados de inspeção aproveitados no cadastro de eventos.

    Args:
        identificador (str): Código textual da ação fornecido pelo eFiscaliza.
        responsaveis (tuple[str, ...]): Nomes selecionados como responsáveis.
            A tupla é vazia quando a API não informa responsáveis selecionados.
        participantes (tuple[str, ...]): Nomes da equipe, excluindo os
            responsáveis. A tupla é vazia quando a API não informa participantes.

    Returns:
        AcaoFiscalizacao: Identificador, responsáveis e participantes da ação.
    """

    identificador: str
    responsaveis: tuple[str, ...]
    participantes: tuple[str, ...]


class _SemRedirecionamento(HTTPRedirectHandler):
    """Mantém o cabeçalho de autenticação restrito à URL original."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        """Recusa o redirecionamento sugerido pelo servidor.

        Args:
            req (Request): Requisição original.
            fp (HTTPResponse): Resposta HTTP aberta pelo cliente.
            code (int): Código do redirecionamento.
            msg (str): Mensagem associada ao código HTTP.
            headers (HTTPMessage): Cabeçalhos da resposta.
            newurl (str): URL indicada pelo redirecionamento.

        Returns:
            None: Indica ao urllib que nenhuma nova requisição deve ser criada.
        """
        return None


def _nomes_selecionados(campo: object) -> tuple[str, ...]:
    """Extrai os nomes das opções selecionadas no eFiscaliza.

    Args:
        campo (object): Lista de opções selecionadas ou objeto que a contém
            na chave `value`.

    Returns:
        tuple[str, ...]: Nomes da chave `Label`, na ordem de origem e sem
            espaços nas extremidades. A tupla é vazia se não houver nomes válidos.
    """
    valores = campo.get("value") if isinstance(campo, dict) else campo
    if not isinstance(valores, list):
        return ()
    return tuple(
        item["Label"].strip()
        for item in valores
        if isinstance(item, dict) and isinstance(item.get("Label"), str) and item["Label"].strip()
    )


def _interpretar_resposta(dados: object) -> AcaoFiscalizacao | None:
    """Interpreta a resposta de uma consulta de ação de fiscalização.

    Args:
        dados (object): Conteúdo JSON já decodificado.

    Returns:
        AcaoFiscalizacao | None: Ação com código textual e fiscais informados,
            ou None quando o serviço indica explicitamente que a ação não existe.

    Raises:
        ValueError: Se a estrutura for inválida, se o serviço indicar falha
            ou se o retorno de sucesso não contiver uma ação com código textual.
    """
    if not isinstance(dados, dict):
        raise ValueError("Resposta do eFiscaliza inválida.")
    resultado = dados.get("resultado")
    acoes = dados.get("acaoInspecao")
    if not isinstance(resultado, dict) or not isinstance(acoes, list):
        raise ValueError("Resposta do eFiscaliza inválida.")

    if resultado.get("sucesso") is False and not acoes and (
        resultado.get("mensagem") == "Nenhuma ação de inspeção encontrada."
    ):
        return None
    if resultado.get("sucesso") is not True or len(acoes) != 1 or not isinstance(acoes[0], dict):
        raise ValueError("Resposta do eFiscaliza inválida.")

    acao = acoes[0]
    codigo = acao.get("coInspecAcao")
    identificador = codigo.get("value") if isinstance(codigo, dict) else None
    if not isinstance(identificador, str) or not identificador.strip():
        raise ValueError("A ação não possui código textual.")
    campo_responsavel = acao.get("noFiscalResponsavel")
    responsaveis = _nomes_selecionados(campo_responsavel)
    participantes = (
        campo_responsavel.get("possible_values") if isinstance(campo_responsavel, dict) else None
    )
    if participantes is None:
        participantes = acao.get("noFiscalParticipante") or acao.get("noFiscaisParticipantes")

    # No eFiscaliza, value indica o responsável e possible_values reúne a equipe.
    nomes_responsaveis = {nome.casefold() for nome in responsaveis}
    nomes_participantes = tuple(dict.fromkeys(
        nome for nome in _nomes_selecionados(participantes)
        if nome.casefold() not in nomes_responsaveis
    ))
    return AcaoFiscalizacao(identificador.strip(), responsaveis, nomes_participantes)


def consultar_acao(codigo: int) -> AcaoFiscalizacao | None:
    """Consulta uma ação de fiscalização pelo código numérico.

    A requisição GET usa HTTP Basic com senha vazia. O arquivo
    `src/.secret/.secret_efiscaliza` pode conter só o usuário ou uma entrada
    `user` com separador `=` ou `:`. A CA de `EFISCALIZA_CA_FILE` ou do
    arquivo local `efiscaliza-ca.pem` complementa a verificação TLS padrão.
    O tempo limite da requisição é de cinco segundos.

    Args:
        codigo (int): Código numérico da ação de fiscalização.

    Returns:
        AcaoFiscalizacao | None: Ação encontrada ou None para a resposta
            explícita de ação inexistente.

    Raises:
        RuntimeError: Se o arquivo da credencial não puder ser lido, o usuário
            estiver ausente, a conexão ou o serviço falhar, ou a resposta for inválida.
    """
    try:
        registro = _ARQUIVO_CREDENCIAL.read_text(encoding="utf-8-sig").strip()
        chave, separador, valor = registro.partition("=" if "=" in registro else ":")
        if separador and chave.strip().strip('"\'') != "user":
            raise ValueError("Entrada de usuário do eFiscaliza inválida.")
        usuario = (valor if separador else chave).strip().removesuffix(",").strip().strip('"\'')
        if not usuario:
            raise ValueError("Usuário do eFiscaliza ausente.")
        credencial = base64.b64encode(f"{usuario}:".encode()).decode("ascii")
        contexto = ssl.create_default_context()
        if ca := os.environ.get("EFISCALIZA_CA_FILE"):
            contexto.load_verify_locations(cafile=ca)
        else:
            ca_local = _ARQUIVO_CREDENCIAL.with_name("efiscaliza-ca.pem")
            if ca_local.is_file():
                contexto.load_verify_locations(cafile=ca_local)
        cliente = build_opener(HTTPSHandler(context=contexto), _SemRedirecionamento())
        pedido = Request(
            f"{_URL_ACOES}{codigo}",
            headers={"Authorization": f"Basic {credencial}", "Accept": "application/json"},
        )
        with cliente.open(pedido, timeout=5) as resposta:
            return _interpretar_resposta(json.load(resposta))
    except (HTTPException, OSError, ValueError):
        raise RuntimeError("Não foi possível consultar o eFiscaliza.") from None
