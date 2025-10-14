import marimo

__generated_with = "0.16.5"
app = marimo.App()


@app.cell
def _():
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd


    from scipy.signal import decimate
    from scipy.integrate import cumulative_trapezoid
    from scipy.optimize import minimize
    return cumulative_trapezoid, decimate, minimize, np, pd, plt


@app.cell
def _(pd):
    speeds = pd.read_excel('Raw Data - Measured and Modelled Trunk Acc & Upper Mass Acc & GRF.xlsx', sheet_name='Measured TrunkAcc').iloc[0].values[1:].astype(str)
    subjects = list(pd.read_excel('Raw Data - Measured and Modelled Trunk Acc & Upper Mass Acc & GRF.xlsx', sheet_name='Measured TrunkAcc').columns[1:].astype(str).str.split('.'))
    subject_index = dict()
    trial = 0
    last_speed = '-1'
    for i in range(len(subjects)):
        if speeds[i] != last_speed:
            trial = 0
        else:
            trial = trial + 1
        last_speed = speeds[i]
        subject_index[subjects[i][0]+','+speeds[i] + ','+ str(trial)] = i + 1

    subject_index
    return (subject_index,)


@app.cell
def _(pd):
    data_acc = pd.read_excel('Raw Data - Measured and Modelled Trunk Acc & Upper Mass Acc & GRF.xlsx', sheet_name='Measured TrunkAcc', skiprows=2)
    data_acc
    return (data_acc,)


@app.cell
def _(pd):
    data_grf = pd.read_excel('Raw Data - Measured and Modelled Trunk Acc & Upper Mass Acc & GRF.xlsx', sheet_name='Measured GRF', skiprows=2)
    data_grf
    return (data_grf,)


@app.cell
def _(data_acc, data_grf, decimate, np, subject_index):
    index = '1,2,0'
    a1 = data_acc.iloc[:,subject_index[index]].values
    time = data_acc.iloc[:,0].values[~np.isnan(a1)]
    a1 = a1[~np.isnan(a1)]
    grf = data_grf.iloc[:,subject_index[index]].values
    grf = grf[~np.isnan(grf)]
    grf = decimate(grf, 30)
    return a1, grf, time


@app.cell
def _(grf, plt, time):
    plt.plot(time, grf)
    return


@app.cell
def _(a1, plt, time):
    plt.plot(time, a1)
    return


@app.cell
def _(a1, cumulative_trapezoid):
    _v1 = cumulative_trapezoid(a1, dx=0.1, initial=0)
    p1 = cumulative_trapezoid(_v1, dx=0.1, initial=0)
    return


@app.cell
def _(pd, plt):
    data_static = pd.read_csv('/media/rnwatanabe/Data/Renato/tiagoMestrado/RBDS002static.txt', sep='\t')
    dt = data_static['Time'].values[1]
    trunk_cm = (data_static[['R.ASISX', 'R.ASISY', 'R.ASISZ']].values + data_static[['L.ASISX', 'L.ASISY', 'L.ASISZ']].values + data_static[['R.PSISX', 'R.PSISY', 'R.PSISZ']].values + data_static[['L.PSISX', 'L.PSISY', 'L.PSISZ']].values) / 4
    time_1 = data_static['Time'].values
    plt.plot(data_static['Time'], trunk_cm[:, 2])
    return dt, time_1, trunk_cm


@app.cell
def _(dt, np, plt, time_1, trunk_cm):
    p1_1 = trunk_cm[:, 2]
    _v1 = np.gradient(p1_1, dt)
    a1_1 = np.gradient(_v1, dt)
    plt.plot(time_1, a1_1)
    return a1_1, p1_1


@app.cell
def _(a1_1, minimize, np, p1_1):
    p1_medio = p1_1.mean() / 1000
    a1_medio = a1_1.mean() / 1000

    def erro(theta, a1, p1):
        g = -9.81
        return np.sum((a1 - (theta[0] ** 2 * (p1 - theta[1]) + g)) ** 2)
    theta = minimize(erro, [1, 1], (a1_medio, p1_medio)).x
    theta
    return


if __name__ == "__main__":
    app.run()
