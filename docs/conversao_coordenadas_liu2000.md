# Conversão de Coordenadas: Dados Experimentais → Modelo Liu & Nigg 2000

## 📌 Problema

O modelo biomecânico de Liu & Nigg (2000) utiliza uma convenção de coordenadas diferente dos dados experimentais de captura de movimento. Para comparar corretamente os dados simulados com os dados experimentais, é necessário converter as coordenadas dos dados experimentais para a convenção do modelo.

**IMPORTANTE**: As equações do modelo e a simulação estão corretas. O que precisa ser ajustado são:
1. As **condições iniciais** da simulação (devem usar dados estáticos)
2. A **conversão dos dados experimentais** para comparação nos gráficos

## 🔍 Diferenças de Convenção

### Dados Experimentais (Captura de Movimento)

- **Sistema de referência**: Solo (chão da plataforma de força)
- **Origem**: Solo = 0 metros
- **Direção positiva**: Para CIMA (eixo Y vertical positivo)
- **Exemplo**: 
  - Joelho a 0.5m do solo → `p_knee = 0.5 m`
  - Tronco a 1.2m do solo → `p_trunk = 1.2 m`

### Modelo Liu & Nigg 2000

- **Sistema de referência**: Posição inicial de cada massa
- **Origem**: Posição média durante a fase estática (antes do movimento)
- **Direção positiva**: Para BAIXO (convenção do modelo)
- **Exemplo**:
  - Massa na posição inicial → `p = 0 m`
  - Massa desceu 5cm → `p = 0.05 m` (positivo)
  - Massa subiu 3cm → `p = -0.03 m` (negativo)

## 📐 Fórmulas de Conversão

### 1. Posições de Referência

Primeiro, calculamos a posição inicial de cada massa usando a média dos dados estáticos:

```python
p1_ref = np.mean(p1_s)  # heel (calcanhar)
p2_ref = np.mean(p2_s)  # knee (joelho)
p3_ref = np.mean(p3_s)  # trunk (tronco)
p4_ref = np.mean(p4_s)  # crest (crista ilíaca)
```

### 2. Conversão de Posições

Para converter da convenção experimental para a convenção do modelo:

```python
p_modelo = p_ref - p_experimental
```

**Interpretação:**
- Se `p_experimental > p_ref`: massa está acima da posição inicial → `p_modelo < 0` (negativo)
- Se `p_experimental < p_ref`: massa está abaixo da posição inicial → `p_modelo > 0` (positivo)
- Se `p_experimental = p_ref`: massa está na posição inicial → `p_modelo = 0`

### 3. Conversão de Velocidades

As velocidades também precisam ter o sinal invertido:

```python
v_modelo = -v_experimental
```

**Interpretação:**
- Se a massa está subindo (v_experimental > 0) → v_modelo < 0 (negativo no modelo)
- Se a massa está descendo (v_experimental < 0) → v_modelo > 0 (positivo no modelo)

### 4. Acelerações

As acelerações seguem a mesma lógica das velocidades:

```python
a_modelo = -a_experimental
```

## 💡 Exemplo Numérico

Suponha que:
- Posição inicial do joelho (dados estáticos): `p2_ref = 0.50 m` (50cm acima do solo)
- Durante a corrida, o joelho está em: `p2_experimental = 0.45 m` (45cm acima do solo)

**Conversão:**
```python
p2_modelo = p2_ref - p2_experimental
p2_modelo = 0.50 - 0.45
p2_modelo = 0.05 m
```

**Interpretação:** O joelho desceu 5cm em relação à posição inicial (positivo no modelo).

## 🔄 Diagrama Visual

```
Convenção Experimental          Convenção do Modelo Liu 2000
(referência: solo)              (referência: posição inicial)

    ↑ Y (positivo)                  ↓ p (positivo)
    |                               |
    |  p_trunk = 1.2m              |  p = -0.1m (subiu)
    |                               |
    |  p_ref = 1.1m  ←─────────────┼─ p = 0 (referência)
    |                               |
    |  p_knee = 0.5m               |  p = +0.05m (desceu)
    |                               |
────┴──── Solo (y=0)               └─ (não usado)
```

## 📊 Implementação no Código

### Passo 1: Carregar dados experimentais

```python
# Dados dinâmicos (referência: solo, cresce para cima)
p1_d_exp = heel_d[:,1]/1000    # m
p2_d_exp = knee_d[:,1]/1000    # m
p3_d_exp = trunk_d[:,1]/1000   # m
p4_d_exp = crest_d[:,1]/1000   # m
```

### Passo 2: Calcular posições de referência (dos dados estáticos)

```python
# Posições de referência (média dos dados estáticos)
p1_ref = np.mean(p1_s)  # heel
p2_ref = np.mean(p2_s)  # knee
p3_ref = np.mean(p3_s)  # trunk
p4_ref = np.mean(p4_s)  # crest
```

### Passo 3: Configurar simulação com condições iniciais corretas

```python
# Condições iniciais da simulação (na posição de referência)
p1_sim[0] = 0.0  # posição inicial = 0 (referência)
p2_sim[0] = 0.0
p3_sim[0] = 0.0
p4_sim[0] = 0.0
v1_sim[0] = 0.0  # velocidade inicial = 0
v2_sim[0] = 0.0
v3_sim[0] = 0.0
v4_sim[0] = 0.0

# Executar simulação com método de Euler
# (as equações permanecem inalteradas)
```

### Passo 4: Converter dados experimentais para comparação

```python
# Converter para convenção do modelo (referência: inicial, cresce para baixo)
# APENAS PARA COMPARAÇÃO NOS GRÁFICOS
p1_d = p1_ref - p1_d_exp
p2_d = p2_ref - p2_d_exp
p3_d = p3_ref - p3_d_exp
p4_d = p4_ref - p4_d_exp

# Velocidades com sinal invertido
v1_d = -np.gradient(p1_d_exp, time_d)
v2_d = -np.gradient(p2_d_exp, time_d)
v3_d = -np.gradient(p3_d_exp, time_d)
v4_d = -np.gradient(p4_d_exp, time_d)
```

### Passo 5: Plotar comparação

```python
# Agora p1_d, p2_d, p3_d, p4_d estão na convenção do modelo
# e podem ser comparados diretamente com a simulação
plt.plot(time_d, p1_sim, label='Simulação')
plt.plot(time_d, p1_d, label='Experimental (convertido)')
plt.axhline(y=0, color='k', linestyle='--', label='Posição inicial')
```

## ✅ Validação

Para verificar se a conversão está correta:

1. **Verificar sinais**: 
   - Durante o impacto, as massas devem descer → `p_modelo` deve aumentar (positivo)
   - Durante a fase de voo, as massas devem subir → `p_modelo` deve diminuir (negativo)

2. **Verificar magnitude**:
   - A diferença entre `p_experimental` e `p_ref` deve ser igual a `p_modelo`
   - Exemplo: se `p_ref = 1.0m` e `p_experimental = 0.9m`, então `p_modelo = 0.1m`

3. **Verificar continuidade**:
   - Os gráficos de `p_modelo` vs tempo devem ser contínuos e suaves
   - Não deve haver saltos ou descontinuidades

## 📚 Referências

- Liu, W., & Nigg, B. M. (2000). A mechanical model to determine the influence of masses and mass distribution on the impact force during running. *Journal of Biomechanics*, 33(2), 219-224.

## 🔗 Arquivos Relacionados

- `notebooks/analysis_rbds_r09_RNW.py`: Implementação da conversão
- `docs/referencias/liu2000.pdf`: Artigo original do modelo
- `data/raw/RBDS002static.txt`: Dados estáticos (para calcular posições de referência)
- `data/raw/RBDS002runT25markers.txt`: Dados dinâmicos (para converter)

## 📝 Notas Importantes

1. **Sempre use dados estáticos para calcular as posições de referência**, não os primeiros valores dos dados dinâmicos.

2. **As equações do modelo estão corretas** - não precisam ser modificadas. O que muda são:
   - As condições iniciais da simulação (p=0, v=0)
   - A conversão dos dados experimentais para comparação

3. **A conversão é necessária apenas para comparação nos gráficos**. Os parâmetros do modelo (k1, k2, c1, etc.) são otimizados usando os dados estáticos.

4. **Não confunda as variáveis**:
   - `p1_d_exp`, `p2_d_exp`, etc.: dados experimentais originais (referência: solo)
   - `p1_d`, `p2_d`, etc.: dados experimentais convertidos (referência: inicial) - **para comparação**
   - `p1_s`, `p2_s`, etc.: dados estáticos (usados para calcular referências)
   - `p1_sim`, `p2_sim`, etc.: resultados da simulação (referência: inicial)

5. **Condições iniciais da simulação**:
   - Sempre iniciar em p=0, v=0 (posição de referência dos dados estáticos)
   - NÃO usar os primeiros valores dos dados dinâmicos

6. **A força de reação do solo (MGRF)** não precisa de conversão, pois é uma força vertical que atua independentemente do sistema de coordenadas.

