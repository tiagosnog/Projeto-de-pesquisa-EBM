# Comandos Úteis

Referência rápida de comandos para trabalhar com o projeto.

## 🔧 Configuração Inicial

```bash
# Clonar repositório
git clone https://github.com/tiagosnog/Projeto-de-pesquisa-EBM.git
cd Projeto-de-pesquisa-EBM

# Criar ambiente virtual
uv venv

# Instalar projeto em modo editável
uv pip install -e .

# Instalar com dependências de desenvolvimento
uv pip install -e ".[dev]"
```

## 📓 Notebooks Marimo

```bash
# Abrir notebook específico
uv run marimo edit notebooks/analysis_test_rbds.py
uv run marimo edit notebooks/projeto_pesquisa.py
uv run marimo edit notebooks/modelamento_msd_nedergaard.py

# Executar notebook como script (sem interface)
uv run marimo run notebooks/analysis_test_rbds.py

# Criar novo notebook
uv run marimo new notebooks/meu_notebook.py

# Converter Jupyter para Marimo
uv run marimo convert notebook.ipynb -o notebooks/notebook.py

# Exportar notebook para HTML
uv run marimo export html notebooks/analysis_test_rbds.py -o output.html

# Exportar para script Python
uv run marimo export script notebooks/analysis_test_rbds.py -o output.py
```

## 🧪 Testes

```bash
# Executar todos os testes
uv run pytest

# Executar com verbosidade
uv run pytest -v

# Executar testes específicos
uv run pytest tests/test_basic.py

# Executar com cobertura
uv run pytest --cov=src/projeto_pesquisa_ebm

# Gerar relatório de cobertura HTML
uv run pytest --cov=src/projeto_pesquisa_ebm --cov-report=html

# Executar testes em paralelo
uv run pytest -n auto
```

## 📦 Gerenciamento de Pacotes

```bash
# Listar pacotes instalados
uv pip list

# Instalar novo pacote
uv pip install <pacote>

# Instalar versão específica
uv pip install <pacote>==1.2.3

# Atualizar pacote
uv pip install --upgrade <pacote>

# Desinstalar pacote
uv pip uninstall <pacote>

# Sincronizar com pyproject.toml
uv pip sync

# Gerar requirements.txt
uv pip freeze > requirements.txt
```

## 🎨 Formatação e Linting

```bash
# Formatar código com black
uv run black src/ tests/ examples/

# Verificar formatação sem modificar
uv run black --check src/ tests/ examples/

# Executar linting com ruff
uv run ruff check src/ tests/ examples/

# Corrigir problemas automaticamente
uv run ruff check --fix src/ tests/ examples/

# Formatar e verificar tudo
uv run black src/ tests/ examples/ && uv run ruff check src/ tests/ examples/
```

## 🐍 Python

```bash
# Executar script Python
uv run python script.py

# Executar módulo
uv run python -m projeto_pesquisa_ebm

# Abrir REPL Python
uv run python

# Executar exemplo
uv run python examples/basic_usage.py

# Executar com profiling
uv run python -m cProfile script.py
```

## 📊 Análise de Dados

```bash
# Executar análise principal
uv run marimo edit notebooks/analysis_test_rbds.py

# Processar dados específicos
uv run python -c "from projeto_pesquisa_ebm import load_markers_data; print(load_markers_data('data/raw/RBDS002static.txt').head())"

# Executar pipeline completo
uv run python scripts/run_pipeline.py  # (se existir)
```

## 🔍 Debugging

```bash
# Executar com debugger
uv run python -m pdb script.py

# Executar com ipython
uv run ipython

# Executar notebook com debug
uv run marimo edit --debug notebooks/analysis_test_rbds.py
```

## 📝 Documentação

```bash
# Gerar documentação (se configurado)
uv run sphinx-build -b html docs/ docs/_build/

# Servir documentação localmente
uv run python -m http.server -d docs/_build/html/

# Visualizar README
cat README.md
cat QUICKSTART.md
```

## 🔄 Git

```bash
# Status
git status

# Adicionar arquivos
git add .

# Commit
git commit -m "feat: adiciona nova funcionalidade"

# Push
git push origin main

# Pull
git pull origin main

# Criar branch
git checkout -b feature/nova-feature

# Ver diferenças
git diff

# Ver histórico
git log --oneline
```

## 🧹 Limpeza

```bash
# Remover cache Python
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

# Remover cache pytest
rm -rf .pytest_cache

# Remover arquivos temporários
find . -type f -name "*~" -delete
find . -type f -name "*.swp" -delete

# Limpar tudo
rm -rf __pycache__ .pytest_cache *.pyc *~ *.swp
```

## 📈 Performance

```bash
# Profiling de CPU
uv run python -m cProfile -o profile.stats script.py
uv run python -m pstats profile.stats

# Profiling de memória
uv run python -m memory_profiler script.py

# Benchmark
uv run python -m timeit "import numpy as np; np.random.rand(1000)"
```

## 🌐 Servidor

```bash
# Iniciar servidor Marimo
uv run marimo edit --host 0.0.0.0 --port 8080

# Servir arquivos estáticos
uv run python -m http.server 8000

# Jupyter (se instalado)
uv run jupyter notebook
```

## 🔐 Ambiente

```bash
# Ativar ambiente virtual (opcional com uv)
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Desativar ambiente
deactivate

# Verificar Python usado
which python
python --version

# Verificar uv
which uv
uv --version
```

## 📋 Informações do Projeto

```bash
# Ver estrutura do projeto
ls -la

# Ver dependências
cat pyproject.toml

# Ver notebooks disponíveis
ls -la notebooks/

# Ver exemplos
ls -la examples/

# Ver testes
ls -la tests/
```

## 🚀 Atalhos Úteis

```bash
# Alias úteis (adicione ao ~/.bashrc ou ~/.zshrc)
alias uvr="uv run"
alias uvp="uv run python"
alias uvm="uv run marimo edit"
alias uvt="uv run pytest -v"
alias uvf="uv run black . && uv run ruff check ."

# Uso:
uvr python script.py
uvm notebooks/analysis_test_rbds.py
uvt
uvf
```

## 💡 Dicas

1. **Use `uv run` para garantir ambiente correto**
   ```bash
   uv run python script.py  # Sempre usa o ambiente do projeto
   ```

2. **Marimo salva automaticamente**
   - Não precisa salvar manualmente
   - Arquivos são Python puro

3. **Testes antes de commit**
   ```bash
   uv run pytest && uv run black --check . && uv run ruff check .
   ```

4. **Atualizar dependências**
   ```bash
   uv pip install --upgrade -e .
   ```

5. **Verificar instalação**
   ```bash
   uv run python -c "import projeto_pesquisa_ebm; print(projeto_pesquisa_ebm.__version__)"
   ```

