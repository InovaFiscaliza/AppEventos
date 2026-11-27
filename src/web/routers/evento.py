"""Cadastro de eventos e consulta de município por coordenadas."""

from dataclasses import asdict
from pathlib import Path
from posixpath import dirname, relpath

from fastapi import APIRouter, Depends, Form, HTTPException, Query, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from psycopg import Error

from src.modules.eventos.acao_fiscalizacao import sugerir_equipe
from src.modules.eventos.cadastro import (
    CadastroIndisponivel,
    CadastroInvalido,
    DadosCadastroEvento,
    cadastrar_evento,
)
from src.modules.eventos.municipio_por_coordenadas import identificar_municipio
from src.modules.fiscais.persistencia import listar_fiscais_para_evento
from src.modules.sessao import sessao_fiscal
from src.utils import api_efiscaliza

router = APIRouter(dependencies=[Depends(sessao_fiscal.sincronizar_sessao_rf_fusion)])
templates = Jinja2Templates(
    directory=Path(__file__).resolve().parent.parent / "templates",
    context_processors=[sessao_fiscal.contexto_perfil_cabecalho],
)


def _renderizar_formulario(
    request: Request, dados: dict | None = None, status_code: int = 200
) -> HTMLResponse:
    try:
        fiscais = listar_fiscais_para_evento()
    except Error:
        if status_code != 503:
            raise
        fiscais = []
    # O navegador resolve o caminho relativo mesmo quando o proxy remove
    # o prefixo público antes de encaminhar a requisição ao FastAPI.
    consulta_municipio_url = relpath(
        request.app.url_path_for("consultar_municipio"),
        start=dirname(request.scope["route"].path),
    )
    contexto = {
        "tipo_cadastro": "evento",
        "fiscais": fiscais,
        "consulta_municipio_url": consulta_municipio_url,
        "consulta_acao_url": relpath(
            request.app.url_path_for("consultar_acao_fiscalizacao"),
            start=dirname(request.scope["route"].path),
        ),
    }
    if dados:
        contexto.update(dados)
    return templates.TemplateResponse(
        request=request, name="cadastro/evento_novo.html", context=contexto, status_code=status_code
    )


@router.get("/eventos/novo", response_class=HTMLResponse, name="novo_evento")
@router.get("/cadastro/evento", response_class=HTMLResponse, name="cadastro_evento")
def novo_evento(request: Request) -> HTMLResponse:
    """Exibe o formulário de criação de evento.

    Args:
        request (Request): Requisição usada para renderizar o template.

    Returns:
        HTMLResponse: Formulário com os fiscais cadastrados.
    """
    return _renderizar_formulario(request)


@router.get("/eventos/municipio", name="consultar_municipio")
def consultar_municipio(
    latitude: float = Query(ge=-90, le=90),
    longitude: float = Query(ge=-180, le=180),
) -> dict[str, int | str] | None:
    """Consulta o município cadastrado para o ponto informado.

    Args:
        latitude (float): Latitude em graus decimais, de -90 a 90.
        longitude (float): Longitude em graus decimais, de -180 a 180.

    Returns:
        dict[str, int | str] | None: Código IBGE, nome e UF de uma correspondência
            única, ou None quando o ponto não puder ser associado a um município.

    Raises:
        HTTPException: Com status 503 se a consulta ao Ibama falhar.
    """
    try:
        return identificar_municipio(latitude, longitude)
    except RuntimeError as erro:
        raise HTTPException(503, "Consulta de município indisponível.") from erro


@router.get("/eventos/acao-fiscalizacao", name="consultar_acao_fiscalizacao")
def consultar_acao_fiscalizacao(
    codigo: int = Query(ge=1, le=2_147_483_647),
) -> dict:
    """Valida o código da ação e sugere a equipe já cadastrada no AppEventos.

    Args:
        codigo (int): Código numérico informado no formulário.

    Returns:
        dict: Identificador textual, IDs locais sugeridos e indicação de
            participantes que não puderam ser associados.

    Raises:
        HTTPException: Com status 404 se a ação não existir ou 503 se a
            integração ou a consulta dos fiscais falhar.
    """
    try:
        acao = api_efiscaliza.consultar_acao(codigo)
        if acao is None:
            raise HTTPException(404, "Nenhuma ação de inspeção encontrada para esse código.")
        responsavel, participantes = sugerir_equipe(acao, listar_fiscais_para_evento())
    except (Error, RuntimeError) as erro:
        raise HTTPException(503, "Não foi possível consultar a ação no eFiscaliza.") from erro
    return {
        "identificador": acao.identificador,
        "responsavel": responsavel,
        "participantes": participantes,
        "equipe_incompleta": bool(acao.responsaveis and responsavel is None)
        or len(participantes) < len(acao.participantes),
    }


@router.post("/eventos/novo", name="salvar_evento", response_model=None)
@router.post("/cadastro/evento", name="salvar_cadastro_evento", response_model=None)
def salvar_evento(
    request: Request,
    nome: str = Form(""),
    data_inicio: str = Form(""),
    data_fim: str = Form(""),
    latitude: str = Form(""),
    longitude: str = Form(""),
    id_fiscal_responsavel: str = Form(""),
    teste_etiquetagem: str = Form("0"),
    observacao: str = Form(""),
    ids_fiscais: list[str] | None = Form(None),
    codigo_acao: str = Form(""),
) -> HTMLResponse | RedirectResponse:
    """Valida e grava o evento e os vínculos da equipe de fiscalização.

    O evento e a equipe são gravados em uma única transação.

    Args:
        request (Request): Requisição usada para renderizar erros no formulário.
        nome (str): Nome obrigatório do evento.
        data_inicio (str): Data de início em formato ISO ou texto vazio.
        data_fim (str): Data de fim em formato ISO ou texto vazio.
        latitude (str): Latitude digitada ou preenchida pelo mapa.
        longitude (str): Longitude digitada ou preenchida pelo mapa.
        id_fiscal_responsavel (str): Identificador do fiscal ou texto vazio.
        teste_etiquetagem (str): Indicador enviado pelo formulário, 0 ou 1.
        observacao (str): Texto livre sobre o evento.
        ids_fiscais (list[str] | None): Identificadores dos fiscais adicionados à equipe.
        codigo_acao (str): Código numérico de fiscalização ou texto vazio.

    Returns:
        HTMLResponse | RedirectResponse: Formulário com os valores e o erro
            encontrado, ou redirecionamento à página inicial após gravar.
    """
    dados = DadosCadastroEvento(
        nome=nome,
        data_inicio=data_inicio,
        data_fim=data_fim,
        latitude=latitude,
        longitude=longitude,
        id_fiscal_responsavel=id_fiscal_responsavel,
        teste_etiquetagem=teste_etiquetagem,
        observacao=observacao,
        ids_fiscais=ids_fiscais or [],
        codigo_acao=codigo_acao,
    )
    try:
        cadastrar_evento(dados)
    except CadastroInvalido as erro:
        contexto = {
            **asdict(dados),
            "nome": dados.nome.strip(),
            "municipio": erro.municipio,
            "erro": str(erro),
        }
        status = 503 if isinstance(erro, CadastroIndisponivel) else 400
        return _renderizar_formulario(request, contexto, status)
    # Os dois endpoints de gravação ficam um nível abaixo da raiz pública.
    return RedirectResponse(url="../", status_code=303)
