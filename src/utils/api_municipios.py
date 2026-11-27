"""Consulta a malha municipal do Ibama por coordenadas."""

import json
import re
from http.client import HTTPException
from urllib.parse import urlencode
from urllib.request import Request, urlopen

# Endpoint de consulta espacial da camada de limites municipais do Ibama.
URL_MUNICIPIOS_IBAMA = (
    "https://pamgia.ibama.gov.br/server/rest/services/"
    "BasesSincronizadas/lim_municipios_ibge_a/FeatureServer/0/query"
)
TEMPO_LIMITE_CONSULTA = 5  # Segundos.


def localizar_codigos(latitude: float, longitude: float) -> list[int]:
    """Localiza os códigos IBGE dos municípios que intersectam um ponto.

    Args:
        latitude (float): Latitude em graus decimais, de -90 a 90.
        longitude (float): Longitude em graus decimais, de -180 a 180.

    Returns:
        list[int]: Códigos IBGE em ordem crescente, sem duplicatas. A lista é
            vazia se nenhum polígono intersectar o ponto e pode conter mais de
            um código se o ponto cair sobre uma divisa.

    Raises:
        ValueError: Se a latitude ou a longitude estiver fora do intervalo válido.
        RuntimeError: Se a requisição falhar ou a resposta do Ibama for inválida.
    """
    if not (-90 <= latitude <= 90 and -180 <= longitude <= 180):
        raise ValueError("Latitude ou longitude fora dos limites válidos.")

    # O ArcGIS recebe o ponto em ordem X, Y (longitude, latitude), com SRID 4326.
    parametros = urlencode({
        "f": "json",
        "geometry": f"{longitude},{latitude}",
        "geometryType": "esriGeometryPoint",
        "inSR": "4326",
        "spatialRel": "esriSpatialRelIntersects",
        "outFields": "cd_mun",
        "returnGeometry": "false",
    })

    # Identifica o aplicativo na requisição. O serviço rejeita o agente padrão do urllib.
    pedido = Request(
        f"{URL_MUNICIPIOS_IBAMA}?{parametros}",
        headers={"User-Agent": "AppEventos/1.0", "Accept": "application/json"},
    )
    try:
        with urlopen(pedido, timeout=TEMPO_LIMITE_CONSULTA) as resposta:
            dados = json.load(resposta)
    except (OSError, HTTPException, ValueError) as erro:
        raise RuntimeError("Falha na consulta ao Ibama.") from erro

    # O ArcGIS pode comunicar uma falha no JSON mesmo com status HTTP 200.
    if not isinstance(dados, dict) or "error" in dados or not isinstance(dados.get("features"), list):
        raise RuntimeError("Resposta inválida da consulta ao Ibama.")

    try:
        codigos = [item["attributes"]["cd_mun"] for item in dados["features"]]
    except (KeyError, TypeError) as erro:
        raise RuntimeError("A resposta do Ibama não contém geocódigos válidos.") from erro

    if any(not isinstance(codigo, str) or not re.fullmatch(r"[0-9]{7}", codigo) for codigo in codigos):
        raise RuntimeError("A resposta do Ibama não contém geocódigos válidos.")

    return sorted({int(codigo) for codigo in codigos})
