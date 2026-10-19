"""
Módulo de conexión Singleton con el SDK oficial de Supabase.
Garantiza una única instancia reutilizable del cliente Supabase sin concatenación SQL.
"""

from __future__ import annotations

import logging
import os
from typing import Optional
from dotenv import load_dotenv
from supabase import Client, create_client

logger = logging.getLogger(__name__)

_supabase_client: Optional[Client] = None


def get_supabase_client() -> Client:
    """
    Obtiene o inicializa la instancia Singleton del cliente Supabase.

    Returns:
        Client: Instancia configurada del cliente oficial de Supabase.

    Raises:
        ValueError: Si SUPABASE_URL o SUPABASE_KEY no están configuradas en el entorno.
    """
    global _supabase_client
    if _supabase_client is not None:
        return _supabase_client

    load_dotenv()

    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")

    if not supabase_url or not supabase_key:
        logger.error("Credenciales de Supabase no encontradas en el entorno.")
        raise ValueError(
            "Variables de entorno SUPABASE_URL y/o SUPABASE_KEY no configuradas."
        )

    logger.info("Inicializando conexión Singleton con Supabase SDK (Host: %s)...", supabase_url)
    _supabase_client = create_client(supabase_url, supabase_key)
    logger.info("Conexión con Supabase SDK establecida exitosamente.")

    return _supabase_client


def reset_supabase_client() -> None:
    """
    Restablece la instancia Singleton del cliente Supabase (útil para pruebas unitarias).
    """
    global _supabase_client
    _supabase_client = None
