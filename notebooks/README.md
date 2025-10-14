# Notebooks Marimo

Este diretório contém os notebooks Marimo convertidos dos notebooks Jupyter originais.

## Como usar

Para executar qualquer notebook, use o comando:

```bash
uv run marimo edit <nome_do_notebook>.py
```

Por exemplo:
```bash
uv run marimo edit analysis_test_rbds.py
```

## Notebooks Disponíveis

### Análises Principais

- **analysis_test_rbds.py**: Análise completa dos dados RBDS
  - Processamento de dados de acelerômetro
  - Análise de forças de reação do solo (GRF)
  - Integração e cálculo de velocidades

- **analysis_test_rbds_r08.py**: Análise específica da amostra R08
  
- **analysis_test_rbds_r09.py**: Análise específica da amostra R09

### Extração de Dados

- **projeto_pesquisa.py**: Extração de dados para amostra 08
  - Leitura de markers e forces
  - Processamento inicial dos dados

### Modelamento MSD

- **modelamento_msd_nedergaard.py**: Modelamento baseado em Nedergaard
  - Sistema massa-mola-amortecedor de 2 graus de liberdade
  - Simulação de forças de impacto
  - Método de Euler para integração

- **modelamento_msd_niels_simplex.py**: Modelamento com otimização
  - Otimização de parâmetros k1 e k2
  - Método simplex
  - Comparação com dados medidos

## Vantagens do Marimo

Os notebooks Marimo oferecem várias vantagens sobre notebooks Jupyter tradicionais:

1. **Reatividade**: Células são automaticamente re-executadas quando suas dependências mudam
2. **Reprodutibilidade**: Ordem de execução determinística
3. **Git-friendly**: Arquivos Python puros, fáceis de versionar
4. **Interatividade**: Widgets e visualizações interativas integradas
5. **Execução como scripts**: Podem ser executados como scripts Python normais

## Dicas

- Use `Ctrl+S` ou `Cmd+S` para salvar
- Use `Shift+Enter` para executar uma célula
- O notebook salva automaticamente as alterações
- Variáveis são compartilhadas entre células de forma reativa

