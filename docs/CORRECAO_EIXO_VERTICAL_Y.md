# Correção: Eixo Y é VERTICAL (Fukuchi 2017)

## 📌 Descoberta Importante

Segundo **Fukuchi et al. 2017** (a fonte dos dados experimentais), a convenção de eixos é:

- **Eixo X** (índice 0): Médio-lateral (lado a lado)
- **Eixo Y** (índice 1): **VERTICAL** (para cima/baixo) ← **CORRETO**
- **Eixo Z** (índice 2): Anteroposterior (direção do movimento)

## ✅ O Código Estava Correto!

O notebook `analysis_rbds_r09_RNW.py` já estava usando o **eixo Y (índice 1)** para todas as massas, que é o correto!

### O que estava errado:
- ❌ A **documentação** dizia que Y era "anteroposterior"
- ❌ Os **comentários** explicavam incorretamente a razão

### O que estava certo:
- ✅ O **código** usava Y (índice 1) - correto!
- ✅ A **força Fy** era usada como MGRF - correto!

## 🔧 Correções Realizadas

### 1. Documentação Atualizada

**ANTES:**
```markdown
- **Eixo Y** (índice 1): Anteroposterior (direção do movimento) ← **USADO**
- **Eixo Z** (índice 2): Vertical (para cima/baixo)

**Razão**: O modelo Liu 2000 analisa o movimento na direção anteroposterior (Y)
```

**DEPOIS:**
```markdown
- **Eixo Y** (índice 1): **VERTICAL** (para cima/baixo) ← **USADO**
- **Eixo Z** (índice 2): Anteroposterior (direção do movimento)

**Razão**: O modelo Liu & Nigg 2000 analisa o movimento na **direção vertical (Y)**,
que é a direção onde ocorre o impacto e a absorção de choque durante a corrida.

**Referências:**
- Fukuchi et al. 2017: Define Y como eixo vertical
- Liu & Nigg 2000: Modelo de 4 massas para movimento vertical
```

### 2. Comentários no Código Atualizados

**Dados Estáticos:**
```python
# IMPORTANTE: Usar eixo Y (índice 1) = VERTICAL (Fukuchi 2017)
# Eixo Y = direção vertical (para cima/baixo) - onde ocorre o impacto
p1_s = heel_s[:, 1] / 1000  # Eixo Y do heel = VERTICAL
```

**Dados Dinâmicos:**
```python
# IMPORTANTE: Usando eixo Y (índice 1) = VERTICAL (Fukuchi 2017)
# Eixo Y = direção vertical - onde ocorre o impacto durante a corrida
p1_d_exp = heel_d[:,1]/1000  # m (eixo Y - VERTICAL)
```

**Força de Reação do Solo:**
```python
# IMPORTANTE: Fy = Força VERTICAL (Fukuchi 2017)
# Fy é a força de reação do solo na direção vertical (eixo Y)
MGRF = Forces[['Fy']].values.squeeze()
```

### 3. Prints de Verificação Atualizados

```python
print("=== POSIÇÕES DE REFERÊNCIA (dados estáticos - eixo Y VERTICAL) ===")
print(f"p1_ref (heel):  {p1_ref:.4f} m (altura acima do solo)")
print(f"p2_ref (knee):  {p2_ref:.4f} m (altura acima do solo)")
print(f"p3_ref (trunk): {p3_ref:.4f} m (altura acima do solo)")
print(f"p4_ref (crest): {p4_ref:.4f} m (altura acima do solo)")
```

## 📊 Sistema de Coordenadas Correto

### Convenção Fukuchi 2017

```
        Y (VERTICAL) ↑
        |
        |  ← Movimento vertical (impacto)
        |     Modelo Liu 2000 analisa ESTE eixo
        |
        |________→ Z (anteroposterior - direção da corrida)
       /
      /
     ↙
    X (médio-lateral)
```

### Índices nos Arrays NumPy

| Índice | Eixo | Direção | Uso no Modelo Liu 2000 |
|--------|------|---------|------------------------|
| 0 | X | Médio-lateral | ❌ Não usado |
| 1 | Y | **VERTICAL** | ✅ **USADO** |
| 2 | Z | Anteroposterior | ❌ Não usado |

## 🎯 Por que Y é Vertical?

### Modelo Liu & Nigg 2000

O modelo de **4 massas em série** (pé, perna, coxa, tronco) foi desenvolvido para analisar:

1. **Impacto vertical** durante a corrida
2. **Absorção de choque** na direção vertical
3. **Compressão das massas** devido à força de reação do solo vertical
4. **Oscilações verticais** das massas durante o contato com o solo

### Dados Experimentais (Fukuchi 2017)

- **Fy**: Força de reação do solo na direção **VERTICAL**
- **Marcadores**: Posições Y representam **altura acima do solo**
- **Movimento**: Durante o impacto, as massas se movem principalmente na direção **VERTICAL**

## ✅ Validação

### Como Verificar se Está Correto

1. **Valores de referência** devem representar alturas:
   ```
   p1_ref (heel):  ≈ 0.05-0.15 m (altura do calcanhar acima do solo)
   p2_ref (knee):  ≈ 0.40-0.60 m (altura do joelho acima do solo)
   p3_ref (trunk): ≈ 0.90-1.20 m (altura do tronco acima do solo)
   p4_ref (crest): ≈ 1.00-1.30 m (altura da crista ilíaca acima do solo)
   ```

2. **Força Fy** deve ser:
   - Em repouso: ≈ 785 N (peso do corpo)
   - Durante impacto: 1500-2400 N (2-3× o peso do corpo)

3. **Durante o impacto**:
   - Massas **descem** (valores de p aumentam na convenção do modelo)
   - Força vertical **aumenta** (Fy > peso do corpo)

## 📚 Referências

1. **Fukuchi, R. K., Fukuchi, C. A., & Duarte, M. (2017).** A public dataset of running biomechanics and the effects of running speed on lower extremity kinematics and kinetics. *PeerJ*, 5, e3298.
   - Define a convenção de eixos dos dados experimentais
   - **Y = VERTICAL**

2. **Liu, W., & Nigg, B. M. (2000).** A mechanical model to determine the influence of masses and mass distribution on the impact force during running. *Journal of Biomechanics*, 33(2), 219-224.
   - Modelo de 4 massas para movimento **VERTICAL**
   - Analisa impacto e absorção de choque na direção **VERTICAL**

## 🎓 Lição Aprendida

**Sempre verifique a convenção de eixos na fonte original dos dados!**

Mesmo que o código esteja funcionalmente correto, a documentação incorreta pode:
- Causar confusão
- Dificultar a manutenção
- Levar a erros futuros

## 📝 Checklist de Verificação

- [x] Código usa eixo Y (índice 1) ✅
- [x] Documentação corrigida para "Y = VERTICAL" ✅
- [x] Comentários atualizados ✅
- [x] Força Fy identificada como vertical ✅
- [x] Prints de verificação atualizados ✅
- [x] Referências adicionadas ✅

## 🔗 Arquivos Modificados

- `notebooks/analysis_rbds_r09_RNW.py`: Documentação e comentários atualizados
- `docs/CORRECAO_EIXO_VERTICAL_Y.md`: Este documento

## 💡 Próximos Passos

1. ✅ Executar o notebook e verificar os valores de referência
2. ✅ Confirmar que as alturas fazem sentido fisicamente
3. ✅ Validar que a força Fy está na faixa esperada
4. ✅ Comparar simulação com dados experimentais

---

**Data da Correção:** 2025-10-11  
**Autor:** Augment Agent  
**Motivo:** Correção da documentação baseada em Fukuchi 2017

