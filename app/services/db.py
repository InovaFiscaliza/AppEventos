"""Engine SQLAlchemy central."""

import os

from sqlalchemy import create_engine

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql+psycopg://appeventos:appPasswd@localhost:5433/appeventos",
)
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
