# Correção: Inconsistência de Eixos nas Coordenadas

## 🐛 Problema Identificado

### Pergunta do Usuário
> "Como a posição inicial do p1 experimental está sendo calculado após a conversão?"

### Análise Revelou Inconsistência Crítica

Os dados **estáticos** e **dinâmicos** estavam usando **eixos diferentes**:

#### ANTES da Correção (❌ ERRADO):

**Dados Estáticos:**
```python
p1_s = trunk_mm[:, 2] / 1000  # ❌ Eixo Z (vertical)
p2_s = knee[:, 1] / 1000      # ✓ Eixo Y (anteroposterior)
p3_s = trunk_mm[:, 1] / 1000  # ✓ Eixo Y (anteroposterior)
p4_s = crest_s[:, 1] / 1000   # ✓ Eixo Y (anteroposterior)
```

**Dados Dinâmicos:**
```python
p1_d_exp = heel_d[:, 1] / 1000   # ✓ Eixo Y (anteroposterior)
p2_d_exp = knee_d[:, 1] / 1000   # ✓ Eixo Y (anteroposterior)
p3_d_exp = trunk_d[:, 1] / 1000  # ✓ Eixo Y (anteroposterior)
p4_d_exp = crest_d[:, 1] / 1000  # ✓ Eixo Y (anteroposterior)
```

### Consequência do Erro

Na conversão:
```python
p1_ref = np.mean(p1_s)        # Média do eixo Z (vertical)
p1_d = p1_ref - p1_d_exp      # ❌ Subtraindo Z - Y (sem sentido!)
```

**Isso estava subtraindo coordenadas de eixos diferentes!**

## ✅ Solução Implementada

### DEPOIS da Correção (✅ CORRETO):

**Dados Estáticos:**
```python
heel_s = data_static[['R.Heel.TopX','R.Heel.TopY','R.Heel.TopZ']].values
p1_s = heel_s[:, 1] / 1000    # ✓ Eixo Y (anteroposterior)
p2_s = knee[:, 1] / 1000      # ✓ Eixo Y (anteroposterior)
p3_s = trunk_mm[:, 1] / 1000  # ✓ Eixo Y (anteroposterior)
p4_s = crest_s[:, 1] / 1000   # ✓ Eixo Y (anteroposterior)
```

**Dados Dinâmicos (sem mudança):**
```python
p1_d_exp = heel_d[:, 1] / 1000   # ✓ Eixo Y (anteroposterior)
p2_d_exp = knee_d[:, 1] / 1000   # ✓ Eixo Y (anteroposterior)
p3_d_exp = trunk_d[:, 1] / 1000  # ✓ Eixo Y (anteroposterior)
p4_d_exp = crest_d[:, 1] / 1000  # ✓ Eixo Y (anteroposterior)
```

**Agora a conversão faz sentido:**
```python
p1_ref = np.mean(p1_s)        # Média do eixo Y (anteroposterior)
p1_d = p1_ref - p1_d_exp      # ✓ Subtraindo Y - Y (correto!)
```

## 📐 Sistema de Coordenadas

### Convenção dos Dados de Captura de Movimento

```
        Z (vertical)
        ↑
        |
        |
        |________→ Y (anteroposterior - direção do movimento)
       /
      /
     ↙
    X (médio-lateral)
```

### Índices nos Arrays NumPy

| Índice | Eixo | Direção | Uso no Modelo Liu 2000 |
|--------|------|---------|------------------------|
| 0 | X | Médio-lateral | ❌ Não usado |
| 1 | Y | Anteroposterior | ✅ **USADO** |
| 2 | Z | Vertical | ❌ Não usado |

### Por que Eixo Y?

O modelo Liu & Nigg 2000 analisa o movimento na **direção anteroposterior** (Y), que é:
- A direção principal do movimento durante a corrida
- A direção onde ocorre o impacto e a propulsão
- A direção relevante para o modelo de 4 massas em série

## 🔧 Mudanças no Código

### Arquivo: `notebooks/analysis_rbds_r09_RNW.py`

#### 1. Adicionada Documentação (Linhas 20-40)

```python
@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Estáticos
    
    ### ⚠️ IMPORTANTE: Convenção de Eixos
    
    Para o modelo Liu & Nigg 2000 de corrida, usamos o **eixo Y** (índice 1) para todas as massas:
    
    - **Eixo X** (índice 0): Médio-lateral (lado a lado)
    - **Eixo Y** (índice 1): Anteroposterior (direção do movimento) ← **USADO**
    - **Eixo Z** (índice 2): Vertical (para cima/baixo)
    
    **Razão**: O modelo Liu 2000 analisa o movimento na direção anteroposterior (Y),
    que é a direção principal do movimento durante a corrida.
    
    Todos os dados (estáticos e dinâmicos) devem usar o **mesmo eixo** para consistência.
    """
    )
    return
```

#### 2. Corrigido Cálculo de p1_s (Linhas 41-68)

**ANTES:**
```python
p1_s = trunk_mm[:, 2] / 1000  # ❌ Eixo Z
```

**DEPOIS:**
```python
# Calcular heel estático (mesma forma que nos dados dinâmicos)
heel_s = data_static[['R.Heel.TopX','R.Heel.TopY','R.Heel.TopZ']].values

# IMPORTANTE: Usar eixo Y (índice 1) para consistência com dados dinâmicos
# Eixo Y = direção anteroposterior (direção do movimento na corrida)
p1_s = heel_s[:, 1] / 1000  # ✓ Eixo Y do heel
```

#### 3. Adicionados Comentários nos Dados Dinâmicos (Linhas 177-194)

```python
# Dados experimentais (referência: solo, cresce para cima)
# IMPORTANTE: Usando eixo Y (índice 1) - direção anteroposterior
# Mesma convenção dos dados estáticos para consistência
p1_d_exp = heel_d[:,1]/1000  # m (eixo Y)
p2_d_exp = knee_d[:,1]/1000  # m (eixo Y)
p3_d_exp = trunk_d[:,1]/1000  # m (eixo Y)
p4_d_exp = crest_d[:,1]/1000  # m (eixo Y)
```

#### 4. Adicionada Verificação na Conversão (Linhas 242-263)

```python
print("=== POSIÇÕES DE REFERÊNCIA (dados estáticos - eixo Y) ===")
print(f"p1_ref (heel):  {p1_ref:.4f} m")
print(f"p2_ref (knee):  {p2_ref:.4f} m")
print(f"p3_ref (trunk): {p3_ref:.4f} m")
print(f"p4_ref (crest): {p4_ref:.4f} m")

# Verificar valores iniciais dos dados experimentais
print("\n=== VALORES INICIAIS (dados experimentais - eixo Y) ===")
print(f"p1_d_exp[0] (heel):  {p1_d_exp[0]:.4f} m")
print(f"p2_d_exp[0] (knee):  {p2_d_exp[0]:.4f} m")
print(f"p3_d_exp[0] (trunk): {p3_d_exp[0]:.4f} m")
print(f"p4_d_exp[0] (crest): {p4_d_exp[0]:.4f} m")
```

## ✅ Validação

### Como Verificar se a Correção Está Correta

1. **Execute a célula de conversão** e verifique os prints:
   - Os valores de `p1_ref`, `p2_ref`, `p3_ref`, `p4_ref` devem estar na mesma ordem de grandeza
   - Os valores de `p1_d_exp[0]`, `p2_d_exp[0]`, etc. devem ser próximos aos valores de referência

2. **Verifique a conversão**:
   ```python
   p1_d[0] = p1_ref - p1_d_exp[0]
   ```
   - Se `p1_d_exp[0] ≈ p1_ref`, então `p1_d[0] ≈ 0` ✓
   - Isso faz sentido: no início, a massa está próxima à posição de referência

3. **Verifique os gráficos**:
   - Os dados convertidos devem oscilar em torno de y=0
   - Durante o impacto, valores devem ser positivos (massa desce)
   - Durante o voo, valores devem ser negativos (massa sobe)

## 📊 Exemplo Numérico

### Valores Esperados (Eixo Y - Anteroposterior)

```
Dados Estáticos (referência):
p1_ref (heel):  ≈ 0.5 m
p2_ref (knee):  ≈ 0.5 m
p3_ref (trunk): ≈ 0.5 m
p4_ref (crest): ≈ 0.5 m

Dados Dinâmicos (início):
p1_d_exp[0] (heel):  ≈ 0.5 m
p2_d_exp[0] (knee):  ≈ 0.5 m
p3_d_exp[0] (trunk): ≈ 0.5 m
p4_d_exp[0] (crest): ≈ 0.5 m

Dados Convertidos (início):
p1_d[0] = 0.5 - 0.5 ≈ 0.0 m ✓
p2_d[0] = 0.5 - 0.5 ≈ 0.0 m ✓
p3_d[0] = 0.5 - 0.5 ≈ 0.0 m ✓
p4_d[0] = 0.5 - 0.5 ≈ 0.0 m ✓
```

## 🎯 Resposta à Pergunta Original

> "Como a posição inicial do p1 experimental está sendo calculado após a conversão?"

**Resposta:**

Após a correção, a posição inicial de `p1_d` (convertido) é calculada assim:

```python
# 1. Calcular posição de referência (média dos dados estáticos - eixo Y)
p1_ref = np.mean(p1_s)  # p1_s = heel_s[:, 1] (eixo Y)

# 2. Converter dados experimentais (eixo Y)
p1_d = p1_ref - p1_d_exp  # Ambos no eixo Y!

# 3. Posição inicial convertida
p1_d[0] = p1_ref - p1_d_exp[0]
```

**Agora faz sentido fisicamente:**
- Se `p1_d_exp[0]` está próximo de `p1_ref` → `p1_d[0] ≈ 0` (na posição de referência)
- Se `p1_d_exp[0]` está abaixo de `p1_ref` → `p1_d[0] > 0` (massa desceu)
- Se `p1_d_exp[0]` está acima de `p1_ref` → `p1_d[0] < 0` (massa subiu)

## 📚 Documentação Relacionada

- [conversao_coordenadas_liu2000.md](conversao_coordenadas_liu2000.md): Documentação da conversão
- [variaveis_modelo_liu2000.md](variaveis_modelo_liu2000.md): Guia de nomenclatura
- [CORRECAO_CONFLITO_VARIAVEIS.md](CORRECAO_CONFLITO_VARIAVEIS.md): Correção anterior

## 💡 Lição Aprendida

**Sempre verifique que dados estáticos e dinâmicos usam o mesmo eixo de coordenadas!**

Ao trabalhar com dados de captura de movimento 3D:
1. Identifique qual eixo é relevante para o modelo
2. Use o **mesmo eixo** em todos os dados (estáticos e dinâmicos)
3. Documente claramente qual eixo está sendo usado
4. Adicione verificações para validar a consistência

