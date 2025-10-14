#!/usr/bin/env python3
"""
Correções sugeridas para o modelo Liu & Nigg 2000
"""

import numpy as np

def simulacao_euler_completa(time_d, MGRF, m1, m2, m3, m4, g, 
                           k1_otim, k2_otim, k3_otim, k4_otim, k5_otim,
                           c1_otim, c2_otim, c4_otim):
    """
    Simulação de Euler completa para o modelo de 4 massas
    """
    dt_d = time_d[1] - time_d[0]
    n_steps = len(time_d)
    
    # Inicializar arrays para todas as massas
    p1_sim = np.zeros(n_steps)
    v1_sim = np.zeros(n_steps)
    p2_sim = np.zeros(n_steps)
    v2_sim = np.zeros(n_steps)
    p3_sim = np.zeros(n_steps)
    v3_sim = np.zeros(n_steps)
    p4_sim = np.zeros(n_steps)
    v4_sim = np.zeros(n_steps)
    
    # Condições iniciais
    p1_sim[0] = 0
    p2_sim[0] = 0
    p3_sim[0] = 0
    p4_sim[0] = 0
    v1_sim[0] = 0
    v2_sim[0] = 0
    v3_sim[0] = 0
    v4_sim[0] = 0
    
    for i in range(n_steps - 1):
        # Equação para massa 1 (pé)
        # m1*a1 = m1*g - MGRF - k1*(p1 - p3) - k2*(p1 - p2) - c1*(v1 - v3) - c2*(v1 - v2)
        dv1dt = (m1 * g - MGRF[i] - k1_otim * (p1_sim[i] - p3_sim[i]) - 
                 k2_otim * (p1_sim[i] - p2_sim[i]) - c1_otim * (v1_sim[i] - v3_sim[i]) - 
                 c2_otim * (v1_sim[i] - v2_sim[i])) / m1
        
        # Equação para massa 2 (perna)
        # m2*a2 = m2*g + k2*(p1 - p2) - k3*(p2 - p3) + c2*(v1 - v2)
        dv2dt = (m2 * g + k2_otim * (p1_sim[i] - p2_sim[i]) - 
                 k3_otim * (p2_sim[i] - p3_sim[i]) + c2_otim * (v1_sim[i] - v2_sim[i])) / m2
        
        # Equação para massa 3 (coxa)
        # m3*a3 = m3*g + k1*(p1 - p3) + k3*(p2 - p3) - (k4 + k5)*(p3 - p4) + c1*(v1 - v3) - c4*(v3 - v4)
        dv3dt = (m3 * g + k1_otim * (p1_sim[i] - p3_sim[i]) + 
                 k3_otim * (p2_sim[i] - p3_sim[i]) - (k4_otim + k5_otim) * (p3_sim[i] - p4_sim[i]) + 
                 c1_otim * (v1_sim[i] - v3_sim[i]) - c4_otim * (v3_sim[i] - v4_sim[i])) / m3
        
        # Equação para massa 4 (tronco)
        # m4*a4 = m4*g + (k4 + k5)*(p3 - p4) + c4*(v3 - v4)
        dv4dt = (m4 * g + (k4_otim + k5_otim) * (p3_sim[i] - p4_sim[i]) + 
                 c4_otim * (v3_sim[i] - v4_sim[i])) / m4
        
        # Atualizar velocidades
        v1_sim[i + 1] = v1_sim[i] + dv1dt * dt_d
        v2_sim[i + 1] = v2_sim[i] + dv2dt * dt_d
        v3_sim[i + 1] = v3_sim[i] + dv3dt * dt_d
        v4_sim[i + 1] = v4_sim[i] + dv4dt * dt_d
        
        # Atualizar posições
        p1_sim[i + 1] = p1_sim[i] + v1_sim[i] * dt_d
        p2_sim[i + 1] = p2_sim[i] + v2_sim[i] * dt_d
        p3_sim[i + 1] = p3_sim[i] + v3_sim[i] * dt_d
        p4_sim[i + 1] = p4_sim[i] + v4_sim[i] * dt_d
    
    return p1_sim, p2_sim, p3_sim, p4_sim, v1_sim, v2_sim, v3_sim, v4_sim


def erro_3_massa4(delta, m4, a4_s, g, k4_otim, k5_otim, p3_s, p4_s, v3_s, v4_s):
    """
    Função de erro para otimização da massa 4
    Nota: Esta função pode não ser necessária se k4, k5, c4 já foram otimizados nas outras massas
    """
    # m4*a4_s = m4*g + (k4 + k5)*(p3_s - p4_s) + c4*(v3_s - v4_s)
    # delta[0] = c4_otim (se ainda não foi otimizado)
    return np.sum((m4*a4_s - (m4*g + (k4_otim + k5_otim)*(p3_s - p4_s) + delta[0]*(v3_s - v4_s)))**2)


def verificar_estabilidade_sistema(k1, k2, k3, k4, k5, c1, c2, c4, m1, m2, m3, m4):
    """
    Verificar a estabilidade do sistema através da matriz de estado
    """
    # Matriz de massa
    M = np.diag([m1, m2, m3, m4])
    
    # Matriz de rigidez
    K = np.array([
        [k1 + k2, -k2, -k1, 0],
        [-k2, k2 + k3, -k3, 0],
        [-k1, -k3, k1 + k3 + k4 + k5, -(k4 + k5)],
        [0, 0, -(k4 + k5), k4 + k5]
    ])
    
    # Matriz de amortecimento
    C = np.array([
        [c1 + c2, -c2, -c1, 0],
        [-c2, c2, 0, 0],
        [-c1, 0, c1 + c4, -c4],
        [0, 0, -c4, c4]
    ])
    
    # Matriz de estado A = [0, I; -M^(-1)*K, -M^(-1)*C]
    M_inv = np.linalg.inv(M)
    zeros = np.zeros((4, 4))
    I = np.eye(4)
    
    A = np.block([
        [zeros, I],
        [-M_inv @ K, -M_inv @ C]
    ])
    
    # Calcular autovalores
    eigenvalues = np.linalg.eigvals(A)
    
    # Sistema é estável se todas as partes reais dos autovalores são negativas
    real_parts = np.real(eigenvalues)
    is_stable = np.all(real_parts <= 0)
    
    return is_stable, eigenvalues, real_parts


if __name__ == "__main__":
    print("Script de correções para o modelo Liu & Nigg 2000")
    print("Este script contém as funções corrigidas para:")
    print("1. Simulação de Euler completa (4 massas)")
    print("2. Função de erro para massa 4")
    print("3. Verificação de estabilidade do sistema")
