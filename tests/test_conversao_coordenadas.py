"""
Testes para validar a conversão de coordenadas entre dados experimentais e modelo Liu 2000
"""

import numpy as np
import pytest


def test_conversao_posicao_basica():
    """
    Testa a conversão básica de posição
    """
    # Dados de exemplo
    p_ref = 1.0  # posição inicial (1m acima do solo)
    p_exp = 0.9  # posição experimental (0.9m acima do solo)
    
    # Conversão
    p_modelo = p_ref - p_exp
    
    # Verificação: massa desceu 0.1m, então p_modelo deve ser positivo
    assert p_modelo == 0.1, f"Esperado 0.1, obtido {p_modelo}"
    assert p_modelo > 0, "Massa desceu, p_modelo deve ser positivo"


def test_conversao_posicao_massa_subiu():
    """
    Testa conversão quando a massa sobe
    """
    p_ref = 1.0  # posição inicial
    p_exp = 1.1  # massa subiu 0.1m
    
    p_modelo = p_ref - p_exp
    
    # Massa subiu, p_modelo deve ser negativo
    assert p_modelo == -0.1, f"Esperado -0.1, obtido {p_modelo}"
    assert p_modelo < 0, "Massa subiu, p_modelo deve ser negativo"


def test_conversao_posicao_massa_na_referencia():
    """
    Testa conversão quando a massa está na posição de referência
    """
    p_ref = 1.0
    p_exp = 1.0  # mesma posição
    
    p_modelo = p_ref - p_exp
    
    assert p_modelo == 0.0, f"Esperado 0.0, obtido {p_modelo}"


def test_conversao_velocidade():
    """
    Testa a conversão de velocidade
    """
    # Velocidade experimental positiva (subindo)
    v_exp = 0.5  # m/s para cima
    v_modelo = -v_exp
    
    assert v_modelo == -0.5, f"Esperado -0.5, obtido {v_modelo}"
    assert v_modelo < 0, "Velocidade para cima deve ser negativa no modelo"
    
    # Velocidade experimental negativa (descendo)
    v_exp = -0.3  # m/s para baixo
    v_modelo = -v_exp
    
    assert v_modelo == 0.3, f"Esperado 0.3, obtido {v_modelo}"
    assert v_modelo > 0, "Velocidade para baixo deve ser positiva no modelo"


def test_conversao_array_posicoes():
    """
    Testa conversão de um array de posições
    """
    p_ref = 1.0
    p_exp = np.array([1.0, 0.95, 0.90, 0.95, 1.0])
    
    p_modelo = p_ref - p_exp
    
    esperado = np.array([0.0, 0.05, 0.10, 0.05, 0.0])
    
    np.testing.assert_array_almost_equal(p_modelo, esperado, decimal=10)


def test_conversao_array_velocidades():
    """
    Testa conversão de um array de velocidades
    """
    v_exp = np.array([0.0, 0.5, 0.0, -0.5, 0.0])
    v_modelo = -v_exp
    
    esperado = np.array([0.0, -0.5, 0.0, 0.5, 0.0])
    
    np.testing.assert_array_almost_equal(v_modelo, esperado, decimal=10)


def test_consistencia_posicao_velocidade():
    """
    Testa se a conversão mantém consistência entre posição e velocidade
    """
    # Simular movimento: massa descendo
    dt = 0.01  # s
    t = np.arange(0, 1, dt)
    
    # Posição experimental: massa descendo de 1.0m para 0.5m
    p_ref = 1.0
    p_exp = 1.0 - 0.5 * t  # descendo linearmente
    
    # Converter posição
    p_modelo = p_ref - p_exp
    
    # Calcular velocidade do modelo
    v_modelo_calculada = np.gradient(p_modelo, dt)
    
    # Velocidade experimental
    v_exp = np.gradient(p_exp, dt)
    v_modelo_convertida = -v_exp
    
    # As duas formas de calcular v_modelo devem ser consistentes
    np.testing.assert_array_almost_equal(
        v_modelo_calculada, 
        v_modelo_convertida, 
        decimal=5
    )


def test_conversao_preserva_magnitude():
    """
    Testa se a conversão preserva a magnitude do deslocamento
    """
    p_ref = 1.0
    p_exp_inicial = 1.0
    p_exp_final = 0.8
    
    # Deslocamento experimental
    delta_exp = abs(p_exp_final - p_exp_inicial)
    
    # Deslocamento no modelo
    p_modelo_inicial = p_ref - p_exp_inicial
    p_modelo_final = p_ref - p_exp_final
    delta_modelo = abs(p_modelo_final - p_modelo_inicial)
    
    # Magnitudes devem ser iguais
    assert abs(delta_exp - delta_modelo) < 1e-10, \
        f"Magnitudes diferentes: exp={delta_exp}, modelo={delta_modelo}"


def test_conversao_multiplas_massas():
    """
    Testa conversão para múltiplas massas simultaneamente
    """
    # Posições de referência
    p_refs = np.array([0.1, 0.5, 1.0, 1.2])  # heel, knee, trunk, crest
    
    # Posições experimentais em um instante
    p_exps = np.array([0.08, 0.48, 0.98, 1.18])
    
    # Conversão
    p_modelos = p_refs - p_exps
    
    # Todas as massas desceram
    esperado = np.array([0.02, 0.02, 0.02, 0.02])
    
    np.testing.assert_array_almost_equal(p_modelos, esperado, decimal=10)
    assert np.all(p_modelos > 0), "Todas as massas desceram, p_modelo deve ser positivo"


def test_conversao_inversa():
    """
    Testa se a conversão inversa recupera os dados originais
    """
    p_ref = 1.0
    p_exp_original = 0.85
    
    # Conversão direta
    p_modelo = p_ref - p_exp_original
    
    # Conversão inversa
    p_exp_recuperado = p_ref - p_modelo
    
    assert abs(p_exp_original - p_exp_recuperado) < 1e-10, \
        f"Conversão inversa falhou: original={p_exp_original}, recuperado={p_exp_recuperado}"


def test_exemplo_real_liu2000():
    """
    Testa com valores realistas do modelo Liu 2000
    """
    # Valores típicos de referência (em metros)
    p1_ref = 0.05   # heel próximo ao solo
    p2_ref = 0.50   # knee
    p3_ref = 1.00   # trunk
    p4_ref = 1.10   # crest
    
    # Durante impacto, massas descem
    p1_exp = 0.03   # heel desceu 2cm
    p2_exp = 0.48   # knee desceu 2cm
    p3_exp = 0.98   # trunk desceu 2cm
    p4_exp = 1.08   # crest desceu 2cm
    
    # Conversão
    p1_modelo = p1_ref - p1_exp
    p2_modelo = p2_ref - p2_exp
    p3_modelo = p3_ref - p3_exp
    p4_modelo = p4_ref - p4_exp
    
    # Todas devem ser positivas (massas desceram)
    assert p1_modelo > 0, "p1 deve ser positivo (massa desceu)"
    assert p2_modelo > 0, "p2 deve ser positivo (massa desceu)"
    assert p3_modelo > 0, "p3 deve ser positivo (massa desceu)"
    assert p4_modelo > 0, "p4 deve ser positivo (massa desceu)"
    
    # Verificar valores esperados
    assert abs(p1_modelo - 0.02) < 1e-10
    assert abs(p2_modelo - 0.02) < 1e-10
    assert abs(p3_modelo - 0.02) < 1e-10
    assert abs(p4_modelo - 0.02) < 1e-10


if __name__ == "__main__":
    # Executar todos os testes
    pytest.main([__file__, "-v"])

