import marimo

__generated_with = "0.16.5"
app = marimo.App()


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### Extração de dados para amostra 08,  markers e forces.""")
    return


@app.cell
def _():
    #Bibliotecas
    import numpy as np
    import matplotlib.pyplot as plt
    import pandas as pd
    return pd, plt


@app.cell
def _(pd):
    #Carregamento de dados: markers, amostra 08 para 3,5 m/s.
    dados_markers = pd.read_csv (r'C:/Users/Tiago/OneDrive/6-Mestrado UFABC/1.Projeto de pesquisa/1.Dados BMC/35/Markers/RBDS008runT35markers.txt', delimiter ="\t") 
    dados_markers
    return (dados_markers,)


@app.cell
def _(dados_markers):
    dados_markers.size
    return


@app.cell
def _(pd):
    #Carregamento de dados: force, amostra 08 para 3,5 m/s.
    dados_forces = pd.read_csv(r'C:/Users/Tiago/OneDrive/6-Mestrado UFABC/1.Projeto de pesquisa/1.Dados BMC/35/Forces/RBDS008runT35forces.txt', delimiter ="\t")
    dados_forces
    return (dados_forces,)


@app.cell
def _(dados_forces):
    dados_forces.size
    return


@app.cell
def _(dados_forces):
    force_Fx = dados_forces['Fx'] 
    force_Fy = dados_forces['Fy'] 
    force_Fz = dados_forces['Fz'] 
    torque_Ty = dados_forces['Ty']
    time = dados_forces['Time']
    return force_Fx, force_Fy, force_Fz, time, torque_Ty


@app.cell
def _(force_Fx, plt, time):
    _fig, _ax = plt.subplots(figsize=(25, 5))
    _ax.grid(True)
    plt.plot(time, force_Fx)
    plt.title('Gráfico t x Fx', fontsize=14)
    plt.xlabel('Time [ms]', fontsize=14)
    plt.ylabel('Force [N]', fontsize=14)
    plt.show()
    return


@app.cell
def _(force_Fy, plt, time):
    _fig, _ax = plt.subplots(figsize=(25, 5))
    _ax.grid(True)
    plt.plot(time, force_Fy, color='red')
    plt.title('Gráfico t x Fy', fontsize=14)
    plt.xlabel('Time [ms]', fontsize=14)
    plt.ylabel('Force [N]', fontsize=14)
    plt.show()
    return


@app.cell
def _(force_Fz, plt, time):
    _fig, _ax = plt.subplots(figsize=(25, 5))
    _ax.grid(True)
    plt.plot(time, force_Fz, color='green')
    plt.title('Gráfico t x Fz', fontsize=14)
    plt.xlabel('Time [ms]', fontsize=14)
    plt.ylabel('Force [N]', fontsize=14)
    plt.show()
    return


@app.cell
def _(plt, time, torque_Ty):
    _fig, _ax = plt.subplots(figsize=(25, 8))
    _ax.grid(True)
    plt.plot(time, torque_Ty, color='purple')
    plt.title('Gráfico t x Ty', fontsize=14)
    plt.xlabel('Time [ms]', fontsize=14)
    plt.ylabel('Torque [Nm]', fontsize=14)
    plt.show()
    return


@app.cell
def _():
    import marimo as mo
    return (mo,)


if __name__ == "__main__":
    app.run()
