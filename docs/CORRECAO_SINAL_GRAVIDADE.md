# Correção: Sinal da Gravidade no Sistema de Coordenadas do Modelo

## 🎯 Problema Identificado

### Observação do Usuário
> "The gravity acceleration is defined with a minus signal. However the model coordinate system increases in the direction of the soil. Analyse where it should be changed and correct it."

**O usuário está 100% correto!**

## 📐 Análise do Sistema de Coordenadas

### Sistema de Coordenadas do Modelo Liu & Nigg 2000

```
        ↑ Negativo (afastando do solo)
        |
        |
    ────┼──── Referência (posição inicial dos dados estáticos)
        |
        |
        ↓ Positivo (em direção ao solo)
```

**Convenção:**
- **Positivo (+)** = movimento para BAIXO (em direção ao solo)
- **Negativo (-)** = movimento para CIMA (afastando do solo)

### Direção da Gravidade

A gravidade atua **para BAIXO** (em direção ao solo).

No sistema de coordenadas do modelo:
- Para BAIXO = **POSITIVO**
- Portanto: **g deve ser POSITIVO**

## ❌ Implementação Anterior (INCORRETA)

### Definição Anterior

```python
# ❌ ERRADO
g = -9.81  # m/s² (aceleração da gravidade)
```

### Por que estava errado?

1. **Inconsistência com o sistema de coordenadas**: 
   - Modelo: positivo = para baixo
   - Gravidade: atua para baixo
   - Portanto: g deveria ser positivo

2. **Compensação incorreta**:
   - O código anterior usava `abs(g)` em alguns lugares
   - Isso mascara o problema mas não o resolve

3. **Confusão com convenção padrão**:
   - Em física, geralmente g = -9.81 m/s² (com Y para cima)
   - Mas aqui o sistema é invertido!

## ✅ Implementação Correta

### Definição Correta

```python
# ✅ CORRETO
# IMPORTANTE: No sistema de coordenadas do modelo, positivo = para BAIXO
# Portanto, g deve ser POSITIVO (gravidade atua na direção positiva)
g = 9.81  # m/s² (aceleração da gravidade - POSITIVA no sistema do modelo)
```

### Cálculo do Peso

**ANTES:**
```python
peso_corpo = m * abs(g)  # ❌ Precisava de abs() para compensar
```

**DEPOIS:**
```python
peso_corpo = m * g  # ✅ g já é positivo
```

## 🔍 Análise das Equações

### Equação da Massa 1 (Pé)

```
m1·a1 = m1·g - MGRF - k1·(p1-p3) - k2·(p1-p2) - c1·(v1-v3) - c2·(v1-v2)
```

**Análise das forças:**

1. **m1·g** (peso):
   - Atua para BAIXO
   - No sistema do modelo: para baixo = POSITIVO
   - Portanto: **+m1·g** ✅

2. **-MGRF** (reação do solo):
   - Atua para CIMA (oposta ao peso)
   - No sistema do modelo: para cima = NEGATIVO
   - MGRF é positivo nos dados (convenção da plataforma)
   - Portanto: **-MGRF** ✅

3. **Forças das molas e amortecedores**:
   - Dependem das posições/velocidades relativas
   - Sinais corretos conforme modelo Liu 2000

### Equações das Outras Massas

**Massa 2, 3, 4:**
```
m2·a2 = m2·g + ...
m3·a3 = m3·g + ...
m4·a4 = m4·g + ...
```

Todas têm **+m·g** porque a gravidade atua para baixo (positivo).

## 🔧 Mudanças no Código

### 1. Definição de g (Linha 432)

**ANTES:**
```python
g = -9.81  # m/s² (aceleração da gravidade)
```

**DEPOIS:**
```python
# IMPORTANTE: No sistema de coordenadas do modelo, positivo = para BAIXO
# Portanto, g deve ser POSITIVO (gravidade atua na direção positiva)
g = 9.81  # m/s² (aceleração da gravidade - POSITIVA no sistema do modelo)
```

### 2. Cálculo do Peso (Linha 442)

**ANTES:**
```python
peso_corpo = m * abs(g)  # N (força peso total)
```

**DEPOIS:**
```python
peso_corpo = m * g  # N (força peso total - g já é positivo)
```

### 3. Equações de Simulação (Linhas 781-806)

**Adicionados comentários explicativos:**
```python
# IMPORTANTE: g é POSITIVO (para baixo), MGRF é NEGATIVO (para cima)
dv1dt = float((m1 * g - MGRF[i] - k1_otim * (p1_sim[i] - p3_sim[i]) - ...
```

### 4. Documentação Atualizada (Linhas 374-434)

Adicionada seção explicando a convenção de sinais:

```markdown
### ⚠️ IMPORTANTE: Convenção de Sinais

**Sistema de Coordenadas do Modelo:**
- **Positivo = para BAIXO** (em direção ao solo)
- **Negativo = para CIMA** (afastando do solo)

**Forças:**
- **g = +9.81 m/s²** (gravidade atua para BAIXO = direção positiva)
- **MGRF**: força para CIMA, mas valor positivo nos dados
  - Na equação: `-MGRF` (sinal negativo porque atua para cima)
```

## 📊 Diagrama de Forças

### Massa 1 (Pé) em Contato com o Solo

```
        ↑ -MGRF (reação do solo, para cima)
        |
    ┌───┴───┐
    │  m1   │  Massa 1 (pé)
    └───┬───┘
        |
        ↓ +m1·g (peso, para baixo)
        
        ↓ Positivo (direção do solo)
```

**Equação:**
```
m1·a1 = (+m1·g) + (-MGRF) + (forças das molas/amortecedores)
       = m1·g - MGRF - k1·(p1-p3) - k2·(p1-p2) - ...
```

## ✅ Validação

### Como Verificar se Está Correto

1. **Valores de g**:
   ```python
   g = 9.81  # ✅ Positivo
   ```

2. **Peso do corpo**:
   ```python
   peso_corpo = m * g = 80 * 9.81 = 784.8 N  # ✅ Positivo
   ```

3. **Durante simulação em repouso** (sem movimento):
   - Aceleração deveria ser zero: `a = g - MGRF/m = 0`
   - Portanto: `MGRF = m·g` ✅
   - Com g positivo e MGRF positivo, isso funciona!

4. **Durante queda livre** (sem MGRF):
   - Aceleração deveria ser g: `a = g` ✅
   - Massa acelera para baixo (positivo) ✅

## 🎓 Comparação com Convenção Padrão

### Convenção Padrão de Física (Y para cima)

```
    ↑ Y (positivo para cima)
    |
    |
────┴──── Solo
```

- g = -9.81 m/s² (negativo porque atua para baixo)
- MGRF = +valor (positivo porque atua para cima)

### Convenção do Modelo Liu 2000 (Y para baixo)

```
────┬──── Referência
    |
    ↓ Y (positivo para baixo)
```

- g = +9.81 m/s² (positivo porque atua para baixo)
- MGRF na equação: -MGRF (negativo porque atua para cima)

## 📚 Referências

1. **Liu, W., & Nigg, B. M. (2000).** A mechanical model to determine the influence of masses and mass distribution on the impact force during running.
   - Define o sistema de coordenadas do modelo
   - Positivo = compressão (para baixo)

2. **Fukuchi, R. K., et al. (2017).** A public dataset of running biomechanics.
   - Dados experimentais com Y = vertical
   - Fy = força vertical (positiva para cima na plataforma)

## 🎯 Lição Aprendida

**Sempre verifique a convenção de sinais do sistema de coordenadas!**

Quando o sistema de coordenadas é invertido (positivo para baixo):
1. ✅ Gravidade deve ser POSITIVA
2. ✅ Forças para cima devem ter sinal NEGATIVO nas equações
3. ✅ Documentar claramente a convenção
4. ❌ Não usar `abs()` para "corrigir" sinais - isso mascara o problema

---

**Data da Correção:** 2025-10-11  
**Autor:** Augment Agent  
**Motivo:** Correção baseada no feedback do usuário sobre convenção de sinais

