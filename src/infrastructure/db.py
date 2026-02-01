import os
from pathlib import Path
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager

# importa Base desde tu módulo de modelos
from .models.models import Base
# <-- cambiado: importar configuración centralizada
from ..config import DATABASE_URL, DB_ECHO

# Opciones de conexión para sqlite vs otras bases
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, echo=DB_ECHO, future=True, connect_args=connect_args)

# Session factory (sin autocommit, sin autoflush por defecto)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

def init_db() -> None:
    """
    Crea las tablas declaradas en Base.metadata. Llamar al iniciar la aplicación.
    """
    Base.metadata.create_all(bind=engine)

@contextmanager
def get_db() -> Generator[Session, None, None]:
    """
    Context manager simple para obtener una sesión SQLAlchemy.
    Uso:
        with get_db() as db:
            ... usar db (db es Session)
    Para FastAPI, usar un generador con yield en la dependencia.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# FastAPI-compatible dependency (ejemplo)
def get_db_dependency():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
