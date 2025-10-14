"""
Exemplo básico de uso do pacote projeto_pesquisa_ebm

Este script demonstra como usar as funções utilitárias e modelos
do pacote para análise de dados biomecânicos.
"""

import numpy as np
import matplotlib.pyplot as plt
from projeto_pesquisa_ebm import (
    load_markers_data,
    load_forces_data,
    calculate_velocity,
    calculate_acceleration,
    normalize_grf,
    MassSpringDamperModel,
)


def example_load_data():
    """Exemplo de carregamento de dados"""
    print("=" * 60)
    print("Exemplo 1: Carregamento de Dados")
    print("=" * 60)
    
    # Carregar dados de markers
    try:
        markers = load_markers_data('data/raw/RBDS002static.txt')
        print(f"✓ Dados de markers carregados: {markers.shape}")
        print(f"  Colunas: {list(markers.columns[:5])}...")
    except FileNotFoundError:
        print("✗ Arquivo de markers não encontrado")
    
    # Carregar dados de forças
    try:
        forces = load_forces_data('data/raw/RBDS002runT25forces.txt')
        print(f"✓ Dados de forças carregados: {forces.shape}")
        print(f"  Colunas: {list(forces.columns)}")
    except FileNotFoundError:
        print("✗ Arquivo de forças não encontrado")
    
    print()


def example_kinematics():
    """Exemplo de cálculos cinemáticos"""
    print("=" * 60)
    print("Exemplo 2: Cálculos Cinemáticos")
    print("=" * 60)
    
    # Simular dados de posição
    dt = 0.01  # 100 Hz
    t = np.arange(0, 2, dt)
    position = 1.0 + 0.1 * np.sin(2 * np.pi * t)  # Movimento senoidal
    
    # Calcular velocidade e aceleração
    velocity = calculate_velocity(position, dt)
    acceleration = calculate_acceleration(velocity, dt)
    
    print(f"✓ Posição: média = {position.mean():.3f} m")
    print(f"✓ Velocidade: média = {velocity.mean():.3f} m/s")
    print(f"✓ Aceleração: média = {acceleration.mean():.3f} m/s²")
    print()


def example_grf_normalization():
    """Exemplo de normalização de GRF"""
    print("=" * 60)
    print("Exemplo 3: Normalização de GRF")
    print("=" * 60)
    
    # Simular dados de GRF
    grf = np.array([0, 500, 1000, 1500, 2000, 1500, 1000, 500, 0])
    mass = 70  # kg
    
    # Normalizar
    grf_normalized = normalize_grf(grf, mass)
    
    print(f"✓ GRF original: {grf}")
    print(f"✓ GRF normalizada (BW): {grf_normalized.round(2)}")
    print(f"  Pico: {grf_normalized.max():.2f} BW")
    print()


def example_msd_model():
    """Exemplo de modelo massa-mola-amortecedor"""
    print("=" * 60)
    print("Exemplo 4: Modelo Massa-Mola-Amortecedor")
    print("=" * 60)
    
    # Parâmetros do modelo
    m1 = 56.0  # kg (massa superior)
    m2 = 14.0  # kg (massa inferior)
    k1 = 34.1  # N/m
    k2 = 78.4  # N/m
    c = 0.35   # N.s/m
    
    # Criar modelo
    model = MassSpringDamperModel(m1, m2, k1, k2, c)
    
    # Condições iniciais
    x1_0 = 0.864  # m
    x2_0 = 0.0    # m/s
    x3_0 = 0.456  # m
    x4_0 = 0.0    # m/s
    
    # Simular
    print("✓ Simulando modelo MSD...")
    results = model.simulate(
        t_max=1.0,
        dt=0.01,
        x1_0=x1_0,
        x2_0=x2_0,
        x3_0=x3_0,
        x4_0=x4_0
    )
    
    print(f"  Tempo de simulação: {results['time'][-1]:.2f} s")
    print(f"  Posição final m1: {results['x1'][-1]:.3f} m")
    print(f"  Posição final m2: {results['x3'][-1]:.3f} m")
    print()


def example_visualization():
    """Exemplo de visualização"""
    print("=" * 60)
    print("Exemplo 5: Visualização de Dados")
    print("=" * 60)
    
    # Simular dados
    t = np.linspace(0, 1, 100)
    grf = 1000 * np.sin(np.pi * t) ** 2
    
    # Criar gráfico
    plt.figure(figsize=(10, 4))
    plt.plot(t, grf, 'b-', linewidth=2)
    plt.xlabel('Tempo (s)')
    plt.ylabel('GRF (N)')
    plt.title('Exemplo de Força de Reação do Solo')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Salvar
    output_file = 'examples/example_plot.png'
    plt.savefig(output_file, dpi=150)
    print(f"✓ Gráfico salvo em: {output_file}")
    plt.close()
    print()


def main():
    """Executa todos os exemplos"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "EXEMPLOS DE USO - PROJETO EBM" + " " * 18 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    example_load_data()
    example_kinematics()
    example_grf_normalization()
    example_msd_model()
    example_visualization()
    
    print("=" * 60)
    print("✓ Todos os exemplos executados com sucesso!")
    print("=" * 60)
    print()


if __name__ == "__main__":
    main()

