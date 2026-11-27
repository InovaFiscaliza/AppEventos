"""Valida e registra um evento com sua equipe e seu município."""

from contextlib import closing
from dataclasses import dataclass
from datetime import date
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation

from psycopg import Error
from psycopg.errors import ForeignKeyViolation

from src.modules.eventos.municipio_por_coordenadas import identificar_municipio
from src.modules.eventos.persistencia import EventoHandler
from src.utils import api_efiscaliza


@dataclass
class DadosCadastroEvento:
    """Agrupa os valores recebidos para cadastrar o evento.

    Args:
        nome (str): Nome do evento.
        data_inicio (str): Data inicial em formato ISO ou texto vazio.
        data_fim (str): Data final em formato ISO ou texto vazio.
        latitude (str): Latitude em graus decimais ou texto vazio.
        longitude (str): Longitude em graus decimais ou texto vazio.
        id_fiscal_responsavel (str): ID do responsável ou texto vazio.
        teste_etiquetagem (str): Indicador de teste, 0 ou 1.
        observacao (str): Texto livre sobre o evento.
        ids_fiscais (list[str]): IDs dos fiscais selecionados.
        codigo_acao (str): Código numérico da ação ou texto vazio.

    Returns:
        DadosCadastroEvento: Valores ainda sujeitos às regras de validação.
    """

    nome: str
    data_inicio: str
    data_fim: str
    latitude: str
    longitude: str
    id_fiscal_responsavel: str
    teste_etiquetagem: str
    observacao: str
    ids_fiscais: list[str]
    codigo_acao: str = ""


class CadastroInvalido(ValueError):
    """Indica uma validação de cadastro que o usuário pode corrigir.

    Args:
        mensagem (str): Motivo da falha.
        municipio (str | None): Município já identificado, se houver.

    Returns:
        CadastroInvalido: Erro com o município para reapresentar no formulário.
    """

    def __init__(self, mensagem: str, municipio: str | None = None) -> None:
        super().__init__(mensagem)
        self.municipio = municipio


class CadastroIndisponivel(CadastroInvalido):
    """Indica falha em uma dependência usada pelo cadastro.

    Args:
        mensagem (str): Motivo da indisponibilidade.
        municipio (str | None): Município já identificado, se houver.

    Returns:
        CadastroIndisponivel: Erro com o município para reapresentar no formulário.
    """


def _converter_data(valor: str) -> date | None:
    """Converte uma data enviada pelo formulário.

    Args:
        valor (str): Data no formato AAAA-MM-DD ou texto vazio.

    Returns:
        date | None: Data convertida ou None se o campo estiver vazio.

    Raises:
        ValueError: Se o valor preenchido não representar uma data válida.
    """
    return date.fromisoformat(valor) if valor else None


def _converter_coordenada(valor: str, limite: int) -> Decimal:
    try:
        coordenada = Decimal(valor)
    except InvalidOperation as erro:
        raise ValueError("Informe coordenadas válidas.") from erro

    if not coordenada.is_finite() or not -limite <= coordenada <= limite:
        raise ValueError("Informe coordenadas válidas.")

    # A consulta usa a mesma precisão de seis casas decimais da TB_EVENTO.
    return coordenada.quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)


def cadastrar_evento(dados: DadosCadastroEvento) -> None:
    """Valida os dados e grava o evento e a equipe em uma transação.

    Args:
        dados (DadosCadastroEvento): Valores recebidos para o cadastro.

    Returns:
        None.

    Raises:
        CadastroInvalido: Se os dados ou os fiscais selecionados forem inválidos.
        CadastroIndisponivel: Se uma dependência falhar durante o cadastro.
        psycopg.Error: Se a leitura do cadastro de municípios falhar.
        RuntimeError: Se a gravação não retornar o ID do evento.
    """
    nome = dados.nome.strip()
    if not nome:
        raise CadastroInvalido("Informe o nome do evento.")
    if len(nome) > 200:
        raise CadastroInvalido("O nome do evento deve ter até 200 caracteres.")

    try:
        inicio = _converter_data(dados.data_inicio)
        fim = _converter_data(dados.data_fim)
    except ValueError as erro:
        raise CadastroInvalido("Informe datas válidas.") from erro
    if inicio and fim and fim < inicio:
        raise CadastroInvalido("A data de fim não pode ser anterior à data de início.")

    try:
        fiscal = int(dados.id_fiscal_responsavel) if dados.id_fiscal_responsavel else None
    except ValueError as erro:
        raise CadastroInvalido("Selecione um fiscal responsável válido.") from erro
    if fiscal is not None and not 1 <= fiscal <= 2_147_483_647:
        raise CadastroInvalido("Selecione um fiscal responsável válido.")

    try:
        equipe = {int(identificador) for identificador in dados.ids_fiscais}
    except ValueError as erro:
        raise CadastroInvalido("Selecione fiscais válidos para a equipe.") from erro
    if any(not 1 <= identificador <= 2_147_483_647 for identificador in equipe):
        raise CadastroInvalido("Selecione fiscais válidos para a equipe.")
    if fiscal is not None:
        equipe.add(fiscal)

    if dados.teste_etiquetagem not in ("0", "1"):
        raise CadastroInvalido("Informe se o evento possui teste de etiquetagem.")

    latitude, longitude = dados.latitude, dados.longitude
    lat = lon = None
    municipio = None
    municipio_formatado = None
    if latitude or longitude:
        if not latitude or not longitude:
            raise CadastroInvalido("Informe a latitude e a longitude.")
        try:
            lat = _converter_coordenada(latitude, 90)
            lon = _converter_coordenada(longitude, 180)
        except ValueError as erro:
            raise CadastroInvalido(str(erro)) from erro
        try:
            municipio = identificar_municipio(float(lat), float(lon))
        except RuntimeError as erro:
            raise CadastroIndisponivel(
                "Não foi possível consultar o município. Tente novamente."
            ) from erro
        if municipio is None:
            raise CadastroInvalido("Não foi possível identificar um município único para esse ponto.")
        municipio_formatado = f"{municipio['nome']} ({municipio['uf']})"

    codigo_acao = None
    acao = None
    if dados.codigo_acao.strip():
        valor = dados.codigo_acao.strip()
        if not valor.isascii() or not valor.isdecimal() or len(valor) > 10 or not 1 <= int(valor) <= 2_147_483_647:
            raise CadastroInvalido("Informe um código de ação válido.", municipio_formatado)
        codigo_acao = int(valor)
        try:
            acao = api_efiscaliza.consultar_acao(codigo_acao)
        except RuntimeError as erro:
            raise CadastroIndisponivel(
                "Não foi possível validar a ação no eFiscaliza.", municipio_formatado
            ) from erro
        if acao is None:
            raise CadastroInvalido(
                "Nenhuma ação de inspeção encontrada para esse código.", municipio_formatado
            )

    try:
        with closing(EventoHandler()) as handler:
            handler.gravar_evento(
                {
                    "NO_EVENTO": nome,
                    "DT_INICIO": inicio,
                    "DT_FIM": fim,
                    "VR_LATITUDE": lat,
                    "VR_LONGITUDE": lon,
                    "CO_MUNICIPIO_IBGE": municipio["codigo"] if municipio else None,
                    "ID_FISCAL_RESPONSAVEL": fiscal,
                    "IC_TESTE_ETIQUETAGEM": int(dados.teste_etiquetagem),
                    "TX_OBSERVACAO": dados.observacao or None,
                    "CO_ACAO_FISCALIZACAO": codigo_acao,
                    "TX_ACAO_FISCALIZACAO": acao.identificador if acao else None,
                },
                equipe,
            )
    except ForeignKeyViolation as erro:
        restricao = erro.diag.constraint_name
        if restricao == "FK_TB_EVENTO_TB_FISCAL_RESPONSAVEL":
            raise CadastroInvalido(
                "O fiscal selecionado não está mais disponível.", municipio_formatado
            ) from erro
        if restricao == "FK_TB_EVENTO_FISCAL_TB_FISCAL":
            raise CadastroInvalido(
                "Um dos fiscais da equipe não está mais disponível.", municipio_formatado
            ) from erro
        raise CadastroIndisponivel(
            "Não foi possível gravar o evento no banco de dados.", municipio_formatado
        ) from erro
    except Error as erro:
        raise CadastroIndisponivel(
            "Não foi possível gravar o evento no banco de dados.", municipio_formatado
        ) from erro
