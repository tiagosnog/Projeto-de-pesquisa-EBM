import marimo

__generated_with = "0.16.5"
app = marimo.App()


@app.cell
def _():
    import numpy as np
    import matplotlib.pyplot as plt
    return np, plt


@app.cell
def _():
    # Definições iniciais e parâmetros
    m1 = 56.0       # Massa 1 (kg), 80% da massa total de 70 kg
    m2 = 14.0       # Massa 2 (kg), 20% da massa total de 70 kg
    k1 = 34.1       # Constante da mola 1 (N/m)
    k2 = 78.4       # Constante da mola 2 (N/m)
    c = 0.35        # Coeficiente de amortecimento (N.s/m)
    g = -9.81       # Aceleração devido à gravidade (m/s^2)
    x1 = 0.864      # Posição inicial de x1 (m)
    x3 = 0.456      # Posição inicial de x3 (m)
    l1 = 0.408      # Comprimento de repouso da mola (m) 
    l2 = 0.241      # Comprimento de repouso da mola (m)
    return c, g, k1, k2, l1, l2, m1, m2


@app.cell
def _(c, g, k1, k2, l1, l2, m1, m2, np):
    # Funções de aceleração
    def x2_dot(x1, x2, x3, x4):
        return g - k1 * (x1 - l1 - x3) / m1

    def x4_dot(x1, x2, x3, x4):
        return g + (k1 * (x1 - l1 - x3) - k2 * (x3 - l2) - c * x4) / m2

    # Funções de força
    def F1(x1, x2, x3, x4):
        return m1 * g - k1 * (x1 - l1 - x3)

    def F2(x1, x2, x3, x4):
        return m2 * g + k1 * (x1 - l1 - x3) - k2 * (x3 - l2) - c * x4
    t_int_sim = 0.01
    # Parâmetros de simulação
    t_max = 20  # Intervalo de tempo para a simulação (s)
    passos_sim = int(t_max / t_int_sim)  # Tempo total de simulação (s)
    _F_inicial = 700  # Número de passos na simulação
    t_int_impulso = 0.1
    passos_impulso = int(t_max / t_int_impulso)
    # Definindo os parâmetros do impulso (força inicial é 700 N e ela aumenta ao longo do tempo)
    _Fimp = np.zeros(passos_impulso)
    for _i in range(passos_impulso):
        _Fimp[_i] = _F_inicial * 1.05 ** (_i * t_int_impulso)  # Força inicial de impulso (em Newtons)
    t_calc = np.linspace(0, t_max, passos_sim)  # Intervalo de tempo para o impulso (0.1 segundos)
    _x1_calc = np.zeros(passos_sim)  # Número de passos para o impulso
    _x2_calc = np.zeros(passos_sim)
    _x3_calc = np.zeros(passos_sim)
    _x4_calc = np.zeros(passos_sim)
    x2_dot_calc = np.zeros(passos_sim)  # A força dobra a cada 0.1s
    x4_dot_calc = np.zeros(passos_sim)
    _F1_calc = np.zeros(passos_sim)
    # Inicializando os arrays para armazenar os resultados
    _F2_calc = np.zeros(passos_sim)
    F_resultante_calc = np.zeros(passos_sim)
    for _i in range(1, passos_sim):
        _x1_calc[_i] = _x1_calc[_i - 1] + t_int_sim * _x2_calc[_i - 1]
        _x2_calc[_i] = _x2_calc[_i - 1] + t_int_sim * x2_dot(_x1_calc[_i - 1], _x2_calc[_i - 1], _x3_calc[_i - 1], _x4_calc[_i - 1])
        _x3_calc[_i] = _x3_calc[_i - 1] + t_int_sim * _x4_calc[_i - 1]
        _x4_calc[_i] = _x4_calc[_i - 1] + t_int_sim * x4_dot(_x1_calc[_i - 1], _x2_calc[_i - 1], _x3_calc[_i - 1], _x4_calc[_i - 1])  # Aceleração de x1 (m1)
        x2_dot_calc[_i] = x2_dot(_x1_calc[_i], _x2_calc[_i], _x3_calc[_i], _x4_calc[_i])  # Aceleração de x3 (m2)
        x4_dot_calc[_i] = x4_dot(_x1_calc[_i], _x2_calc[_i], _x3_calc[_i], _x4_calc[_i])  # Força F1
        _F1_calc[_i] = F1(_x1_calc[_i], _x2_calc[_i], _x3_calc[_i], _x4_calc[_i])  # Força F2
        _F2_calc[_i] = F2(_x1_calc[_i], _x2_calc[_i], _x3_calc[_i], _x4_calc[_i])  # Força resultante (F1 + F2)
        if _i < passos_impulso:
            F_resultante_calc[_i] = _F1_calc[_i] + _F2_calc[_i] + _Fimp[_i]
    # Método de Euler para simulação
        else:
            F_resultante_calc[_i] = _F1_calc[_i] + _F2_calc[_i] + _Fimp[-1]  # Calcular a força resultante
    return (
        F1,
        F2,
        F_resultante_calc,
        passos_sim,
        t_calc,
        t_int_sim,
        t_max,
        x2_dot,
        x4_dot,
    )


@app.cell
def _(F_resultante_calc, plt, t_calc):
    plt.figure(figsize=(10, 5))
    plt.plot(t_calc, F_resultante_calc, color='green')
    plt.title('Força Resultante x Tempo')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Força Resultante (N)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    return


@app.cell
def _(F1, F2, np, passos_sim, t_int_sim, t_max, x2_dot, x4_dot):
    _F_inicial = 700
    impulso_fator = 1.1
    t_ajuste_impulso = 0.1
    t_calc_1 = np.linspace(0, t_max, passos_sim)
    _x1_calc = np.zeros(passos_sim)
    _x2_calc = np.zeros(passos_sim)
    _x3_calc = np.zeros(passos_sim)
    _x4_calc = np.zeros(passos_sim)
    x2_dot_calc_1 = np.zeros(passos_sim)
    x4_dot_calc_1 = np.zeros(passos_sim)
    _F1_calc = np.zeros(passos_sim)
    _F2_calc = np.zeros(passos_sim)
    F_resultante_calc_1 = np.zeros(passos_sim)
    tempo_acumulado = 0.0
    _Fimp = _F_inicial
    for _i in range(1, passos_sim):
        _x1_calc[_i] = _x1_calc[_i - 1] + t_int_sim * _x2_calc[_i - 1]
        _x2_calc[_i] = _x2_calc[_i - 1] + t_int_sim * x2_dot(_x1_calc[_i - 1], _x2_calc[_i - 1], _x3_calc[_i - 1], _x4_calc[_i - 1])
        _x3_calc[_i] = _x3_calc[_i - 1] + t_int_sim * _x4_calc[_i - 1]
        _x4_calc[_i] = _x4_calc[_i - 1] + t_int_sim * x4_dot(_x1_calc[_i - 1], _x2_calc[_i - 1], _x3_calc[_i - 1], _x4_calc[_i - 1])
        x2_dot_calc_1[_i] = x2_dot(_x1_calc[_i], _x2_calc[_i], _x3_calc[_i], _x4_calc[_i])
        x4_dot_calc_1[_i] = x4_dot(_x1_calc[_i], _x2_calc[_i], _x3_calc[_i], _x4_calc[_i])
        _F1_calc[_i] = F1(_x1_calc[_i], _x2_calc[_i], _x3_calc[_i], _x4_calc[_i])
        _F2_calc[_i] = F2(_x1_calc[_i], _x2_calc[_i], _x3_calc[_i], _x4_calc[_i])
        tempo_acumulado = tempo_acumulado + t_int_sim
        if tempo_acumulado >= t_ajuste_impulso:
            _Fimp = _F_inicial * impulso_fator ** int(tempo_acumulado // t_ajuste_impulso)
            tempo_acumulado = 0.0
        F_resultante_calc_1[_i] = _F1_calc[_i] + _F2_calc[_i] + _Fimp
    return F_resultante_calc_1, t_calc_1, x2_dot_calc_1, x4_dot_calc_1


@app.cell
def _(F_resultante_calc_1, plt, t_calc_1, x2_dot_calc_1, x4_dot_calc_1):
    plt.figure(figsize=(12, 10))
    plt.subplot(2, 2, 3)
    plt.plot(t_calc_1, F_resultante_calc_1, color='green')
    plt.title('Força resultante x tempo')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Força (N)')
    plt.axhline(y=700, color='blue', linestyle='--')
    plt.legend()
    plt.subplot(2, 2, 4)
    plt.plot(t_calc_1, x2_dot_calc_1, label='Aceleração x2_dot (massa 1)', linestyle='-.', color='red')
    plt.plot(t_calc_1, x4_dot_calc_1, label='Aceleração x4_dot (massa 2)', linestyle='--', color='purple')
    plt.title('Acelerações x tempo')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Aceleração (m/s²)')
    plt.legend()
    plt.tight_layout()
    plt.show()
    return


if __name__ == "__main__":
    app.run()
