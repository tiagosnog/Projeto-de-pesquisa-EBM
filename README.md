# Projeto de Pesquisa - Engenharia Biomédica

Elaboração do projeto de pesquisa para o mestrado em **Engenharia Biomédica** UFABC

## 📋 Descrição

Este projeto contém análises biomecânicas de dados de corrida, incluindo modelamento de sistemas massa-mola-amortecedor (MSD) e análise de forças de reação do solo (GRF).

## 🏗️ Estrutura do Projeto

```
.
├── src/                          # Código fonte do projeto
│   └── projeto_pesquisa_ebm/    # Pacote principal
├── notebooks/                    # Notebooks Marimo para análises
│   ├── analysis_test_rbds.py
│   ├── analysis_test_rbds_r08.py
│   ├── analysis_test_rbds_r09.py
│   ├── projeto_pesquisa.py
│   ├── modelamento_msd_nedergaard.py
│   └── modelamento_msd_niels_simplex.py
├── data/                         # Dados do projeto
│   ├── raw/                     # Dados brutos
│   └── processed/               # Dados processados
├── docs/                         # Documentação
│   ├── referencias/             # Artigos e referências
│   └── planejamento/            # Planejamento do projeto
├── tests/                        # Testes unitários
├── pyproject.toml               # Configuração do projeto e dependências
└── README.md                    # Este arquivo
```

## 🚀 Instalação

Este projeto usa [uv](https://github.com/astral-sh/uv) como gerenciador de pacotes Python.

### Pré-requisitos

- Python 3.10 ou superior
- uv instalado (veja [instruções de instalação](https://github.com/astral-sh/uv#installation))

### Configuração do Ambiente

1. Clone o repositório:
```bash
git clone https://github.com/tiagosnog/Projeto-de-pesquisa-EBM.git
cd Projeto-de-pesquisa-EBM
```

2. Crie o ambiente virtual e instale as dependências:
```bash
uv venv
uv pip install -e .
```

3. Ative o ambiente virtual:
```bash
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows
```

## ⚠️ Arquivo de Dados Faltante

**IMPORTANTE:** O arquivo `Raw Data - Measured and Modelled Trunk Acc & Upper Mass Acc & GRF.xlsx` não está no repositório.

Este arquivo é necessário para executar os notebooks de análise. Se você o tiver localmente:

```bash
cp "caminho/para/Raw Data - Measured and Modelled Trunk Acc & Upper Mass Acc & GRF.xlsx" data/raw/
```

Veja `MISSING_FILES.md` para mais detalhes e alternativas.

## 📊 Uso

### Executando Notebooks Marimo

Os notebooks foram convertidos para o formato Marimo, que oferece uma experiência interativa superior aos notebooks Jupyter tradicionais.

Para executar um notebook:

```bash
uv run marimo edit notebooks/analysis_test_rbds.py
```

Isso abrirá o notebook no seu navegador padrão.

### Notebooks Disponíveis

- **analysis_test_rbds.py**: Análise principal dos dados RBDS
- **analysis_test_rbds_r08.py**: Análise específica da amostra R08
- **analysis_test_rbds_r09.py**: Análise específica da amostra R09
- **projeto_pesquisa.py**: Extração de dados para amostra 08
- **modelamento_msd_nedergaard.py**: Modelamento MSD baseado em Nedergaard
- **modelamento_msd_niels_simplex.py**: Modelamento MSD com otimização simplex

## 📦 Dependências Principais

- **numpy**: Computação numérica
- **pandas**: Manipulação de dados
- **matplotlib**: Visualização de dados
- **scipy**: Computação científica e otimização
- **openpyxl**: Leitura/escrita de arquivos Excel
- **marimo**: Notebooks interativos reativos

## 🧪 Desenvolvimento

Para instalar dependências de desenvolvimento:

```bash
uv pip install -e ".[dev]"
```

Isso instalará ferramentas adicionais como:
- pytest (testes)
- black (formatação de código)
- ruff (linting)

## 📝 Licença

Este projeto está sob a licença especificada no arquivo LICENSE.

## 👥 Autores

- Tiago Snog
- Renato Naville Watanabe

## 📅 Data

Janeiro 2025
