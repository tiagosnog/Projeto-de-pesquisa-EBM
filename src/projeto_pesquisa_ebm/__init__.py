"""
Projeto de pesquisa para o mestrado em Engenharia Biomédica UFABC
Análise de dados biomecânicos de corrida
"""

__version__ = "0.1.0"

from .utils import (
    load_markers_data,
    load_forces_data,
    calculate_trunk_cm,
    calculate_velocity,
    calculate_acceleration,
    normalize_grf,
    get_data_path,
)

from .models import MassSpringDamperModel

__all__ = [
    "load_markers_data",
    "load_forces_data",
    "calculate_trunk_cm",
    "calculate_velocity",
    "calculate_acceleration",
    "normalize_grf",
    "get_data_path",
    "MassSpringDamperModel",
]

