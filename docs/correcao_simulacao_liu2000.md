# Correção da Simulação do Modelo Liu & Nigg 2000

## 🎯 Resumo da Correção

### O que estava errado:
❌ Condições iniciais da simulação usavam os primeiros valores dos dados dinâmicos  
❌ Dados experimentais não eram convertidos para a convenção do modelo antes da comparação

### O que foi corrigido:
✅ Condições iniciais da simulação agora usam p=0, v=0 (posição de referência dos dados estáticos)  
✅ Dados experimentais são convertidos para a convenção do modelo antes da comparação nos gráficos  
✅ As equações do modelo permanecem inalteradas (estavam corretas)

## 📐 Convenções de Coordenadas

### Dados Experimentais (Captura de Movimento)
- **Referência**: Solo (y = 0 no chão)
- **Direção positiva**: Para CIMA (↑)
- **Exemplo**: Joelho a 0.5m do solo → `p_knee_exp = 0.5 m`

### Modelo Liu & Nigg 2000
- **Referência**: Posição inicial (obtida dos dados estáticos)
- **Direção positiva**: Para BAIXO (↓)
- **Exemplo**: Massa na posição inicial → `p = 0 m`
- **Exemplo**: Massa desceu 5cm → `p = 0.05 m` (positivo)

## 🔧 Implementação Correta

### 1. Calcular Posições de Referência (Dados Estáticos)

```python
# Média dos dados estáticos = posição inicial de referência
p1_ref = np.mean(p1_s)  # heel
p2_ref = np.mean(p2_s)  # knee
p3_ref = np.mean(p3_s)  # trunk
p4_ref = np.mean(p4_s)  # crest
```

### 2. Configurar Simulação (Condições Iniciais Corretas)

```python
# Condições iniciais: posição de referência
p1_sim[0] = 0.0  # na posição inicial (referência)
p2_sim[0] = 0.0
p3_sim[0] = 0.0
p4_sim[0] = 0.0

# Velocidades iniciais
v1_sim[0] = 0.0  # em repouso
v2_sim[0] = 0.0
v3_sim[0] = 0.0
v4_sim[0] = 0.0
```

### 3. Executar Simulação (Equações Inalteradas)

```python
for i in range(n_steps - 1):
    # Equação para massa 1 (pé) - CORRETA, não muda
    dv1dt = (m1*g - MGRF[i] - k1*(p1[i]-p3[i]) - k2*(p1[i]-p2[i]) 
             - c1*(v1[i]-v3[i]) - c2*(v1[i]-v2[i])) / m1
    
    # Equação para massa 2 (perna) - CORRETA, não muda
    dv2dt = (m2*g + k2*(p1[i]-p2[i]) - k3*(p2[i]-p3[i]) 
             + c2*(v1[i]-v2[i])) / m2
    
    # Equação para massa 3 (coxa) - CORRETA, não muda
    dv3dt = (m3*g + k1*(p1[i]-p3[i]) + k3*(p2[i]-p3[i]) 
             - (k4+k5)*(p3[i]-p4[i]) + c1*(v1[i]-v3[i]) 
             - c4*(v3[i]-v4[i])) / m3
    
    # Equação para massa 4 (tronco) - CORRETA, não muda
    dv4dt = (m4*g + (k4+k5)*(p3[i]-p4[i]) + c4*(v3[i]-v4[i])) / m4
    
    # Atualizar velocidades e posições (Método de Euler)
    v1[i+1] = v1[i] + dv1dt * dt
    p1[i+1] = p1[i] + v1[i] * dt
    # ... (repetir para v2, p2, v3, p3, v4, p4)
```

### 4. Converter Dados Experimentais para Comparação

```python
# Converter dados experimentais para convenção do modelo
# APENAS PARA COMPARAÇÃO NOS GRÁFICOS
p1_d = p1_ref - p1_d_exp  # inverte referência e direção
p2_d = p2_ref - p2_d_exp
p3_d = p3_ref - p3_d_exp
p4_d = p4_ref - p4_d_exp

# Velocidades também invertem sinal
v1_d = -np.gradient(p1_d_exp, time_d)
v2_d = -np.gradient(p2_d_exp, time_d)
v3_d = -np.gradient(p3_d_exp, time_d)
v4_d = -np.gradient(p4_d_exp, time_d)
```

### 5. Plotar Comparação

```python
plt.figure(figsize=(15, 10))

plt.subplot(2, 2, 1)
plt.plot(time_d, p1_sim, 'b-', linewidth=1.2, label='Simulação')
plt.plot(time_d, p1_d, 'orange', linewidth=0.8, alpha=0.7, 
         label='Experimental (convertido)')
plt.axhline(y=0, color='k', linestyle='--', alpha=0.3, 
            label='Posição inicial')
plt.xlabel('Tempo (s)')
plt.ylabel('Posição (m) - ref: inicial')
plt.title('Massa 1 (Pé)')
plt.legend()
plt.grid(True)

# ... (repetir para massas 2, 3, 4)
```

## 📊 Interpretação dos Resultados

### Gráficos de Posição

- **Linha y=0 (tracejada)**: Posição inicial de referência
- **Valores positivos**: Massa desceu em relação à posição inicial
- **Valores negativos**: Massa subiu em relação à posição inicial

### Durante o Impacto (fase de contato com o solo)

- Todas as massas devem **descer** → valores **positivos** no gráfico
- A massa 1 (pé) deve ter maior deslocamento
- As massas superiores (trunk, crest) têm menor deslocamento

### Durante a Fase de Voo

- Todas as massas devem **subir** → valores **negativos** no gráfico
- O movimento deve ser suave e contínuo

## ✅ Checklist de Validação

- [ ] Condições iniciais: p=0, v=0 ✓
- [ ] Posições de referência calculadas dos dados estáticos ✓
- [ ] Equações do modelo inalteradas ✓
- [ ] Dados experimentais convertidos para comparação ✓
- [ ] Gráficos mostram linha y=0 (posição inicial) ✓
- [ ] Durante impacto: valores positivos (massas descem) ✓
- [ ] Durante voo: valores negativos (massas sobem) ✓

## 🔍 Variáveis Importantes

| Variável | Descrição | Convenção |
|----------|-----------|-----------|
| `p1_s`, `p2_s`, `p3_s`, `p4_s` | Dados estáticos | Solo (↑) |
| `p1_ref`, `p2_ref`, `p3_ref`, `p4_ref` | Posições de referência | Valor absoluto |
| `p1_d_exp`, `p2_d_exp`, `p3_d_exp`, `p4_d_exp` | Dados experimentais originais | Solo (↑) |
| `p1_d`, `p2_d`, `p3_d`, `p4_d` | Dados experimentais convertidos | Inicial (↓) |
| `p1_sim`, `p2_sim`, `p3_sim`, `p4_sim` | Resultados da simulação | Inicial (↓) |

## 📚 Referências

- Liu, W., & Nigg, B. M. (2000). A mechanical model to determine the influence of masses and mass distribution on the impact force during running. *Journal of Biomechanics*, 33(2), 219-224.

## 📁 Arquivos Relacionados

- `notebooks/analysis_rbds_r09_RNW.py`: Implementação corrigida
- `docs/conversao_coordenadas_liu2000.md`: Documentação detalhada da conversão
- `tests/test_conversao_coordenadas.py`: Testes unitários da conversão

## 💡 Dicas

1. **Sempre verifique as condições iniciais**: Devem ser p=0, v=0
2. **Não modifique as equações**: Elas estão corretas
3. **Converta apenas para comparação**: A simulação usa a convenção do modelo
4. **Use dados estáticos para referência**: Não use dados dinâmicos
5. **Verifique os sinais**: Durante impacto, valores devem ser positivos

## ⚠️ Erros Comuns

1. ❌ Usar `p1_d[0]` como condição inicial → ✅ Usar `0.0`
2. ❌ Comparar `p1_sim` com `p1_d_exp` → ✅ Comparar `p1_sim` com `p1_d` (convertido)
3. ❌ Modificar as equações do modelo → ✅ Manter equações inalteradas
4. ❌ Usar primeiro valor dos dados dinâmicos como referência → ✅ Usar média dos dados estáticos

