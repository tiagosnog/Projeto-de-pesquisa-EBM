# Correção: MGRF na Otimização com Dados Estáticos

## 🎯 Problema Identificado

### Observação do Usuário
> "Tenho a impressão que durante a otimização, o peso do sujeito não está sendo considerado? Isso é verdade? As equações durante a otimização estão certas? Se preciso do peso, multiplicar a massa pelo g para aproximar MGRF durante a otimização que usa dados estáticos."

**Resposta: CORRETO! Excelente observação!**

## 🔍 Análise do Problema

### ANTES da Correção (❌ ERRADO)

**Equação de Otimização (Massa 1):**
```python
def erro_0 (alfa, m1, a1_s, g, p1_s, p3_s, p2_s, v1_s, v2_s, v3_s):
    return np.sum((m1*a1_s - (m1*g - alfa[0] - alfa[1]*(p1_s - p3_s) - ...))**2)
```

Onde:
- `alfa[0] = Fg_otim` (força de reação do solo otimizada)
- Bounds: `(0, 0)` → Fg_otim sempre = 0

**Problema:**
- Durante dados **estáticos**, o sujeito está parado
- MGRF deveria ser ≈ **peso do corpo** (m × |g| ≈ 785 N)
- Mas estava sendo otimizado como 0 N ❌

### Contexto Físico

**Durante Dados ESTÁTICOS:**
- Sujeito está parado (ou quase parado)
- Acelerações ≈ 0
- Velocidades ≈ 0
- **MGRF ≈ Peso do corpo** (constante)

```
MGRF_estático = m_total × |g|
MGRF_estático = 80 kg × 9.81 m/s²
MGRF_estático ≈ 785 N
```

**Durante Dados DINÂMICOS (Corrida):**
- Sujeito está em movimento
- Acelerações variam
- Velocidades variam
- **MGRF varia com o tempo** (medido pela plataforma de força)
- Durante impacto: MGRF pode chegar a 2-3× o peso do corpo

## ✅ Solução Implementada

### DEPOIS da Correção (✅ CORRETO)

#### 1. Adicionar Cálculo do Peso do Corpo

```python
@app.cell
def _(time_1):
    m = 80              # kg (massa total do indivíduo)
    g = -9.81           # m/s² (aceleração da gravidade)
    
    # IMPORTANTE: Durante dados estáticos, MGRF ≈ peso do corpo
    peso_corpo = m * abs(g)  # N (força peso total)
    
    print(f"Peso do corpo: {peso_corpo:.2f} N")
    
    return dt, g, m, m1, m2, m3, m4, peso_corpo
```

#### 2. Corrigir Equação de Otimização

**ANTES:**
```python
def erro_0 (alfa, m1, a1_s, g, p1_s, p3_s, p2_s, v1_s, v2_s, v3_s):
    return np.sum((m1*a1_s - (m1*g - alfa[0] - alfa[1]*(p1_s - p3_s) - ...))**2)
    #                              ^^^^^^^ Fg_otim (sempre 0)

alfa = minimize(erro_0, [0,6000,6000,300,650], ..., 
                bounds=[(0,0), ...])  # Fg fixo em 0
```

**DEPOIS:**
```python
def erro_0 (alfa, m1, a1_s, g, peso_corpo, p1_s, p3_s, p2_s, v1_s, v2_s, v3_s):
    return np.sum((m1*a1_s - (m1*g - peso_corpo - alfa[0]*(p1_s - p3_s) - ...))**2)
    #                              ^^^^^^^^^^^ Peso do corpo (~785 N)

alfa = minimize(erro_0, [6000,6000,300,650], ..., 
                bounds=[(4000,7000), ...])  # Sem Fg na otimização
```

**Mudanças:**
- ✅ Adicionado `peso_corpo` como parâmetro
- ✅ Substituído `alfa[0]` (Fg_otim) por `peso_corpo`
- ✅ Removido Fg da otimização (agora `alfa` tem 4 elementos ao invés de 5)
- ✅ `Fg_otim = 0.0` (fixo, não usado na simulação dinâmica)

#### 3. Simulação Permanece Inalterada (✅ JÁ ESTAVA CORRETO)

```python
# Equação para massa 1 (pé) - SIMULAÇÃO DINÂMICA
dv1dt = float((m1 * g + 1.04*MGRF[i] - k1_otim * (p1_sim[i] - p3_sim[i]) - ...
#                       ^^^^^^^^^^^^ MGRF[i] varia com o tempo (correto!)
```

**Nota:** O fator `1.04` é um ajuste de calibração.

## 📊 Comparação: Estático vs Dinâmico

| Aspecto | Dados Estáticos (Otimização) | Dados Dinâmicos (Simulação) |
|---------|------------------------------|------------------------------|
| **Movimento** | Parado | Corrida |
| **Acelerações** | ≈ 0 | Variáveis |
| **Velocidades** | ≈ 0 | Variáveis |
| **MGRF** | `peso_corpo` ≈ 785 N (constante) | `MGRF[i]` (variável no tempo) |
| **MGRF máximo** | ~785 N | 2-3× peso (~1500-2400 N) |
| **Equação** | `m1*g - peso_corpo - k1*...` | `m1*g + MGRF[i] - k1*...` |

## 🔧 Mudanças no Código

### Arquivo: `notebooks/analysis_rbds_r09_RNW.py`

#### 1. Parâmetros (Linhas 357-381)

**Adicionado:**
```python
# IMPORTANTE: Durante dados estáticos, MGRF ≈ peso do corpo
peso_corpo = m * abs(g)  # N (força peso total)

print(f"=== PARÂMETROS DO MODELO ===")
print(f"Massa total: {m} kg")
print(f"Peso do corpo: {peso_corpo:.2f} N")
```

#### 2. Documentação (Linhas 351-395)

**Adicionado:**
```markdown
### ⚠️ IMPORTANTE: Força de Reação do Solo (MGRF)

**Durante Dados ESTÁTICOS:**
- O sujeito está parado (ou quase parado)
- MGRF ≈ Peso do corpo = m_total × |g| ≈ 80 × 9.81 ≈ 785 N
- **Não otimizamos Fg**, usamos o peso do corpo diretamente

**Durante Dados DINÂMICOS (Simulação):**
- MGRF varia com o tempo (medido pela plataforma de força)
- MGRF pode chegar a 2-3× o peso do corpo durante o impacto
- Usamos os dados medidos da plataforma de força
```

#### 3. Otimização Massa 1 (Linhas 396-433)

**ANTES:**
```python
# alfa[0] = Fg_otm  [N]
# alfa[1] = k1_otim [N/m]
# alfa[2] = k2_otim [N/m]
# alfa[3] = c1_otim [Ns/m]
# alfa[4] = c2_otim [Ns/m]

def erro_0 (alfa, m1, a1_s, g, p1_s, p3_s, p2_s, v1_s, v2_s, v3_s):
    return np.sum((m1*a1_s - (m1*g - alfa[0] - alfa[1]*(p1_s - p3_s) - ...))**2)

alfa = minimize(erro_0, [0,6000,6000,300,650], ..., 
                bounds=[(0,0),(4000,7000),(4000,7000),(200,600),(550,750)])

Fg_otim = alfa[0]
k1_otim = alfa[1]
k2_otim = alfa[2]
c1_otim = alfa[3]
c2_otim = alfa[4]
```

**DEPOIS:**
```python
# alfa[0] = k1_otim [N/m]
# alfa[1] = k2_otim [N/m]
# alfa[2] = c1_otim [Ns/m]
# alfa[3] = c2_otim [Ns/m]

def erro_0 (alfa, m1, a1_s, g, peso_corpo, p1_s, p3_s, p2_s, v1_s, v2_s, v3_s):
    # Usar peso_corpo ao invés de Fg otimizado
    return np.sum((m1*a1_s - (m1*g - peso_corpo - alfa[0]*(p1_s - p3_s) - ...))**2)

alfa = minimize(erro_0, [6000,6000,300,650], ..., 
                bounds=[(4000,7000),(4000,7000),(200,600),(550,750)])

k1_otim = alfa[0]
k2_otim = alfa[1]
c1_otim = alfa[2]
c2_otim = alfa[3]

# Fg_otim não é mais otimizado, é fixo = 0
Fg_otim = 0.0
```

## ✅ Validação

### Como Verificar se a Correção Está Correta

1. **Execute a célula de parâmetros** e verifique:
   ```
   Peso do corpo: 784.80 N
   ```

2. **Execute a otimização** e verifique que os parâmetros são razoáveis:
   ```
   k1_otim ≈ 4000-7000 N/m
   k2_otim ≈ 4000-7000 N/m
   c1_otim ≈ 200-600 Ns/m
   c2_otim ≈ 550-750 Ns/m
   ```

3. **Execute a simulação** e verifique que os resultados fazem sentido físico

## 📐 Equações Finais

### Otimização (Dados Estáticos)

**Massa 1:**
```
m1·a1_s = m1·g - peso_corpo - k1·(p1_s - p3_s) - k2·(p1_s - p2_s) - c1·(v1_s - v3_s) - c2·(v1_s - v2_s)
```

**Massa 2:**
```
m2·a2_s = m2·g + k2·(p1_s - p2_s) - k3·(p2_s - p3_s) + c2·(v1_s - v2_s)
```

**Massa 3:**
```
m3·a3_s = m3·g + k1·(p1_s - p3_s) + k3·(p2_s - p3_s) - (k4+k5)·(p3_s - p4_s) + c1·(v1_s - v3_s) - c4·(v3_s - v4_s)
```

### Simulação (Dados Dinâmicos)

**Massa 1:**
```
m1·a1 = m1·g + MGRF[i] - k1·(p1 - p3) - k2·(p1 - p2) - c1·(v1 - v3) - c2·(v1 - v2)
```

**Massa 2, 3, 4:** (sem mudanças)

## 💡 Lição Aprendida

**Sempre considere o contexto físico ao configurar otimizações:**

1. **Dados estáticos** → MGRF ≈ peso do corpo (constante)
2. **Dados dinâmicos** → MGRF varia com o tempo (medido)
3. **Não otimize parâmetros que podem ser calculados diretamente**

## 📚 Referências

- Liu, W., & Nigg, B. M. (2000). A mechanical model to determine the influence of masses and mass distribution on the impact force during running. *Journal of Biomechanics*, 33(2), 219-224.

## 🔗 Documentação Relacionada

- [conversao_coordenadas_liu2000.md](conversao_coordenadas_liu2000.md): Conversão de coordenadas
- [CORRECAO_EIXO_COORDENADAS.md](CORRECAO_EIXO_COORDENADAS.md): Correção de eixos
- [variaveis_modelo_liu2000.md](variaveis_modelo_liu2000.md): Guia de nomenclatura

