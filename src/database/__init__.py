"""
Módulo de acceso a datos y conexión con Supabase en Tercera Forma Normal (3FN).
"""

from src.database.connection import get_supabase_client
from src.database.repository import (
    execute_atomic_survey_transaction,
    fetch_all_surveys_joined,
    fetch_catalogs,
)

__all__ = [
    "get_supabase_client",
    "execute_atomic_survey_transaction",
    "fetch_all_surveys_joined",
    "fetch_catalogs",
]
