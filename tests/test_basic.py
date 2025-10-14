"""
Testes básicos para o projeto
"""

import pytest
import numpy as np
import pandas as pd


def test_numpy_import():
    """Testa se numpy está instalado corretamente"""
    assert np.__version__ is not None


def test_pandas_import():
    """Testa se pandas está instalado corretamente"""
    assert pd.__version__ is not None


def test_basic_calculation():
    """Testa cálculos básicos com numpy"""
    arr = np.array([1, 2, 3, 4, 5])
    assert arr.mean() == 3.0
    assert arr.sum() == 15


def test_dataframe_creation():
    """Testa criação de DataFrame"""
    df = pd.DataFrame({
        'A': [1, 2, 3],
        'B': [4, 5, 6]
    })
    assert len(df) == 3
    assert list(df.columns) == ['A', 'B']


if __name__ == "__main__":
    pytest.main([__file__])

