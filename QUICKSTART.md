# Guia de Início Rápido

Este guia ajudará você a começar rapidamente com o projeto.

## 1. Instalação Rápida

```bash
# Clone o repositório
git clone https://github.com/tiagosnog/Projeto-de-pesquisa-EBM.git
cd Projeto-de-pesquisa-EBM

# Crie o ambiente virtual e instale dependências
uv venv
uv pip install -e .

# Ative o ambiente (opcional, uv run faz isso automaticamente)
source .venv/bin/activate  # Linux/Mac
```

## 2. Execute seu Primeiro Notebook

```bash
# Execute o notebook principal de análise
uv run marimo edit notebooks/analysis_test_rbds.py
```

Isso abrirá o notebook no seu navegador. Você verá uma interface interativa onde pode:
- Modificar código e ver resultados instantaneamente
- Visualizar gráficos e dados
- Exportar resultados

## 3. Estrutura de Dados

Os dados estão organizados em:

- `data/raw/`: Dados brutos (arquivos .txt, .xlsx, .c3d)
- `data/processed/`: Dados processados (gerados pelos notebooks)

## 4. Principais Análises

### Análise de GRF (Ground Reaction Force)

Execute o notebook `analysis_test_rbds.py` para:
- Processar dados de acelerômetro
- Calcular forças de reação do solo
- Visualizar padrões de corrida

### Modelamento MSD

Execute os notebooks de modelamento para:
- Simular sistemas massa-mola-amortecedor
- Otimizar parâmetros do modelo
- Comparar com dados experimentais

## 5. Comandos Úteis

```bash
# Executar um notebook
uv run marimo edit notebooks/<nome>.py

# Executar um notebook como script (sem interface)
uv run marimo run notebooks/<nome>.py

# Instalar nova dependência
uv pip install <pacote>

# Atualizar dependências
uv pip install --upgrade -e .

# Executar testes (quando disponíveis)
uv run pytest
```

## 6. Dicas de Uso do Marimo

- **Salvar**: `Ctrl+S` ou `Cmd+S`
- **Executar célula**: `Shift+Enter`
- **Adicionar célula**: Clique no `+` entre células
- **Modo de apresentação**: Clique no ícone de apresentação
- **Exportar**: Menu File > Export

## 7. Próximos Passos

1. Explore os notebooks em `notebooks/`
2. Leia a documentação em `docs/`
3. Verifique os artigos de referência em `docs/referencias/`
4. Adapte as análises para seus próprios dados

## 8. Solução de Problemas

### Erro ao importar módulos

```bash
# Reinstale o pacote em modo editável
uv pip install -e .
```

### Notebook não abre

```bash
# Verifique se o marimo está instalado
uv pip list | grep marimo

# Reinstale se necessário
uv pip install marimo
```

### Dados não encontrados

Verifique se os caminhos nos notebooks apontam para `data/raw/` ou ajuste conforme necessário.

## 9. Recursos Adicionais

- [Documentação do Marimo](https://docs.marimo.io/)
- [Documentação do uv](https://github.com/astral-sh/uv)
- [Documentação do NumPy](https://numpy.org/doc/)
- [Documentação do Pandas](https://pandas.pydata.org/docs/)

## 10. Suporte

Para questões ou problemas:
1. Verifique a documentação em `docs/`
2. Revise os exemplos nos notebooks
3. Abra uma issue no GitHub

