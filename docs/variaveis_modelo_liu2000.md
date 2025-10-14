# Variáveis do Modelo Liu & Nigg 2000

## 📋 Guia de Nomenclatura

Este documento descreve todas as variáveis usadas na implementação do modelo Liu & Nigg 2000 e suas convenções.

## 🔤 Convenção de Nomenclatura

### Sufixos
- `_s`: Dados **estáticos** (static)
- `_d_exp`: Dados **dinâmicos experimentais** (dynamic experimental)
- `_d`: Dados **dinâmicos convertidos** para convenção do modelo (dynamic)
- `_sim`: Dados da **simulação** (simulation)
- `_ref`: Posições de **referência** (reference)
- `_otim`: Parâmetros **otimizados** (optimized)

### Prefixos
- `p`: Posição (position)
- `v`: Velocidade (velocity)
- `a`: Aceleração (acceleration)
- `k`: Rigidez (stiffness)
- `c`: Amortecimento (damping)
- `m`: Massa (mass)

## 📊 Variáveis por Categoria

### 1. Dados Estáticos (Referência: Solo, Direção: ↑)

Usados para calcular posições de referência e otimizar parâmetros.

| Variável | Descrição | Unidade | Convenção |
|----------|-----------|---------|-----------|
| `p1_s` | Posição heel (estático) | m | Solo, ↑ |
| `p2_s` | Posição knee (estático) | m | Solo, ↑ |
| `p3_s` | Posição trunk (estático) | m | Solo, ↑ |
| `p4_s` | Posição crest (estático) | m | Solo, ↑ |
| `v1_s` | Velocidade heel (estático) | m/s | Solo, ↑ |
| `v2_s` | Velocidade knee (estático) | m/s | Solo, ↑ |
| `v3_s` | Velocidade trunk (estático) | m/s | Solo, ↑ |
| `v4_s` | Velocidade crest (estático) | m/s | Solo, ↑ |
| `a1_s` | Aceleração heel (estático) | m/s² | Solo, ↑ |
| `a2_s` | Aceleração knee (estático) | m/s² | Solo, ↑ |
| `a3_s` | Aceleração trunk (estático) | m/s² | Solo, ↑ |

### 2. Dados Experimentais Dinâmicos (Referência: Solo, Direção: ↑)

Dados originais da captura de movimento durante a corrida.

| Variável | Descrição | Unidade | Convenção |
|----------|-----------|---------|-----------|
| `p1_d_exp` | Posição heel (experimental) | m | Solo, ↑ |
| `p2_d_exp` | Posição knee (experimental) | m | Solo, ↑ |
| `p3_d_exp` | Posição trunk (experimental) | m | Solo, ↑ |
| `p4_d_exp` | Posição crest (experimental) | m | Solo, ↑ |
| `v1_d_exp` | Velocidade heel (experimental) | m/s | Solo, ↑ |
| `v2_d_exp` | Velocidade knee (experimental) | m/s | Solo, ↑ |
| `v3_d_exp` | Velocidade trunk (experimental) | m/s | Solo, ↑ |
| `v4_d_exp` | Velocidade crest (experimental) | m/s | Solo, ↑ |
| `a1_d_exp` | Aceleração heel (experimental) | m/s² | Solo, ↑ |
| `a2_d_exp` | Aceleração knee (experimental) | m/s² | Solo, ↑ |
| `a3_d_exp` | Aceleração trunk (experimental) | m/s² | Solo, ↑ |
| `a4_d_exp` | Aceleração crest (experimental) | m/s² | Solo, ↑ |

### 3. Posições de Referência

Calculadas como média dos dados estáticos.

| Variável | Descrição | Cálculo | Unidade |
|----------|-----------|---------|---------|
| `p1_ref` | Posição inicial heel | `np.mean(p1_s)` | m |
| `p2_ref` | Posição inicial knee | `np.mean(p2_s)` | m |
| `p3_ref` | Posição inicial trunk | `np.mean(p3_s)` | m |
| `p4_ref` | Posição inicial crest | `np.mean(p4_s)` | m |

### 4. Dados Convertidos (Referência: Inicial, Direção: ↓)

Dados experimentais convertidos para a convenção do modelo.

| Variável | Descrição | Cálculo | Unidade | Convenção |
|----------|-----------|---------|---------|-----------|
| `p1_d` | Posição heel (convertido) | `p1_ref - p1_d_exp` | m | Inicial, ↓ |
| `p2_d` | Posição knee (convertido) | `p2_ref - p2_d_exp` | m | Inicial, ↓ |
| `p3_d` | Posição trunk (convertido) | `p3_ref - p3_d_exp` | m | Inicial, ↓ |
| `p4_d` | Posição crest (convertido) | `p4_ref - p4_d_exp` | m | Inicial, ↓ |
| `v1_d` | Velocidade heel (convertido) | `-gradient(p1_d_exp)` | m/s | Inicial, ↓ |
| `v2_d` | Velocidade knee (convertido) | `-gradient(p2_d_exp)` | m/s | Inicial, ↓ |
| `v3_d` | Velocidade trunk (convertido) | `-gradient(p3_d_exp)` | m/s | Inicial, ↓ |
| `v4_d` | Velocidade crest (convertido) | `-gradient(p4_d_exp)` | m/s | Inicial, ↓ |

### 5. Simulação (Referência: Inicial, Direção: ↓)

Resultados da simulação usando método de Euler.

| Variável | Descrição | Condição Inicial | Unidade | Convenção |
|----------|-----------|------------------|---------|-----------|
| `p1_sim` | Posição heel (simulado) | 0.0 | m | Inicial, ↓ |
| `p2_sim` | Posição knee (simulado) | 0.0 | m | Inicial, ↓ |
| `p3_sim` | Posição trunk (simulado) | 0.0 | m | Inicial, ↓ |
| `p4_sim` | Posição crest (simulado) | 0.0 | m | Inicial, ↓ |
| `v1_sim` | Velocidade heel (simulado) | 0.0 | m/s | Inicial, ↓ |
| `v2_sim` | Velocidade knee (simulado) | 0.0 | m/s | Inicial, ↓ |
| `v3_sim` | Velocidade trunk (simulado) | 0.0 | m/s | Inicial, ↓ |
| `v4_sim` | Velocidade crest (simulado) | 0.0 | m/s | Inicial, ↓ |

### 6. Parâmetros do Modelo

Obtidos por otimização usando dados estáticos.

| Variável | Descrição | Unidade | Faixa Típica |
|----------|-----------|---------|--------------|
| `k1_otim` | Rigidez massa 1-3 | N/m | 4000-7000 |
| `k2_otim` | Rigidez massa 1-2 | N/m | 4000-7000 |
| `k3_otim` | Rigidez massa 2-3 | N/m | 8000-12000 |
| `k4_otim` | Rigidez massa 3-4 | N/m | 8000-12000 |
| `k5_otim` | Rigidez adicional 3-4 | N/m | 16000-20000 |
| `c1_otim` | Amortecimento 1-3 | Ns/m | 200-600 |
| `c2_otim` | Amortecimento 1-2 | Ns/m | 550-750 |
| `c4_otim` | Amortecimento 3-4 | Ns/m | 1700-2100 |
| `Fg_otim` | Força solo (otimizada) | N | 0 (fixo) |

### 7. Constantes

| Variável | Descrição | Valor | Unidade |
|----------|-----------|-------|---------|
| `m` | Massa total | 80 | kg |
| `m1` | Massa 1 (pé) | `m * 0.0819` | kg |
| `m2` | Massa 2 (perna) | `m * 0.0799` | kg |
| `m3` | Massa 3 (coxa) | `m * 0.1676` | kg |
| `m4` | Massa 4 (tronco) | `m * 0.6706` | kg |
| `g` | Gravidade | -9.81 | m/s² |
| `dt` | Passo de tempo (estático) | ~0.01 | s |
| `dt_d` | Passo de tempo (dinâmico) | ~0.01 | s |

### 8. Forças

| Variável | Descrição | Unidade | Fonte |
|----------|-----------|---------|-------|
| `MGRF` | Força de reação do solo | N | Plataforma de força |
| `time_Fy` | Tempo da força | s | Plataforma de força |

### 9. Tempo

| Variável | Descrição | Unidade | Fonte |
|----------|-----------|---------|-------|
| `time_1` | Tempo (estático) | s | Dados estáticos |
| `time_d` | Tempo (dinâmico) | s | Dados dinâmicos |

## 🎯 Uso Correto das Variáveis

### Para Otimização
```python
# Usar dados estáticos
minimize(erro_0, [0,6000,6000,300,650], 
         (m1, a1_s, g, p1_s, p3_s, p2_s, v1_s, v2_s, v3_s))
```

### Para Simulação
```python
# Condições iniciais
p1_sim[0] = 0.0  # NÃO usar p1_d[0]
v1_sim[0] = 0.0  # NÃO usar v1_d[0]
```

### Para Comparação
```python
# Usar dados convertidos
plt.plot(time_d, p1_sim, label='Simulação')
plt.plot(time_d, p1_d, label='Experimental')  # p1_d, NÃO p1_d_exp
```

## ⚠️ Erros Comuns

| ❌ Errado | ✅ Correto | Motivo |
|----------|-----------|--------|
| `p1_sim[0] = p1_d[0]` | `p1_sim[0] = 0.0` | Condição inicial deve ser na referência |
| `plt.plot(time_d, p1_d_exp)` | `plt.plot(time_d, p1_d)` | Comparar na mesma convenção |
| `p_ref = p1_d[0]` | `p_ref = np.mean(p1_s)` | Referência vem dos dados estáticos |
| `v1_d = v1_d_exp` | `v1_d = -gradient(p1_d_exp)` | Inverter sinal da velocidade |

## 📝 Notas

1. **Sempre use `_exp` para dados experimentais originais**
2. **Sempre use `_d` (sem `_exp`) para dados convertidos**
3. **Sempre use `_sim` para resultados da simulação**
4. **Sempre use `_ref` para posições de referência**
5. **Sempre use `_s` para dados estáticos**

## 🔗 Ver Também

- [conversao_coordenadas_liu2000.md](conversao_coordenadas_liu2000.md): Documentação da conversão
- [correcao_simulacao_liu2000.md](correcao_simulacao_liu2000.md): Guia de implementação
- [README_conversao_coordenadas.md](README_conversao_coordenadas.md): Resumo executivo

