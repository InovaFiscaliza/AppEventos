"""Engine SQLAlchemy central."""

import os

from psycopg.conninfo import make_conninfo
from sqlalchemy import create_engine
from sqlalchemy.engine import URL, make_url

from src.config import DB_CFG

DATABASE_URL = os.environ.get("DATABASE_URL") or URL.create(
    "postgresql+psycopg",
    username=DB_CFG["user"],
    password=DB_CFG["password"],
    host=DB_CFG["address"],
    port=DB_CFG["port"],
    database=DB_CFG["database"],
)
engine = create_engine(DATABASE_URL, pool_pre_ping=True)


def conninfo() -> str:
    """Converte a configuração compartilhada em parâmetros libpq para o handler."""
    url = make_url(DATABASE_URL)
    parametros = dict(url.query)
    parametros.update(url.translate_connect_args(username="user", database="dbname"))
    return make_conninfo(**parametros)
