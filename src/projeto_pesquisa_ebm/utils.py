"""
Funções utilitárias para análise de dados biomecânicos
"""

import numpy as np
import pandas as pd
from pathlib import Path


def load_markers_data(filepath):
    """
    Carrega dados de markers de um arquivo .txt
    
    Parameters
    ----------
    filepath : str or Path
        Caminho para o arquivo de markers
        
    Returns
    -------
    pd.DataFrame
        DataFrame com os dados de markers
    """
    return pd.read_csv(filepath, sep='\t')


def load_forces_data(filepath):
    """
    Carrega dados de forças de um arquivo .txt
    
    Parameters
    ----------
    filepath : str or Path
        Caminho para o arquivo de forças
        
    Returns
    -------
    pd.DataFrame
        DataFrame com os dados de forças
    """
    return pd.read_csv(filepath, sep='\t')


def calculate_trunk_cm(data, markers=['R.ASIS', 'L.ASIS', 'R.PSIS', 'L.PSIS']):
    """
    Calcula o centro de massa do tronco a partir dos markers
    
    Parameters
    ----------
    data : pd.DataFrame
        DataFrame com os dados de markers
    markers : list
        Lista de markers para calcular o CM
        
    Returns
    -------
    np.ndarray
        Array com as coordenadas do centro de massa (x, y, z)
    """
    coords = []
    for marker in markers:
        x = data[f'{marker}X'].values
        y = data[f'{marker}Y'].values
        z = data[f'{marker}Z'].values
        coords.append(np.column_stack([x, y, z]))
    
    return np.mean(coords, axis=0)


def calculate_velocity(position, dt):
    """
    Calcula velocidade a partir da posição usando diferenças finitas
    
    Parameters
    ----------
    position : np.ndarray
        Array com dados de posição
    dt : float
        Intervalo de tempo entre amostras
        
    Returns
    -------
    np.ndarray
        Array com velocidades calculadas
    """
    return np.gradient(position, dt)


def calculate_acceleration(velocity, dt):
    """
    Calcula aceleração a partir da velocidade usando diferenças finitas
    
    Parameters
    ----------
    velocity : np.ndarray
        Array com dados de velocidade
    dt : float
        Intervalo de tempo entre amostras
        
    Returns
    -------
    np.ndarray
        Array com acelerações calculadas
    """
    return np.gradient(velocity, dt)


def normalize_grf(grf, mass):
    """
    Normaliza a força de reação do solo pela massa
    
    Parameters
    ----------
    grf : np.ndarray
        Array com dados de GRF
    mass : float
        Massa do sujeito em kg
        
    Returns
    -------
    np.ndarray
        GRF normalizada (em múltiplos do peso corporal)
    """
    g = 9.81  # m/s²
    weight = mass * g
    return grf / weight


def get_data_path(filename, data_type='raw'):
    """
    Retorna o caminho completo para um arquivo de dados
    
    Parameters
    ----------
    filename : str
        Nome do arquivo
    data_type : str
        Tipo de dados ('raw' ou 'processed')
        
    Returns
    -------
    Path
        Caminho completo para o arquivo
    """
    project_root = Path(__file__).parent.parent.parent
    return project_root / 'data' / data_type / filename

