# Análise das Equações do Modelo Liu & Nigg 2000

## Equações Implementadas no Código

### 1. Massa 1 (Posição 1) - Linha 198
```
m1*a1_s = m1*g - Fg - k1*(p1_s - p3_s) - k2*(p1_s - p2_s) - c1*(v1_s - v3_s) - c2*(v1_s - v2_s)
```

**Implementação na otimização (erro_0):**
```python
m1*a1_s - (m1*g - alfa[0] - alfa[1]*(p1_s - p3_s) - alfa[2]*(p1_s - p2_s) - alfa[3]*(v1_s - v3_s) - alfa[4]*(v1_s - v2_s))
```

**Onde:**
- `alfa[0] = Fg_otim` (força de reação do solo)
- `alfa[1] = k1_otim` (rigidez entre massa 1 e 3)
- `alfa[2] = k2_otim` (rigidez entre massa 1 e 2)
- `alfa[3] = c1_otim` (amortecimento entre massa 1 e 3)
- `alfa[4] = c2_otim` (amortecimento entre massa 1 e 2)

### 2. Massa 2 (Posição 2) - Linha 218
```
m2*a2_s = m2*g + k2*(p1_s - p2_s) - k3*(p2_s - p3_s) + c2*(v1_s - v2_s)
```

**Implementação na otimização (erro_1):**
```python
m2*a2_s - (m2*g + k2_otim*(p1_s - p2_s) - beta[0]*(p2_s - p3_s) + c2_otim*(v1_s - v2_s))
```

**Onde:**
- `beta[0] = k3_otim` (rigidez entre massa 2 e 3)

### 3. Massa 3 (Posição 3) - Linha 229
```
m3*a3_s = m3*g + k1_otim*(p1_s - p3_s) + k3_otim*(p2_s - p3_s) - (k4 + k5)*(p3_s - p4_s) + c1_otim*(v1_s - v3_s) - c4*(v3_s - v4_s)
```

**Implementação na otimização (erro_2):**
```python
m3*a3_s - (m3*g + k1_otim*(p1_s - p3_s) + k3_otim*(p2_s - p3_s) - (gama[0] + gama[1])*(p3_s - p4_s) + c1_otim*(v1_s - v3_s) - gama[2]*(v3_s - v4_s))
```

**Onde:**
- `gama[0] = k4_otim` (rigidez entre massa 3 e 4)
- `gama[1] = k5_otim` (rigidez adicional entre massa 3 e 4)
- `gama[2] = c4_otim` (amortecimento entre massa 3 e 4)

### 4. Massa 4 (Posição 4) - Linha 485 (comentada)
```
m4*a4 = m4*g + (k4 + k5)*(x3 - x4) + c4*(x3 - x4)
```

## Simulação de Euler (Linha 400)

Na simulação dinâmica, apenas a massa 1 é simulada:
```python
dv1dt = (m1 * g - MGRF[_i] - k1_otim * (p1_sim[_i] - p3_sim[_i]) - k2_otim * (p1_sim[_i] - p2_sim[_i]) - c1_otim * (v1_sim[_i] - v3_sim[_i]) - c2_otim * (v1_sim[_i] - v2_sim[_i])) / m1
```

## Análise Crítica

### Problemas Identificados:

1. **Inconsistência na Simulação de Euler:**
   - Apenas a massa 1 é simulada dinamicamente
   - As posições p2_sim, p3_sim, p4_sim são inicializadas como zero e nunca atualizadas
   - Isso significa que a simulação assume que as massas 2, 3 e 4 permanecem estacionárias

2. **Falta de Equações Completas:**
   - A massa 4 não tem equação implementada na otimização
   - O sistema está incompleto

3. **Estrutura do Modelo:**
   - O modelo parece representar um sistema de 4 massas conectadas por molas e amortecedores
   - Massa 1: provavelmente representa o pé/tornozelo
   - Massa 2: provavelmente representa a perna
   - Massa 3: provavelmente representa a coxa
   - Massa 4: provavelmente representa o tronco

### Correções Necessárias:

1. **Completar a Simulação de Euler:**
   - Implementar as equações diferenciais para todas as 4 massas
   - Calcular dv2dt, dv3dt, dv4dt e atualizar todas as posições e velocidades

2. **Implementar Equação da Massa 4:**
   - Adicionar a otimização para os parâmetros da massa 4

3. **Verificar Sinais das Forças:**
   - Confirmar se os sinais das forças estão corretos conforme o modelo Liu2000

## Modelo Típico de Liu & Nigg 2000

Baseado na literatura de biomecânica, o modelo Liu & Nigg 2000 é tipicamente um modelo de 4 massas representando:
- Massa 1: Pé
- Massa 2: Perna (tíbia)
- Massa 3: Coxa (fêmur)
- Massa 4: Tronco

Com conexões:
- k1, c1: entre pé e coxa (representando músculos/tendões)
- k2, c2: entre pé e perna
- k3: entre perna e coxa
- k4, k5, c4: entre coxa e tronco

A força de reação do solo (GRF) atua na massa 1 (pé).

## Recomendações para Correção

### 1. Corrigir a Simulação de Euler

Substituir a simulação atual (que só simula massa 1) por uma simulação completa:

```python
@app.cell
def _(MGRF, c1_otim, c2_otim, c4_otim, g, k1_otim, k2_otim, k3_otim, k4_otim, k5_otim,
      m1, m2, m3, m4, np, p1_d, plt, time_d):
    # Simulação de Euler completa para 4 massas
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

    # Condições iniciais (podem ser ajustadas conforme necessário)
    p1_sim[0] = 0
    p2_sim[0] = 0
    p3_sim[0] = 0
    p4_sim[0] = 0
    v1_sim[0] = 0
    v2_sim[0] = 0
    v3_sim[0] = 0
    v4_sim[0] = 0

    for i in range(n_steps - 1):
        # Massa 1 (pé)
        dv1dt = (m1 * g - MGRF[i] - k1_otim * (p1_sim[i] - p3_sim[i]) -
                 k2_otim * (p1_sim[i] - p2_sim[i]) - c1_otim * (v1_sim[i] - v3_sim[i]) -
                 c2_otim * (v1_sim[i] - v2_sim[i])) / m1

        # Massa 2 (perna)
        dv2dt = (m2 * g + k2_otim * (p1_sim[i] - p2_sim[i]) -
                 k3_otim * (p2_sim[i] - p3_sim[i]) + c2_otim * (v1_sim[i] - v2_sim[i])) / m2

        # Massa 3 (coxa)
        dv3dt = (m3 * g + k1_otim * (p1_sim[i] - p3_sim[i]) +
                 k3_otim * (p2_sim[i] - p3_sim[i]) - (k4_otim + k5_otim) * (p3_sim[i] - p4_sim[i]) +
                 c1_otim * (v1_sim[i] - v3_sim[i]) - c4_otim * (v3_sim[i] - v4_sim[i])) / m3

        # Massa 4 (tronco)
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

    # Plotar resultados
    plt.figure(figsize=(15, 10))

    plt.subplot(2, 2, 1)
    plt.plot(time_d, p1_sim, 'b-', linewidth=0.8, label='Simulação p1')
    plt.plot(time_d, p1_d, 'orange', linewidth=0.8, label='Experimental p1')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Posição (m)')
    plt.title('Massa 1 (Pé)')
    plt.legend()
    plt.grid(True)

    plt.subplot(2, 2, 2)
    plt.plot(time_d, p2_sim, 'g-', linewidth=0.8, label='Simulação p2')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Posição (m)')
    plt.title('Massa 2 (Perna)')
    plt.legend()
    plt.grid(True)

    plt.subplot(2, 2, 3)
    plt.plot(time_d, p3_sim, 'r-', linewidth=0.8, label='Simulação p3')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Posição (m)')
    plt.title('Massa 3 (Coxa)')
    plt.legend()
    plt.grid(True)

    plt.subplot(2, 2, 4)
    plt.plot(time_d, p4_sim, 'm-', linewidth=0.8, label='Simulação p4')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Posição (m)')
    plt.title('Massa 4 (Tronco)')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()

    return p1_sim, p2_sim, p3_sim, p4_sim, v1_sim, v2_sim, v3_sim, v4_sim
```

### 2. Adicionar Verificação de Estabilidade

É recomendável adicionar uma célula para verificar a estabilidade do sistema:

```python
@app.cell
def _(c1_otim, c2_otim, c4_otim, k1_otim, k2_otim, k3_otim, k4_otim, k5_otim,
      m1, m2, m3, m4, np):
    # Verificação de estabilidade do sistema
    # Matriz de massa
    M = np.diag([m1, m2, m3, m4])

    # Matriz de rigidez
    K = np.array([
        [k1_otim + k2_otim, -k2_otim, -k1_otim, 0],
        [-k2_otim, k2_otim + k3_otim, -k3_otim, 0],
        [-k1_otim, -k3_otim, k1_otim + k3_otim + k4_otim + k5_otim, -(k4_otim + k5_otim)],
        [0, 0, -(k4_otim + k5_otim), k4_otim + k5_otim]
    ])

    # Matriz de amortecimento
    C = np.array([
        [c1_otim + c2_otim, -c2_otim, -c1_otim, 0],
        [-c2_otim, c2_otim, 0, 0],
        [-c1_otim, 0, c1_otim + c4_otim, -c4_otim],
        [0, 0, -c4_otim, c4_otim]
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
    real_parts = np.real(eigenvalues)
    is_stable = np.all(real_parts <= 0)

    print("=== ANÁLISE DE ESTABILIDADE ===")
    print(f"Sistema estável: {is_stable}")
    print(f"Autovalores: {eigenvalues}")
    print(f"Partes reais: {real_parts}")

    if not is_stable:
        print("⚠️  ATENÇÃO: Sistema instável! Verifique os parâmetros.")
    else:
        print("✅ Sistema estável.")

    return A, eigenvalues, is_stable
```

## Conclusão

O código atual implementa parcialmente o modelo Liu & Nigg 2000, mas tem limitações importantes:

1. **Simulação incompleta**: Apenas a massa 1 é simulada dinamicamente
2. **Falta de validação**: Não há comparação com dados experimentais para as massas 2, 3 e 4
3. **Ausência de verificação de estabilidade**: Importante para garantir que o modelo é fisicamente válido

As correções sugeridas tornarão o modelo mais completo e fisicamente consistente com o artigo original.
