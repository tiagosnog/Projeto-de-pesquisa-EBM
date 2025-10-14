#!/usr/bin/env python
"""
Script de verificação da instalação do projeto

Execute este script para verificar se tudo foi instalado corretamente:
    uv run python verify_installation.py
"""

import sys
from pathlib import Path


def print_header(text):
    """Imprime cabeçalho formatado"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)


def check_imports():
    """Verifica se todas as bibliotecas necessárias estão instaladas"""
    print_header("Verificando Importações")
    
    required_packages = {
        'numpy': 'NumPy',
        'pandas': 'Pandas',
        'matplotlib': 'Matplotlib',
        'scipy': 'SciPy',
        'openpyxl': 'OpenPyXL',
        'marimo': 'Marimo',
    }
    
    all_ok = True
    for package, name in required_packages.items():
        try:
            module = __import__(package)
            version = getattr(module, '__version__', 'unknown')
            print(f"✓ {name:15} {version}")
        except ImportError:
            print(f"✗ {name:15} NÃO INSTALADO")
            all_ok = False
    
    return all_ok


def check_project_structure():
    """Verifica se a estrutura de pastas está correta"""
    print_header("Verificando Estrutura do Projeto")
    
    required_dirs = [
        'src/projeto_pesquisa_ebm',
        'notebooks',
        'data/raw',
        'data/processed',
        'docs',
        'tests',
        'examples',
    ]
    
    all_ok = True
    for dir_path in required_dirs:
        path = Path(dir_path)
        if path.exists():
            print(f"✓ {dir_path}")
        else:
            print(f"✗ {dir_path} NÃO ENCONTRADO")
            all_ok = False
    
    return all_ok


def check_files():
    """Verifica se os arquivos principais existem"""
    print_header("Verificando Arquivos Principais")
    
    required_files = [
        'pyproject.toml',
        'README.md',
        'QUICKSTART.md',
        'CHANGELOG.md',
        'CONTRIBUTING.md',
        'MIGRATION_SUMMARY.md',
        'COMMANDS.md',
        '.gitignore',
        '.marimo.toml',
        'src/projeto_pesquisa_ebm/__init__.py',
        'src/projeto_pesquisa_ebm/utils.py',
        'src/projeto_pesquisa_ebm/models.py',
        'tests/test_basic.py',
        'examples/basic_usage.py',
    ]
    
    all_ok = True
    for file_path in required_files:
        path = Path(file_path)
        if path.exists():
            size = path.stat().st_size
            print(f"✓ {file_path:45} ({size:,} bytes)")
        else:
            print(f"✗ {file_path:45} NÃO ENCONTRADO")
            all_ok = False
    
    return all_ok


def check_notebooks():
    """Verifica se os notebooks Marimo existem"""
    print_header("Verificando Notebooks Marimo")
    
    notebooks = [
        'analysis_test_rbds.py',
        'analysis_test_rbds_r08.py',
        'analysis_test_rbds_r09.py',
        'projeto_pesquisa.py',
        'modelamento_msd_nedergaard.py',
        'modelamento_msd_niels_simplex.py',
    ]
    
    all_ok = True
    for notebook in notebooks:
        path = Path('notebooks') / notebook
        if path.exists():
            size = path.stat().st_size
            print(f"✓ {notebook:40} ({size:,} bytes)")
        else:
            print(f"✗ {notebook:40} NÃO ENCONTRADO")
            all_ok = False
    
    return all_ok


def check_package():
    """Verifica se o pacote pode ser importado"""
    print_header("Verificando Pacote Python")
    
    try:
        import projeto_pesquisa_ebm
        print(f"✓ Pacote importado com sucesso")
        print(f"  Versão: {projeto_pesquisa_ebm.__version__}")
        
        # Verificar funções disponíveis
        functions = [
            'load_markers_data',
            'load_forces_data',
            'calculate_trunk_cm',
            'calculate_velocity',
            'calculate_acceleration',
            'normalize_grf',
            'get_data_path',
            'MassSpringDamperModel',
        ]
        
        print("\n  Funções disponíveis:")
        for func in functions:
            if hasattr(projeto_pesquisa_ebm, func):
                print(f"  ✓ {func}")
            else:
                print(f"  ✗ {func} NÃO ENCONTRADA")
        
        return True
    except ImportError as e:
        print(f"✗ Erro ao importar pacote: {e}")
        return False


def check_data():
    """Verifica se há dados disponíveis"""
    print_header("Verificando Dados")
    
    data_dir = Path('data/raw')
    if not data_dir.exists():
        print("✗ Diretório data/raw não encontrado")
        return False
    
    data_files = list(data_dir.glob('*'))
    if data_files:
        print(f"✓ {len(data_files)} arquivo(s) encontrado(s) em data/raw/")
        for file in data_files[:5]:  # Mostrar apenas os primeiros 5
            size = file.stat().st_size
            print(f"  • {file.name:40} ({size:,} bytes)")
        if len(data_files) > 5:
            print(f"  ... e mais {len(data_files) - 5} arquivo(s)")
        return True
    else:
        print("⚠ Nenhum arquivo encontrado em data/raw/")
        return True  # Não é erro crítico


def run_basic_test():
    """Executa um teste básico"""
    print_header("Executando Teste Básico")
    
    try:
        import numpy as np
        import pandas as pd
        from projeto_pesquisa_ebm import calculate_velocity, MassSpringDamperModel
        
        # Teste 1: Cálculo de velocidade
        dt = 0.01
        position = np.array([0, 1, 2, 3, 4])
        velocity = calculate_velocity(position, dt)
        print(f"✓ Teste de cálculo de velocidade: OK")
        
        # Teste 2: Modelo MSD
        model = MassSpringDamperModel(m1=56, m2=14, k1=34.1, k2=78.4, c=0.35)
        print(f"✓ Teste de criação de modelo MSD: OK")
        
        return True
    except Exception as e:
        print(f"✗ Erro no teste: {e}")
        return False


def main():
    """Função principal"""
    print("\n" + "╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "VERIFICAÇÃO DA INSTALAÇÃO" + " " * 28 + "║")
    print("╚" + "=" * 68 + "╝")
    
    results = {
        'Importações': check_imports(),
        'Estrutura': check_project_structure(),
        'Arquivos': check_files(),
        'Notebooks': check_notebooks(),
        'Pacote': check_package(),
        'Dados': check_data(),
        'Testes': run_basic_test(),
    }
    
    # Resumo
    print_header("RESUMO")
    
    total = len(results)
    passed = sum(results.values())
    
    for check, status in results.items():
        symbol = "✓" if status else "✗"
        print(f"{symbol} {check}")
    
    print("\n" + "=" * 70)
    print(f"  Verificações: {passed}/{total} passaram")
    
    if passed == total:
        print("\n  🎉 TUDO OK! O projeto está pronto para uso!")
        print("\n  Próximos passos:")
        print("    1. Execute: uv run marimo edit notebooks/analysis_test_rbds.py")
        print("    2. Leia: cat README.md")
        print("    3. Explore: uv run python examples/basic_usage.py")
    else:
        print("\n  ⚠ Algumas verificações falharam. Revise os erros acima.")
        sys.exit(1)
    
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()

