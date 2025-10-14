# Correção: Conflito de Variáveis

## 🐛 Erro Reportado

```
'v1_d' was also defined by: cell-7
'v2_d' was also defined by: cell-7
'v3_d' was also defined by: cell-7
'v4_d' was also defined by: cell-7
```

## 🔍 Causa do Problema

As variáveis `v1_d`, `v2_d`, `v3_d`, `v4_d` estavam sendo definidas em **duas células diferentes**:

1. **Célula 1 (Dados Experimentais)**: Calculava velocidades dos dados experimentais
2. **Célula 2 (Conversão)**: Calculava velocidades convertidas para o modelo

Isso causava um conflito de nomes no Marimo, que detecta quando a mesma variável é definida em múltiplas células.

## ✅ Solução Implementada

Renomear as variáveis na **Célula 1** para adicionar o sufixo `_exp`:

### ANTES (❌ Conflito)

```python
# Célula 1: Dados Experimentais
p1_d_exp = heel_d[:,1]/1000
v1_d = np.gradient(p1_d_exp, time_d)  # ❌ Conflito
a1_d = np.gradient(v1_d, time_d)

# Célula 2: Conversão
v1_d = -np.gradient(p1_d_exp, time_d)  # ❌ Conflito
```

### DEPOIS (✅ Sem Conflito)

```python
# Célula 1: Dados Experimentais
p1_d_exp = heel_d[:,1]/1000
v1_d_exp = np.gradient(p1_d_exp, time_d)  # ✅ Único
a1_d_exp = np.gradient(v1_d_exp, time_d)  # ✅ Único

# Célula 2: Conversão
v1_d = -np.gradient(p1_d_exp, time_d)  # ✅ Único
```

## 📋 Variáveis Renomeadas

| Antes | Depois | Descrição |
|-------|--------|-----------|
| `v1_d` | `v1_d_exp` | Velocidade heel experimental |
| `v2_d` | `v2_d_exp` | Velocidade knee experimental |
| `v3_d` | `v3_d_exp` | Velocidade trunk experimental |
| `v4_d` | `v4_d_exp` | Velocidade crest experimental |
| `a1_d` | `a1_d_exp` | Aceleração heel experimental |
| `a2_d` | `a2_d_exp` | Aceleração knee experimental |
| `a3_d` | `a3_d_exp` | Aceleração trunk experimental |
| `a4_d` | `a4_d_exp` | Aceleração crest experimental |

## 🎯 Nomenclatura Final

### Dados Experimentais Originais (Referência: Solo, ↑)
- `p1_d_exp`, `p2_d_exp`, `p3_d_exp`, `p4_d_exp` (posições)
- `v1_d_exp`, `v2_d_exp`, `v3_d_exp`, `v4_d_exp` (velocidades)
- `a1_d_exp`, `a2_d_exp`, `a3_d_exp`, `a4_d_exp` (acelerações)

### Dados Convertidos (Referência: Inicial, ↓)
- `p1_d`, `p2_d`, `p3_d`, `p4_d` (posições convertidas)
- `v1_d`, `v2_d`, `v3_d`, `v4_d` (velocidades convertidas)

### Dados da Simulação (Referência: Inicial, ↓)
- `p1_sim`, `p2_sim`, `p3_sim`, `p4_sim` (posições simuladas)
- `v1_sim`, `v2_sim`, `v3_sim`, `v4_sim` (velocidades simuladas)

## 📝 Mudanças no Código

### Arquivo: `notebooks/analysis_rbds_r09_RNW.py`

**Linhas 152-167** (Célula de dados experimentais):

```python
# Dados experimentais (referência: solo, cresce para cima)
p1_d_exp = heel_d[:,1]/1000                                       #m
v1_d_exp = np.gradient(p1_d_exp, time_d)                          #m/s
a1_d_exp = np.gradient(v1_d_exp, time_d)                          #m

p2_d_exp = knee_d[:,1]/1000                                       #m
v2_d_exp = np.gradient(p2_d_exp, time_d)                          #m/s
a2_d_exp = np.gradient(v2_d_exp, time_d)                          #m/s²

p3_d_exp = trunk_d[:,1]/1000                                      #m
v3_d_exp = np.gradient(p3_d_exp, time_d)                          #m/s
a3_d_exp = np.gradient(v3_d_exp, time_d)                          #m/s²

p4_d_exp = crest_d[:,1]/1000                                      #m
v4_d_exp = np.gradient(p4_d_exp, time_d)                          #m/s
a4_d_exp = np.gradient(v4_d_exp, time_d)                          #m/s²
```

**Linhas 224-227** (Célula de conversão - permanece inalterada):

```python
# Velocidades também precisam ter sinal invertido
v1_d = -np.gradient(p1_d_exp, time_d)
v2_d = -np.gradient(p2_d_exp, time_d)
v3_d = -np.gradient(p3_d_exp, time_d)
v4_d = -np.gradient(p4_d_exp, time_d)
```

## ✅ Verificação

Após a correção:
- ✅ Cada variável é definida em apenas uma célula
- ✅ Nomenclatura consistente com sufixo `_exp` para dados experimentais
- ✅ Nomenclatura sem sufixo para dados convertidos
- ✅ Sem conflitos no Marimo

## 🔗 Documentação Relacionada

- [variaveis_modelo_liu2000.md](variaveis_modelo_liu2000.md): Guia completo de nomenclatura
- [conversao_coordenadas_liu2000.md](conversao_coordenadas_liu2000.md): Documentação da conversão
- [README_conversao_coordenadas.md](README_conversao_coordenadas.md): Resumo executivo

## 💡 Lição Aprendida

**Sempre use sufixos descritivos** para diferenciar variáveis que representam o mesmo conceito físico mas em diferentes convenções ou estágios de processamento:

- `_exp`: Dados experimentais originais
- `_d`: Dados convertidos/processados
- `_sim`: Dados simulados
- `_ref`: Valores de referência
- `_s`: Dados estáticos
- `_otim`: Parâmetros otimizados

Isso evita conflitos e torna o código mais legível e manutenível.

