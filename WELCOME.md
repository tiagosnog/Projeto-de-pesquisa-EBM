# 👋 Bem-vindo ao Projeto de Pesquisa EBM!

Este projeto foi completamente reorganizado e modernizado para facilitar seu uso e desenvolvimento.

## 🎯 O que mudou?

### ✨ Antes
- Notebooks Jupyter tradicionais
- Estrutura de pastas em português
- Sem gerenciamento de dependências
- Código disperso

### 🚀 Agora
- **Notebooks Marimo** - Interativos e reativos
- **Estrutura moderna** - Organização profissional
- **Gerenciamento com uv** - Rápido e confiável
- **Código modular** - Reutilizável e testável

## 📚 Documentação Disponível

Escolha o documento certo para suas necessidades:

| Documento | Quando usar |
|-----------|-------------|
| **README.md** | Visão geral completa do projeto |
| **QUICKSTART.md** | Começar rapidamente (5 minutos) |
| **COMMANDS.md** | Referência de comandos úteis |
| **MIGRATION_SUMMARY.md** | Entender as mudanças feitas |
| **CONTRIBUTING.md** | Contribuir com o projeto |
| **CHANGELOG.md** | Ver histórico de mudanças |

## 🚀 Início Rápido (3 passos)

### 1️⃣ Verificar Instalação
```bash
uv run python verify_installation.py
```

### 2️⃣ Executar um Notebook
```bash
uv run marimo edit notebooks/analysis_test_rbds.py
```

### 3️⃣ Explorar Exemplos
```bash
uv run python examples/basic_usage.py
```

## 📊 O que você pode fazer?

### Análise de Dados
```bash
# Abrir análise principal
uv run marimo edit notebooks/analysis_test_rbds.py

# Análises específicas
uv run marimo edit notebooks/analysis_test_rbds_r08.py
uv run marimo edit notebooks/analysis_test_rbds_r09.py
```

### Modelamento Biomecânico
```bash
# Modelo Nedergaard
uv run marimo edit notebooks/modelamento_msd_nedergaard.py

# Modelo com otimização
uv run marimo edit notebooks/modelamento_msd_niels_simplex.py
```

### Usar o Código
```python
from projeto_pesquisa_ebm import (
    load_markers_data,
    calculate_velocity,
    MassSpringDamperModel
)

# Carregar dados
data = load_markers_data('data/raw/RBDS002static.txt')

# Calcular velocidade
velocity = calculate_velocity(position, dt=0.01)

# Criar modelo
model = MassSpringDamperModel(m1=56, m2=14, k1=34.1, k2=78.4, c=0.35)
```

## 🎓 Aprendendo Marimo

Marimo é diferente de Jupyter:

### Vantagens
- ✅ **Reativo** - Células se atualizam automaticamente
- ✅ **Reprodutível** - Ordem de execução determinística
- ✅ **Git-friendly** - Arquivos Python puros
- ✅ **Interativo** - Widgets nativos
- ✅ **Executável** - Pode rodar como script

### Comandos Básicos
- `Shift+Enter` - Executar célula
- `Ctrl+S` - Salvar
- `Ctrl+/` - Comentar/descomentar
- `Ctrl+D` - Deletar célula

### Recursos
- [Documentação Marimo](https://docs.marimo.io/)
- [Tutorial Interativo](https://marimo.io/tutorial)
- [Exemplos](https://github.com/marimo-team/marimo/tree/main/examples)

## 🛠️ Ferramentas Disponíveis

### Desenvolvimento
```bash
# Formatar código
uv run black src/ tests/ examples/

# Verificar qualidade
uv run ruff check src/ tests/ examples/

# Executar testes
uv run pytest -v
```

### Análise
```bash
# Executar análise completa
uv run python examples/basic_usage.py

# Processar dados
uv run marimo run notebooks/projeto_pesquisa.py
```

## 📁 Estrutura do Projeto

```
projeto-pesquisa-ebm/
├── 📁 src/                 # Código fonte
├── 📓 notebooks/           # Notebooks Marimo
├── 💾 data/                # Dados (raw + processed)
├── 📚 docs/                # Documentação e referências
├── 🧪 tests/               # Testes automatizados
├── 💡 examples/            # Exemplos de uso
└── 📄 Configurações        # pyproject.toml, etc.
```

## 🎯 Próximos Passos

### Para Iniciantes
1. ✅ Execute `verify_installation.py`
2. 📖 Leia `QUICKSTART.md`
3. 🚀 Abra um notebook Marimo
4. 💡 Execute `examples/basic_usage.py`

### Para Desenvolvedores
1. 📚 Leia `CONTRIBUTING.md`
2. 🧪 Execute os testes
3. 📝 Explore o código em `src/`
4. 🔧 Configure seu editor

### Para Pesquisadores
1. 📊 Explore os notebooks
2. 📖 Leia as referências em `docs/referencias/`
3. 🔬 Adapte as análises para seus dados
4. 📝 Documente seus resultados

## 💡 Dicas Úteis

### Atalhos
```bash
# Criar aliases úteis
alias uvr="uv run"
alias uvm="uv run marimo edit"
alias uvt="uv run pytest -v"

# Usar
uvr python script.py
uvm notebooks/analysis_test_rbds.py
uvt
```

### Workflow Típico
```bash
# 1. Abrir notebook
uv run marimo edit notebooks/analysis_test_rbds.py

# 2. Fazer análises interativas
# (no navegador)

# 3. Exportar resultados
# (usar menu File > Export)

# 4. Executar testes
uv run pytest

# 5. Commit
git add .
git commit -m "feat: adiciona nova análise"
```

## 🆘 Precisa de Ajuda?

### Problemas Comuns

**Erro ao importar módulos**
```bash
uv pip install -e .
```

**Notebook não abre**
```bash
uv pip install marimo
```

**Dados não encontrados**
- Verifique caminhos em `data/raw/`
- Use `get_data_path()` do pacote

### Recursos
- 📖 Documentação completa em `README.md`
- 💬 Issues no GitHub
- 📧 Contato com mantenedores

## 🎉 Pronto para Começar!

Você tem tudo que precisa para começar a trabalhar:

✅ Ambiente configurado  
✅ Notebooks convertidos  
✅ Código modular  
✅ Documentação completa  
✅ Exemplos práticos  
✅ Testes funcionando  

**Comece agora:**
```bash
uv run marimo edit notebooks/analysis_test_rbds.py
```

---

**Boa pesquisa! 🚀**

*Projeto de Pesquisa - Engenharia Biomédica UFABC*  
*Janeiro 2025*

