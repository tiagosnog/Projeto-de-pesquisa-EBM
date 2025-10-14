# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

## [0.1.0] - 2025-01-08

### Adicionado

#### Estrutura do Projeto
- Reorganização completa da estrutura de pastas seguindo convenções Python
- Criação de estrutura modular com `src/`, `data/`, `notebooks/`, `tests/`, `docs/`
- Configuração do projeto com `pyproject.toml` para uso com `uv`
- Ambiente virtual gerenciado por `uv`

#### Notebooks Marimo
- Conversão de 6 notebooks Jupyter para formato Marimo:
  - `analysis_test_rbds.py` - Análise principal dos dados RBDS
  - `analysis_test_rbds_r08.py` - Análise da amostra R08
  - `analysis_test_rbds_r09.py` - Análise da amostra R09
  - `projeto_pesquisa.py` - Extração de dados
  - `modelamento_msd_nedergaard.py` - Modelo MSD Nedergaard
  - `modelamento_msd_niels_simplex.py` - Modelo MSD com otimização

#### Código Fonte
- Módulo `utils.py` com funções utilitárias:
  - Carregamento de dados de markers e forças
  - Cálculo de centro de massa do tronco
  - Cálculos cinemáticos (velocidade, aceleração)
  - Normalização de GRF
  - Gerenciamento de caminhos de dados

- Módulo `models.py` com modelos biomecânicos:
  - Classe `MassSpringDamperModel` para modelamento MSD
  - Simulação usando método de Euler
  - Otimização de parâmetros

#### Documentação
- README.md atualizado com instruções completas
- QUICKSTART.md para início rápido
- README.md específico para notebooks
- Exemplos de uso em `examples/basic_usage.py`
- CHANGELOG.md para rastreamento de mudanças

#### Testes
- Configuração de testes com pytest
- Testes básicos de importação e funcionalidade

#### Configuração
- `.gitignore` atualizado para Python e Marimo
- `.marimo.toml` para configuração do Marimo
- `pyproject.toml` com todas as dependências

#### Dependências
- numpy >= 1.24.0
- pandas >= 2.0.0
- matplotlib >= 3.7.0
- scipy >= 1.10.0
- openpyxl >= 3.1.0
- marimo >= 0.9.0

### Modificado
- Estrutura de pastas reorganizada de português para inglês
- Dados movidos para `data/raw/`
- Artigos movidos para `docs/referencias/`
- Planejamento movido para `docs/planejamento/`

### Removido
- Notebooks Jupyter originais (movidos para `old_structure/`)
- Estrutura antiga de pastas (preservada em `old_structure/`)

## Notas de Migração

### De Jupyter para Marimo
Os notebooks foram convertidos automaticamente usando `marimo convert`. 
Algumas adaptações manuais podem ser necessárias para:
- Widgets interativos
- Visualizações complexas
- Dependências entre células

### Uso do uv
O projeto agora usa `uv` como gerenciador de pacotes. Para executar comandos:
```bash
uv run <comando>
```

Ao invés de ativar o ambiente virtual manualmente.

