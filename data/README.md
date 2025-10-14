# Dados do Projeto

Este diretório contém todos os dados utilizados no projeto de pesquisa.

## Estrutura

```
data/
├── raw/          # Dados brutos (não modificar)
└── processed/    # Dados processados (gerados pelos notebooks)
```

## Dados Brutos (raw/)

Os dados brutos incluem:

### Arquivos de Markers
- `RBDS002runT25markers.txt` - Dados de marcadores da corrida
- `RBDS008runT35markers.txt` - Dados de marcadores da corrida
- `RBDS002static.txt` - Dados estáticos
- `RBDS008static.txt` - Dados estáticos

### Arquivos de Forças
- `RBDS002runT25forces.txt` - Dados de força de reação do solo
- `RBDS008runT35forces.txt` - Dados de força de reação do solo

### Arquivos C3D
- `RBDS08runT35.c3d` - Dados de captura de movimento
- `RBDS08static.c3d` - Dados estáticos de captura

### Arquivos Excel
- `Raw_Data_GRF.xlsx` - Dados de GRF medidos
- `39452935_RBDSinfo_entrevistas.xlsx` - Informações dos participantes
- **`Raw Data - Measured and Modelled Trunk Acc & Upper Mass Acc & GRF.xlsx`** - ⚠️ ARQUIVO FALTANDO
  - Este arquivo é necessário para os notebooks `analysis_test_rbds*.py`
  - Não estava no repositório Git original
  - **AÇÃO NECESSÁRIA:** Copie este arquivo para `data/raw/` se você o tiver localmente

### Notebooks Convertidos
- `analysisTest_RBDS_r08.ipynb` - Análise da amostra R08 (convertido para Marimo)
- `analysisTest_RBDS_r09.ipynb` - Análise da amostra R09 (convertido para Marimo)

### Outros
- `RBDS002processed.txt` - Dados pré-processados
- `nikooyan2011_vib.pdf` - Referência bibliográfica

## Dados Processados (processed/)

Esta pasta contém dados gerados pelos notebooks e scripts de análise.

**Nota:** Arquivos nesta pasta são gerados automaticamente e não devem ser versionados no Git.

## Formato dos Dados

### Arquivos .txt (Markers e Forces)

Formato tabular separado por tabulação (`\t`):
- Primeira linha: cabeçalhos das colunas
- Linhas seguintes: dados numéricos

Exemplo de markers:
```
Time    R.ASISX    R.ASISY    R.ASISZ    ...
0.00    1234.56    789.01     234.56     ...
0.01    1235.67    790.12     235.67     ...
```

Exemplo de forces:
```
Time    Fx      Fy      Fz      COPx    COPy    COPz    Ty
1       35.02   1613.01 37.23   2142.33 0       934.22  6890.13
2       16.17   1565.25 30.44   2126.36 0       932.67  12564.6
```

### Arquivos .c3d

Formato binário padrão para dados de captura de movimento.
Use bibliotecas específicas para leitura (ex: `ezc3d`, `c3d`).

### Arquivos .xlsx

Planilhas Excel com múltiplas abas contendo:
- Dados medidos de GRF
- Dados de aceleração do tronco
- Informações dos participantes

## Carregando Dados

### Usando o Pacote

```python
from projeto_pesquisa_ebm import load_markers_data, load_forces_data

# Carregar markers
markers = load_markers_data('data/raw/RBDS002static.txt')

# Carregar forças
forces = load_forces_data('data/raw/RBDS002runT25forces.txt')
```

### Usando Pandas Diretamente

```python
import pandas as pd

# Carregar arquivo .txt
data = pd.read_csv('data/raw/RBDS002static.txt', sep='\t')

# Carregar arquivo .xlsx
data = pd.read_excel('data/raw/Raw_Data_GRF.xlsx', sheet_name='Measured GRF')
```

## Convenções

1. **Não modificar dados brutos**: Sempre trabalhe com cópias ou dados processados
2. **Documentar processamento**: Registre todas as transformações aplicadas
3. **Usar caminhos relativos**: Use `get_data_path()` do pacote
4. **Versionamento**: Dados brutos pequenos podem ser versionados, grandes devem estar no `.gitignore`

## Metadados

### Participantes
- RBDS002: Participante 002
- RBDS008: Participante 008

### Condições de Teste
- T25: Teste a 2.5 m/s
- T35: Teste a 3.5 m/s
- static: Teste estático

### Taxa de Amostragem
- Markers: 100 Hz (típico)
- Forces: 1000 Hz (típico)

## Referências

Para mais informações sobre os dados, consulte:
- `docs/referencias/` - Artigos científicos relacionados
- `docs/planejamento/` - Planejamento do projeto
- Notebooks em `notebooks/` - Análises detalhadas

## Backup

**Importante:** Mantenha backups dos dados brutos em local seguro!

## Questões?

Para dúvidas sobre os dados:
1. Consulte os notebooks de análise
2. Veja exemplos em `examples/basic_usage.py`
3. Leia a documentação do projeto

