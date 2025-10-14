# Correção: Condições Iniciais da Simulação

## 🎯 Problema Identificado

### Observação do Usuário
> "The initial conditions of the simulations should be the values of the position of the experimental data (converted to the coordinate system of the model and considering the 0 of each variable the value obtained with the static data)"

**O usuário está 100% correto!**

## ❌ Implementação Anterior (INCORRETA)

### Condições Iniciais Anteriores

```python
# ❌ ERRADO: Sempre iniciava em p=0, v=0
p1_sim[0] = 0.0  # posição inicial na referência
p2_sim[0] = 0.0
p3_sim[0] = 0.0
p4_sim[0] = 0.0
v1_sim[0] = 0.0  # velocidade inicial zero
v2_sim[0] = 0.0
v3_sim[0] = 0.0
v4_sim[0] = 0.0
```

### Por que estava errado?

1. **Ignora o estado inicial real**: Os dados experimentais não começam necessariamente em p=0, v=0
2. **Inconsistência com dados reais**: A simulação começa em um estado diferente dos dados experimentais
3. **Comparação injusta**: Compara simulação (começando em repouso) com dados (começando em movimento)

## ✅ Implementação Correta

### Condições Iniciais Corretas

```python
# ✅ CORRETO: Usa valores iniciais dos dados experimentais convertidos
p1_sim[0] = p1_d[0]  # posição inicial do heel (dados experimentais convertidos)
p2_sim[0] = p2_d[0]  # posição inicial do knee (dados experimentais convertidos)
p3_sim[0] = p3_d[0]  # posição inicial do trunk (dados experimentais convertidos)
p4_sim[0] = p4_d[0]  # posição inicial do crest (dados experimentais convertidos)
v1_sim[0] = v1_d[0]  # velocidade inicial do heel (dados experimentais convertidos)
v2_sim[0] = v2_d[0]  # velocidade inicial do knee (dados experimentais convertidos)
v3_sim[0] = v3_d[0]  # velocidade inicial do trunk (dados experimentais convertidos)
v4_sim[0] = v4_d[0]  # velocidade inicial do crest (dados experimentais convertidos)
```

### Por que está correto?

1. **Usa o estado inicial real**: Começa exatamente onde os dados experimentais começam
2. **Consistência**: Simulação e dados experimentais começam no mesmo estado
3. **Comparação justa**: Ambos evoluem a partir do mesmo ponto inicial

## 📊 Fluxo de Dados Correto

### Passo a Passo

```
1. Dados Estáticos
   ↓
   Calcular posições de referência (p_ref)
   
2. Dados Experimentais Dinâmicos
   ↓
   Converter para convenção do modelo:
   - p_d = p_ref - p_exp (posição relativa)
   - v_d = -v_exp (velocidade invertida)
   
3. Condições Iniciais da Simulação
   ↓
   Usar valores iniciais dos dados convertidos:
   - p_sim[0] = p_d[0]
   - v_sim[0] = v_d[0]
   
4. Simulação
   ↓
   Evoluir com equações de Euler a partir de t=0
   
5. Comparação
   ↓
   Plotar p_sim vs p_d (ambos na mesma convenção e com mesmas condições iniciais)
```

## 🔍 Exemplo Numérico

### Cenário Realista

**Dados Estáticos (referência):**
```
p1_ref = 0.100 m  (altura do heel em repouso)
p2_ref = 0.500 m  (altura do knee em repouso)
```

**Dados Experimentais no instante inicial (t=0):**
```
p1_exp[0] = 0.095 m  (heel ligeiramente abaixo da referência)
p2_exp[0] = 0.505 m  (knee ligeiramente acima da referência)
v1_exp[0] = -0.5 m/s (heel descendo)
v2_exp[0] = 0.2 m/s  (knee subindo)
```

**Dados Convertidos:**
```
p1_d[0] = p1_ref - p1_exp[0] = 0.100 - 0.095 = 0.005 m  (5mm abaixo da referência)
p2_d[0] = p2_ref - p2_exp[0] = 0.500 - 0.505 = -0.005 m (5mm acima da referência)
v1_d[0] = -v1_exp[0] = -(-0.5) = 0.5 m/s  (descendo = positivo na convenção do modelo)
v2_d[0] = -v2_exp[0] = -(0.2) = -0.2 m/s  (subindo = negativo na convenção do modelo)
```

**Condições Iniciais da Simulação:**
```python
# ✅ CORRETO
p1_sim[0] = 0.005 m   # começa 5mm abaixo da referência (como nos dados)
p2_sim[0] = -0.005 m  # começa 5mm acima da referência (como nos dados)
v1_sim[0] = 0.5 m/s   # descendo (como nos dados)
v2_sim[0] = -0.2 m/s  # subindo (como nos dados)

# ❌ ERRADO (anterior)
p1_sim[0] = 0.0 m  # começaria na referência (diferente dos dados!)
p2_sim[0] = 0.0 m  # começaria na referência (diferente dos dados!)
v1_sim[0] = 0.0 m/s  # começaria parado (diferente dos dados!)
v2_sim[0] = 0.0 m/s  # começaria parado (diferente dos dados!)
```

## 🔧 Mudanças no Código

### Arquivo: `notebooks/analysis_rbds_r09_RNW.py`

#### 1. Retornar velocidades convertidas (Linha 348)

**ANTES:**
```python
return p1_d, p2_d, p3_d, p4_d
```

**DEPOIS:**
```python
return p1_d, p2_d, p3_d, p4_d, v1_d, v2_d, v3_d, v4_d
```

#### 2. Adicionar velocidades aos parâmetros da célula de simulação (Linha 712)

**ANTES:**
```python
def _(
    MGRF, c1_otim, c2_otim, c4_otim, dt_d, g,
    k1_otim, k2_otim, k3_otim, k4_otim, k5_otim,
    m1, m2, m3, m4, np,
    p1_d, p2_d, p3_d, p4_d,  # ← Sem velocidades
    plt, time_d,
):
```

**DEPOIS:**
```python
def _(
    MGRF, c1_otim, c2_otim, c4_otim, dt_d, g,
    k1_otim, k2_otim, k3_otim, k4_otim, k5_otim,
    m1, m2, m3, m4, np,
    p1_d, p2_d, p3_d, p4_d,
    v1_d, v2_d, v3_d, v4_d,  # ← Com velocidades
    plt, time_d,
):
```

#### 3. Usar dados experimentais convertidos como condições iniciais (Linhas 756-767)

**ANTES:**
```python
# ❌ ERRADO
p1_sim[0] = 0.0
p2_sim[0] = 0.0
p3_sim[0] = 0.0
p4_sim[0] = 0.0
v1_sim[0] = 0.0
v2_sim[0] = 0.0
v3_sim[0] = 0.0
v4_sim[0] = 0.0
```

**DEPOIS:**
```python
# ✅ CORRETO
p1_sim[0] = p1_d[0]  # posição inicial do heel (dados experimentais convertidos)
p2_sim[0] = p2_d[0]  # posição inicial do knee (dados experimentais convertidos)
p3_sim[0] = p3_d[0]  # posição inicial do trunk (dados experimentais convertidos)
p4_sim[0] = p4_d[0]  # posição inicial do crest (dados experimentais convertidos)
v1_sim[0] = v1_d[0]  # velocidade inicial do heel (dados experimentais convertidos)
v2_sim[0] = v2_d[0]  # velocidade inicial do knee (dados experimentais convertidos)
v3_sim[0] = v3_d[0]  # velocidade inicial do trunk (dados experimentais convertidos)
v4_sim[0] = v4_d[0]  # velocidade inicial do crest (dados experimentais convertidos)
```

## ✅ Validação

### Como Verificar se Está Correto

1. **Execute a célula de conversão** e verifique os prints:
   ```
   Condições iniciais dos dados experimentais convertidos:
     p1_d[0] = 0.005123 m
     p2_d[0] = -0.002456 m
     p3_d[0] = 0.001234 m
     p4_d[0] = -0.000987 m
     v1_d[0] = 0.523456 m/s
     v2_d[0] = -0.234567 m/s
     v3_d[0] = 0.123456 m/s
     v4_d[0] = -0.098765 m/s
   ```

2. **Execute a célula de simulação** e verifique os prints:
   ```
   Condições iniciais (dos dados experimentais convertidos):
     Posições: p1=0.005123, p2=-0.002456, p3=0.001234, p4=-0.000987
     Velocidades: v1=0.523456, v2=-0.234567, v3=0.123456, v4=-0.098765
   ```

3. **Verifique que os valores são idênticos** entre conversão e simulação

4. **Nos gráficos de comparação**:
   - A simulação deve começar **exatamente** no mesmo ponto que os dados experimentais
   - Não deve haver "salto" ou descontinuidade no instante inicial

## 📚 Referências

- **Liu & Nigg 2000**: Modelo de 4 massas para movimento vertical
- **Fukuchi et al. 2017**: Dados experimentais de corrida

## 🎓 Lição Aprendida

**As condições iniciais da simulação devem sempre vir dos dados experimentais!**

Ao simular um sistema dinâmico:
1. ✅ Use o estado inicial real dos dados experimentais
2. ✅ Converta para a convenção do modelo antes de usar
3. ✅ Verifique que simulação e dados começam no mesmo ponto
4. ❌ Não assuma p=0, v=0 a menos que os dados realmente comecem assim

---

**Data da Correção:** 2025-10-11  
**Autor:** Augment Agent  
**Motivo:** Correção baseada no feedback do usuário sobre condições iniciais

