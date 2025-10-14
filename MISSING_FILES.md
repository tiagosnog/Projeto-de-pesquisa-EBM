# ⚠️ Arquivos Faltantes

## Arquivo Principal Faltando

### `Raw Data - Measured and Modelled Trunk Acc & Upper Mass Acc & GRF.xlsx`

**Status:** ❌ NÃO ENCONTRADO NO REPOSITÓRIO

**Descrição:**
Este arquivo Excel contém dados medidos e modelados de:
- Aceleração do tronco (Trunk Acc)
- Aceleração da massa superior (Upper Mass Acc)
- Força de reação do solo (GRF)

**Usado em:**
- `notebooks/analysis_test_rbds.py`
- `notebooks/analysis_test_rbds_r08.py`
- `notebooks/analysis_test_rbds_r09.py`

**Sheets esperadas:**
- `Measured TrunkAcc` - Dados de aceleração do tronco medidos
- `Measured GRF` - Dados de GRF medidos
- Possivelmente outras sheets com dados modelados

**Localização esperada:**
```
data/raw/Raw Data - Measured and Modelled Trunk Acc & Upper Mass Acc & GRF.xlsx
```

## 🔧 Como Resolver

### Opção 1: Se você tem o arquivo localmente

```bash
# Copie o arquivo para a pasta correta
cp "caminho/para/Raw Data - Measured and Modelled Trunk Acc & Upper Mass Acc & GRF.xlsx" data/raw/
```

### Opção 2: Se o arquivo está em outro local

Atualize os notebooks para apontar para o local correto:

```python
# Em vez de:
data = pd.read_excel('Raw Data - Measured and Modelled Trunk Acc & Upper Mass Acc & GRF.xlsx', ...)

# Use:
from projeto_pesquisa_ebm import get_data_path
data = pd.read_excel(get_data_path('Raw Data - Measured and Modelled Trunk Acc & Upper Mass Acc & GRF.xlsx'), ...)
```

### Opção 3: Usar dados alternativos

Se você não tem este arquivo, pode usar os dados disponíveis em `data/raw/`:
- `RBDS002runT25forces.txt`
- `RBDS008runT35forces.txt`
- `RBDS002runT25markers.txt`
- `RBDS008runT35markers.txt`

## 📝 Atualizar Notebooks

Depois de adicionar o arquivo, você pode precisar atualizar os caminhos nos notebooks:

### Em `notebooks/analysis_test_rbds.py`

Procure por linhas como:
```python
speeds = pd.read_excel('Raw Data - Measured and Modelled Trunk Acc & Upper Mass Acc & GRF.xlsx', ...)
```

E atualize para:
```python
from projeto_pesquisa_ebm import get_data_path
filepath = get_data_path('Raw Data - Measured and Modelled Trunk Acc & Upper Mass Acc & GRF.xlsx')
speeds = pd.read_excel(filepath, ...)
```

## 🔍 Verificar se o arquivo foi adicionado

```bash
# Verificar se o arquivo existe
ls -lh data/raw/Raw\ Data\ -\ Measured\ and\ Modelled\ Trunk\ Acc\ \&\ Upper\ Mass\ Acc\ \&\ GRF.xlsx

# Ou use Python
python -c "from pathlib import Path; print(Path('data/raw/Raw Data - Measured and Modelled Trunk Acc & Upper Mass Acc & GRF.xlsx').exists())"
```

## 📊 Estrutura Esperada do Arquivo

Com base no código dos notebooks, o arquivo deve ter:

### Sheet: "Measured TrunkAcc"
- Linha 0: Velocidades (speeds)
- Linha 1: Cabeçalhos das colunas (sujeitos)
- Linha 2+: Dados de aceleração

### Sheet: "Measured GRF"
- Linha 0-1: Metadados
- Linha 2: Cabeçalhos
- Linha 3+: Dados de GRF

## 🆘 Precisa de Ajuda?

Se você não conseguir encontrar este arquivo:

1. **Verifique backups** - O arquivo pode estar em um backup antigo
2. **Verifique outros computadores** - Se você trabalhou em outro local
3. **Entre em contato com colaboradores** - Alguém da equipe pode ter o arquivo
4. **Recrie os dados** - Se necessário, os dados podem ser recriados a partir dos arquivos .txt

## 📌 Nota Importante

Este arquivo **não estava no repositório Git original** clonado de:
```
https://github.com/tiagosnog/Projeto-de-pesquisa-EBM.git
```

Isso sugere que:
- O arquivo pode ter sido adicionado ao `.gitignore` (por ser grande)
- O arquivo pode estar apenas localmente
- O arquivo pode precisar ser baixado de outra fonte

## ✅ Checklist

- [ ] Arquivo localizado
- [ ] Arquivo copiado para `data/raw/`
- [ ] Notebooks testados com o arquivo
- [ ] Caminhos atualizados se necessário
- [ ] Arquivo adicionado ao `.gitignore` se for muito grande

---

**Última atualização:** 08 de Janeiro de 2025

