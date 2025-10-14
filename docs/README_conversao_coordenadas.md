# Conversão de Coordenadas - Modelo Liu & Nigg 2000

## 🎯 TL;DR (Resumo Executivo)

**Problema**: Dados experimentais e modelo Liu 2000 usam convenções de coordenadas diferentes.

**Solução**:
1. ✅ Simulação usa condições iniciais **p=0, v=0** (posição de referência dos dados estáticos)
2. ✅ Dados experimentais são **convertidos** para comparação nos gráficos
3. ✅ Equações do modelo **permanecem inalteradas** (estavam corretas)

## 📊 Convenções

| Aspecto | Dados Experimentais | Modelo Liu 2000 |
|---------|---------------------|-----------------|
| **Referência** | Solo (y=0) | Posição inicial (dados estáticos) |
| **Direção +** | Para CIMA ↑ | Para BAIXO ↓ |
| **Exemplo** | Joelho a 0.5m do solo | Massa desceu 0.05m da inicial |

## 🔧 Implementação Rápida

### 1. Posições de Referência
```python
p1_ref = np.mean(p1_s)  # média dos dados estáticos
p2_ref = np.mean(p2_s)
p3_ref = np.mean(p3_s)
p4_ref = np.mean(p4_s)
```

### 2. Condições Iniciais da Simulação
```python
p1_sim[0] = 0.0  # posição inicial = 0
v1_sim[0] = 0.0  # velocidade inicial = 0
# ... (repetir para p2, p3, p4)
```

### 3. Conversão para Comparação
```python
p1_d = p1_ref - p1_d_exp  # converter dados experimentais
v1_d = -np.gradient(p1_d_exp, time_d)  # inverter sinal
# ... (repetir para p2, p3, p4)
```

### 4. Plotar
```python
plt.plot(time_d, p1_sim, label='Simulação')
plt.plot(time_d, p1_d, label='Experimental (convertido)')
plt.axhline(y=0, linestyle='--', label='Posição inicial')
```

## 📚 Documentação Completa

- **[conversao_coordenadas_liu2000.md](conversao_coordenadas_liu2000.md)**: Documentação detalhada
- **[correcao_simulacao_liu2000.md](correcao_simulacao_liu2000.md)**: Guia prático de implementação
- **[CHANGELOG_conversao_coordenadas.md](../CHANGELOG_conversao_coordenadas.md)**: Histórico de mudanças

## 🧪 Testes

Execute os testes para validar a conversão:
```bash
python -m pytest tests/test_conversao_coordenadas.py -v
```

## ✅ Checklist

- [ ] Condições iniciais: p=0, v=0
- [ ] Posições de referência calculadas dos dados estáticos
- [ ] Dados experimentais convertidos antes da comparação
- [ ] Gráficos mostram linha y=0 (posição inicial)
- [ ] Durante impacto: valores positivos (massas descem)

## 🎓 Conceito-Chave

**A conversão é necessária APENAS para comparação nos gráficos.**

A simulação sempre usa a convenção do modelo (p=0 na posição inicial).

## 📁 Arquivos Principais

```
notebooks/
  └── analysis_rbds_r09_RNW.py  ← Implementação corrigida

docs/
  ├── conversao_coordenadas_liu2000.md  ← Documentação detalhada
  ├── correcao_simulacao_liu2000.md     ← Guia prático
  └── README_conversao_coordenadas.md   ← Este arquivo

tests/
  └── test_conversao_coordenadas.py     ← Testes unitários
```

## 🚀 Próximos Passos

1. Execute o notebook `analysis_rbds_r09_RNW.py`
2. Verifique os gráficos de comparação
3. Valide que durante o impacto os valores são positivos
4. Ajuste parâmetros do modelo se necessário

## 💡 Dica Importante

**NÃO modifique as equações do modelo!** Elas estão corretas.

O que muda são:
- Condições iniciais (p=0, v=0)
- Conversão dos dados experimentais para comparação

## 📞 Suporte

Para dúvidas ou problemas:
1. Consulte a documentação detalhada
2. Execute os testes unitários
3. Verifique o CHANGELOG

## 📖 Referência

Liu, W., & Nigg, B. M. (2000). A mechanical model to determine the influence of masses and mass distribution on the impact force during running. *Journal of Biomechanics*, 33(2), 219-224.

