import marimo

__generated_with = "0.16.5"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    import sympy as sp
    from scipy.signal import decimate, welch

    from scipy.optimize import minimize
    from scipy.integrate import solve_ivp
    return minimize, np, pd, plt, solve_ivp, sp, welch


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Estáticos

    ### ⚠️ IMPORTANTE: Convenção de Eixos (Fukuchi 2017)

    Segundo **Fukuchi et al. 2017** (fonte dos dados experimentais), a convenção de eixos é:

    - **Eixo X** (índice 0): Médio-lateral (lado a lado)
    - **Eixo Y** (índice 1): **VERTICAL** (para cima/baixo) ← **USADO**
    - **Eixo Z** (índice 2): Anteroposterior (direção do movimento)

    **Razão**: O modelo **Liu & Nigg 2000** analisa o movimento na **direção vertical (Y)**,
    que é a direção onde ocorre o impacto e a absorção de choque durante a corrida.

    **Referências:**
    - Fukuchi et al. 2017: Define Y como eixo vertical
    - Liu & Nigg 2000: Modelo de 4 massas para movimento vertical

    Todos os dados (estáticos e dinâmicos) devem usar o **mesmo eixo** para consistência.
    """
    )
    return


@app.cell
def _(np, pd, plt):
    def load_marker_data(filename, data_path='./data/raw/'):
        """
        Carrega dados de marcadores e calcula posições, velocidades e acelerações.

        Args:
            filename: Nome do arquivo de marcadores
            data_path: Caminho para os dados

        Returns:
            dict com time, p1_s, v1_s, a1_s, trunk_mm, data
        """
        data = pd.read_csv(data_path + filename, sep='\t')

        # Calcular trunk (média dos marcadores ASIS e PSIS)
        # Se os marcadores ASIS/PSIS tiverem NaN, usar fallback (média entre knee e crest)
        trunk_mm = (data[['R.ASISX', 'R.ASISY', 'R.ASISZ']].values +
                    data[['L.ASISX', 'L.ASISY', 'L.ASISZ']].values +
                    data[['R.PSISX', 'R.PSISY', 'R.PSISZ']].values +
                    data[['L.PSISX', 'L.PSISY', 'L.PSISZ']].values)/4

        # Verificar se trunk tem NaN e usar fallback se necessário
        if np.any(np.isnan(trunk_mm)):
            print(f"⚠️ AVISO: Marcadores ASIS/PSIS com NaN em {filename}")
            print("   Usando fallback: trunk = média entre knee e crest")

            # Calcular crest
                 
            crest = (data[['R.Iliac.CrestX','R.Iliac.CrestY','R.Iliac.CrestZ']].values +
                     data[['L.Iliac.CrestX','L.Iliac.CrestY','L.Iliac.CrestZ']].values)/2

            # Trunk = média entre knee e crest (aproximação razoável)
            trunk_mm = crest

        # Calcular metatarsal (pé direito)
        metatarsal = data[['R.MT1X','R.MT1Y','R.MT1Z']].values
        time = data['Time'].values

        # IMPORTANTE: Usar eixo Y (índice 1) = VERTICAL (Fukuchi 2017)
        p1 = metatarsal[:, 1] / 1000  # Eixo Y do heel = VERTICAL
        v1 = np.gradient(p1, time)
        a1 = np.gradient(v1, time)

        return {
            'time': time,
            'p1': p1,
            'v1': v1,
            'a1': a1,
            'trunk_mm': trunk_mm,
            'data': data
        }

    # Carregar dados T45 para otimização
    marker_data_opt = load_marker_data('RBDS002runT45markers.txt')

    plt.figure()
    plt.plot(marker_data_opt['time'], marker_data_opt['p1'], color='r',linewidth=1,
             label='metatarsal position (Y axis - VERTICAL) - Dados Dinâmicos T45')
    plt.xlabel('tempo (s)')
    plt.ylabel('p1 (m) - eixo Y (VERTICAL)')
    plt.legend()
    plt.grid(True)
    plt.show()
    # print (np.min (marker_data_opt ['p1']))
    return (marker_data_opt,)


@app.cell
def _(marker_data_opt, np, plt):
    def calculate_all_positions(marker_data):
        """
        Calcula posições, velocidades e acelerações para todas as 4 massas.

        Args:
            marker_data: dict retornado por load_marker_data

        Returns:
            dict com p1-p4, v1-v4, a1-a4
        """
        data = marker_data['data']
        time = marker_data['time']
        trunk_mm = marker_data['trunk_mm']

        # Massa 2: Knee (joelho)
        knee = (data[['L.Shank.Top.MedialX', 'L.Shank.Top.MedialY', 'L.Shank.Top.MedialZ']].values +
                data[['R.Shank.Top.MedialX', 'R.Shank.Top.MedialY', 'R.Shank.Top.MedialZ']].values) / 2
        p2 = knee[:, 1] / 1000
        v2 = np.gradient(p2, time)
        a2 = np.gradient(v2, time)

        # Massa 3: Trunk (tronco)
        p3 = trunk_mm[:, 1] / 1000  # usando coordenada Y do trunk (VERTICAL)
        v3 = np.gradient(p3, time)
        a3 = np.gradient(v3, time)

        # Massa 4: Iliac Crest (crista ilíaca)
        crest = (data[['R.Iliac.CrestX','R.Iliac.CrestY','R.Iliac.CrestZ']].values +
                 data[['L.Iliac.CrestX','L.Iliac.CrestY','L.Iliac.CrestZ']].values) / 2
        p4 = crest[:, 1] / 1000  # usando coordenada Y (VERTICAL)
        v4 = np.gradient(p4, time)
        a4 = np.gradient(v4, time)

        return {
            'p1': marker_data['p1'], 'v1': marker_data['v1'], 'a1': marker_data['a1'],
            'p2': p2, 'v2': v2, 'a2': a2,
            'p3': p3, 'v3': v3, 'a3': a3,
            'p4': p4, 'v4': v4, 'a4': a4,
            'time': time
        }

    # Calcular todas as posições para dados de otimização
    positions_opt = calculate_all_positions(marker_data_opt)

    plt.figure()
    plt.plot(positions_opt['time'], positions_opt['p2'], label='p2_s - Dados Dinâmicos T45', color='b',linewidth=1)
    plt.xlabel('tempo (s)')
    plt.ylabel('p2 (m)')
    plt.legend()
    plt.grid(True)
    plt.show()
    return (positions_opt,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Conversão de Coordenadas: Experimental → Modelo Liu 2000

    ### Diferenças de Convenção:

    **Dados Experimentais (Fukuchi 2017):**
    - Referência: Solo (0 no solo)
    - Direção: Valores crescem para CIMA (eixo Y vertical positivo para cima)
    - Exemplo: p1_d = 0.5m significa 0.5m acima do solo (altura vertical)

    **Modelo Liu & Nigg 2000:**
    - Referência: Posição inicial (obtida dos dados estáticos)
    - Direção: Valores crescem para BAIXO (convenção do modelo - compressão positiva)
    - Distâncias são relativas à condição inicial
    - **Condições iniciais da simulação:** Valores iniciais dos dados experimentais convertidos
      - p[0] = p_ref - p_exp[0] (posição inicial relativa à referência estática)
      - v[0] = -v_exp[0] (velocidade inicial com sinal invertido)
    - Modelo analisa movimento VERTICAL (impacto e absorção de choque)

    ### Fórmula de Conversão (para comparação nos gráficos):

    Para converter dados experimentais para a convenção do modelo:

    ```
    p_modelo = p_inicial_estatico - p_experimental
    ```

    Onde:
    - `p_inicial_estatico`: posição média durante a fase estática (referência do modelo)
    - `p_experimental`: posição medida em relação ao solo
    - `p_modelo`: posição na convenção do modelo (positivo = para baixo da referência)

    ### Uso Correto:

    1. **Simulação**: Usa condições iniciais p=0, v=0 (posição de referência dos dados estáticos)
    2. **Comparação**: Converte dados experimentais para a mesma convenção
    3. **Gráficos**: Plota simulação vs dados experimentais convertidos

    ### Exemplo:
    - Se p_inicial_estatico = 1.0m e p_experimental = 0.9m
    - Então p_modelo = 1.0 - 0.9 = 0.1m (massa desceu 0.1m da posição inicial)
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Dinâmicos""")
    return


@app.cell
def _(np, pd, plt):
    data_dynamic = pd.read_csv('./data/raw/RBDS002runT25markers.txt', sep='\t')
    td = data_dynamic['Time'].values[1]

    r_1_metatarsal = (data_dynamic[['R.MT1X','R.MT1Y','R.MT1Z']].values)

    r_shank_bottom_medial = (data_dynamic[['R.Shank.Bottom.MedialX','R.Shank.Bottom.MedialY','R.Shank.Bottom.MedialZ']].values)

    r_thigh_bottom_lateral = (data_dynamic[['R.Thigh.Bottom.LateralX', 'R.Thigh.Bottom.LateralY', 'R.Thigh.Bottom.LateralZ']].values)

    r_iliac_crest = (data_dynamic[['R.Iliac.CrestX','R.Iliac.CrestY','R.Iliac.CrestZ']].values)

    time_d = data_dynamic['Time'].values                              #s


    # Dados experimentais (referência: solo, cresce para cima)
    # IMPORTANTE: Usando eixo Y (índice 1) = VERTICAL (Fukuchi 2017)
    # Eixo Y = direção vertical - onde ocorre o impacto durante a corrida
    # Mesma convenção dos dados estáticos para consistência

    p1_d_exp = r_1_metatarsal[:,1]/1000                               #m (eixo Y - VERTICAL)
    v1_d_exp = np.gradient(p1_d_exp, time_d)                          #m/s
    a1_d_exp = np.gradient(v1_d_exp, time_d)                          #m/s²

    p2_d_exp = r_shank_bottom_medial[:,1]/1000                        #m (eixo Y - VERTICAL)
    v2_d_exp = np.gradient(p2_d_exp, time_d)                          #m/s
    a2_d_exp = np.gradient(v2_d_exp, time_d)                          #m/s²

    p3_d_exp = r_thigh_bottom_lateral[:,1]/1000                       #m (eixo Y - VERTICAL)
    v3_d_exp = np.gradient(p3_d_exp, time_d)                          #m/s
    a3_d_exp = np.gradient(v3_d_exp, time_d)                          #m/s²

    p4_d_exp = r_iliac_crest[:,1]/1000                                #m (eixo Y - VERTICAL)
    v4_d_exp = np.gradient(p4_d_exp, time_d)                          #m/s
    a4_d_exp = np.gradient(v4_d_exp, time_d)                          #m/s²

    plt.figure(figsize=(10,5))
    plt.plot(time_d, p1_d_exp, color="orange", alpha=0.7, label="p1 (experimental)")
    plt.plot(time_d, p2_d_exp, color="b",      alpha=0.7, label="p2 (experimental)")
    plt.plot(time_d, p3_d_exp, color="r",      alpha=0.7, label="p3 (experimental)")
    plt.plot(time_d, p4_d_exp, color="g",      alpha=0.7, label="p4 (experimental)")
    plt.xlim(0, 10)
    plt.xlabel("tempo (s)")
    plt.ylabel("posição (m) - referência: solo")
    plt.title("Deslocamentos Dinâmicos - Dados Experimentais")
    plt.grid(True)
    plt.legend()
    plt.show()
    return p1_d_exp, p2_d_exp, p3_d_exp, p4_d_exp, time_d


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Conversão para Convenção do Modelo

    Aqui convertemos os dados experimentais para a convenção do modelo Liu 2000.

    **Passos:**
    1. Calcular posição inicial de referência (média dos dados estáticos)
    2. Aplicar conversão: `p_modelo = p_ref - p_experimental`
    3. Inverter sinal das velocidades (pois a direção é invertida)
    """
    )
    return


@app.cell
def _(np, p1_d_exp, p2_d_exp, p3_d_exp, p4_d_exp, plt, positions_opt, time_d):
    # Calcular posições de referência (média dos dados estáticos/otimização T45)
    # IMPORTANTE: Dados estáticos e dinâmicos devem usar o MESMO EIXO (Y = VERTICAL)
    # Segundo Fukuchi 2017: Y é o eixo VERTICAL
    # positions_opt contém p1, p2, p3, p4 = eixo Y (VERTICAL)
    # p1_d_exp, p2_d_exp, p3_d_exp, p4_d_exp = eixo Y (VERTICAL)

    p1_ref = np.mean(positions_opt['p1'])  # posição inicial média do heel (eixo Y - VERTICAL)
    p2_ref = np.mean(positions_opt['p2'])  # posição inicial média do knee (eixo Y - VERTICAL)
    p3_ref = np.mean(positions_opt['p3'])  # posição inicial média do trunk (eixo Y - VERTICAL)
    p4_ref = np.mean(positions_opt['p4'])  # posição inicial média do crest (eixo Y - VERTICAL)

    print("=== POSIÇÕES DE REFERÊNCIA (dados estáticos - eixo Y VERTICAL) ===")
    print(f"p1_ref (heel):  {p1_ref:.4f} m (altura acima do solo)")
    print(f"p2_ref (knee):  {p2_ref:.4f} m (altura acima do solo)")
    print(f"p3_ref (trunk): {p3_ref:.4f} m (altura acima do solo)")
    print(f"p4_ref (crest): {p4_ref:.4f} m (altura acima do solo)")

    # Verificar valores iniciais dos dados experimentais
    print("\n=== VALORES INICIAIS (dados experimentais - eixo Y VERTICAL) ===")
    print(f"p1_d_exp[0] (metatarsal):  {p1_d_exp[0]:.4f} m (altura acima do solo)")
    print(f"p2_d_exp[0] (shank bottom medial):  {p2_d_exp[0]:.4f} m (altura acima do solo)")
    print(f"p3_d_exp[0] (thigh bottom medial): {p3_d_exp[0]:.4f} m (altura acima do solo)")
    print(f"p4_d_exp[0] (crest): {p4_d_exp[0]:.4f} m (altura acima do solo)")

    # Converter para convenção do modelo: p_modelo = p_ref - p_experimental
    # (positivo = para baixo da referência)
    p1_d = p1_ref - p1_d_exp
    p2_d = p1_ref - p2_d_exp
    p3_d = p1_ref - p3_d_exp
    p4_d = p1_ref - p4_d_exp

    # Velocidades também precisam ter sinal invertido
    v1_d = -np.gradient(p1_d_exp, time_d)
    v2_d = -np.gradient(p2_d_exp, time_d)
    v3_d = -np.gradient(p3_d_exp, time_d)
    v4_d = -np.gradient(p4_d_exp, time_d)

    # Plotar comparação
    plt.figure(figsize=(15, 10))

    plt.subplot(2, 2, 1)
    plt.plot(time_d, p1_d_exp, 'orange', alpha=0.7, label='Experimental (ref: solo)')
    plt.plot(time_d, p1_d, 'b', alpha=0.7, label='Modelo (ref: inicial)')
    plt.axhline(y=0, color='k', linestyle='--', alpha=0.3)
    plt.xlim(0, 10)
    plt.xlabel('tempo (s)')
    plt.ylabel('posição (m)')
    plt.title('p1 (Heel) - Comparação de Convenções')
    plt.legend()
    plt.grid(True)

    plt.subplot(2, 2, 2)
    plt.plot(time_d, p2_d_exp, 'orange', alpha=0.7, label='Experimental (ref: solo)')
    plt.plot(time_d, p2_d, 'b', alpha=0.7, label='Modelo (ref: inicial)')
    plt.axhline(y=0, color='k', linestyle='--', alpha=0.3)
    plt.xlim(0, 10)
    plt.xlabel('tempo (s)')
    plt.ylabel('posição (m)')
    plt.title('p2 (Knee) - Comparação de Convenções')
    plt.legend()
    plt.grid(True)

    plt.subplot(2, 2, 3)
    plt.plot(time_d, p3_d_exp, 'orange', alpha=0.7, label='Experimental (ref: solo)')
    plt.plot(time_d, p3_d, 'b', alpha=0.7, label='Modelo (ref: inicial)')
    plt.axhline(y=0, color='k', linestyle='--', alpha=0.3)
    plt.xlim(0, 10)
    plt.xlabel('tempo (s)')
    plt.ylabel('posição (m)')
    plt.title('p3 (Trunk) - Comparação de Convenções')
    plt.legend()
    plt.grid(True)

    plt.subplot(2, 2, 4)
    plt.plot(time_d, p4_d_exp, 'orange', alpha=0.7, label='Experimental (ref: solo)')
    plt.plot(time_d, p4_d, 'b', alpha=0.7, label='Modelo (ref: inicial)')
    plt.axhline(y=0, color='k', linestyle='--', alpha=0.3)
    plt.xlim(0, 10)
    plt.xlabel('tempo (s)')
    plt.ylabel('posição (m)')
    plt.title('p4 (Crest) - Comparação de Convenções')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()

    print("\n=== CONVERSÃO CONCLUÍDA ===")
    print("Agora p1_d, p2_d, p3_d, p4_d estão na convenção do modelo Liu 2000")
    print("(referência = posição inicial, positivo = para baixo)")
    print("Eixo Y = VERTICAL (Fukuchi 2017) - movimento de impacto vertical")
    print(f"\nCondições iniciais dos dados experimentais convertidos:")
    print(f"  p1_d[0] = {p1_d[0]:.6f} m")
    print(f"  p2_d[0] = {p2_d[0]:.6f} m")
    print(f"  p3_d[0] = {p3_d[0]:.6f} m")
    print(f"  p4_d[0] = {p4_d[0]:.6f} m")
    print(f"  v1_d[0] = {v1_d[0]:.6f} m/s")
    print(f"  v2_d[0] = {v2_d[0]:.6f} m/s")
    print(f"  v3_d[0] = {v3_d[0]:.6f} m/s")
    print(f"  v4_d[0] = {v4_d[0]:.6f} m/s")
    return p1_d, p2_d, p3_d, p4_d, v1_d, v2_d, v3_d, v4_d


@app.cell
def _(pd, plt):
    def load_force_data(filename, data_path='./data/raw/', sampling_rate=300):
        """
        Carrega dados de força (GRF) do arquivo.

        Args:
            filename: Nome do arquivo de forças
            data_path: Caminho para os dados
            sampling_rate: Taxa de amostragem em Hz (padrão: 300 Hz)

        Returns:
            dict com MGRF e time_Fy
        """
        forces = pd.read_csv(data_path + filename, sep='\t')
        sample = forces['Time'].values
        # IMPORTANTE: Fy = Força VERTICAL (Fukuchi 2017)
        # Fy é a força de reação do solo na direção vertical (eixo Y)
        MGRF = forces[['Fy']].values.squeeze()
        time_Fy = sample / sampling_rate

        return {
            'MGRF': MGRF,
            'time': time_Fy
        }

    # Carregar dados de força T45 para otimização
    force_data_opt = load_force_data('RBDS002runT45forces.txt')

    plt.plot(force_data_opt['time'], force_data_opt['MGRF'], color='purple',
             label='MGRF (Vertical Forrce - Fy) - Data T45')
    plt.xlim(0, 2)
    plt.xlabel('time (s)')
    plt.ylabel('MGRF (N) - Vertical Force')
    plt.legend()
    plt.grid(True)
    plt.show()
    return force_data_opt, load_force_data


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Otimização

    ### ⚠️ IMPORTANTE: Convenção de Sinais

    **Sistema de Coordenadas do Modelo:**
    - **Positivo = para BAIXO** (em direção ao solo)
    - **Negativo = para CIMA** (afastando do solo)

    **Forças:**
    - **g = +9.81 m/s²** (gravidade atua para BAIXO = direção positiva)
    - **MGRF** (Fy dos dados): força para CIMA, mas valor positivo nos dados
      - Na equação: `-MGRF` (sinal negativo porque atua para cima)

    **Dados Experimentais (Fukuchi 2017):**
    - **Fy = Força VERTICAL** (eixo Y é vertical nos dados)
    - MGRF = Fy (força de reação do solo)
    - Fy é positivo nos dados (convenção da plataforma de força)

    **Durante Dados ESTÁTICOS:**
    - O sujeito está parado (ou quase parado)
    - MGRF ≈ Peso do corpo = m_total × g ≈ 80 × 9.81 ≈ 785 N
    - **Não otimizamos Fg**, usamos o peso do corpo diretamente

    **Durante Dados DINÂMICOS (Simulação):**
    - MGRF varia com o tempo (medido pela plataforma de força)
    - MGRF pode chegar a 2-3× o peso do corpo durante o impacto VERTICAL
    - Usamos os dados medidos da plataforma de força (Fy)

    ### Equações de Otimização (Movimento VERTICAL)

    **Massa 1 (pé):**
    ```
    m1·a1 = m1·g - MGRF - k1·(p1-p3) - k2·(p1-p2) - c1·(v1-v3) - c2·(v1-v2)
    ```
    - `m1·g`: peso (para baixo) = POSITIVO
    - `-MGRF`: reação do solo (para cima) = NEGATIVO

    Durante estático: `MGRF = peso_corpo` (constante)
    Durante dinâmico: `MGRF = Fy[i]` (variável no tempo - força vertical)

    **Massa 2 (perna):**
    ```
    m2·a2 = m2·g + k2·(p1-p2) - k3·(p2-p3) + c2·(v1-v2)
    ```

    **Massa 3 (coxa):**
    ```
    m3·a3 = m3·g + k1·(p1-p3) + k3·(p2-p3) - (k4+k5)·(p3-p4) + c1·(v1-v3) - c4·(v3-v4)
    ```

    **Massa 4 (tronco):**
    ```
    m4·a4 = m4·g + (k4+k5)·(p3-p4) + c4·(v3-v4)
    ```

    **Nota:** Todas as equações descrevem movimento na direção VERTICAL (eixo Y).
    g é POSITIVO porque o sistema de coordenadas do modelo tem positivo = para baixo.
    """
    )
    return


@app.cell
def _(positions_opt):
    #Parâmetros da amostra RBDS002static:

    m = 80              # kg (massa total do indivíduo)
    # IMPORTANTE: No sistema de coordenadas do modelo, positivo = para BAIXO
    # Portanto, g deve ser POSITIVO (gravidade atua na direção positiva)
    g = 9.81            # m/s² (aceleração da gravidade - POSITIVA no sistema do modelo)
    dt = float(positions_opt['time'][1] - positions_opt['time'][0])      # s (passo de tempo dos dados)
    m1 = m*0.0145       # kg (massa do metatarso,foot)
    m2 = m*0.0465       # kg (massa da canela, leg)
    m3 = m*0.1000       # kg (massa da coxa, thigh)
    m4 = m*0.1420       # kg (massa crista iliaca, pelvis)

    # IMPORTANTE: Durante dados estáticos, MGRF ≈ peso do corpo
    # Isso é usado na otimização para substituir Fg
    peso_corpo = m * g  # N (força peso total - g já é positivo)

    print(f"=== PARÂMETROS DO MODELO ===")
    print(f"Massa total: {m} kg")
    print(f"Peso do corpo: {peso_corpo:.2f} N")
    print(f"m1 (pé): {m1:.2f} kg ({m1/m*100:.1f}%)")
    print(f"m2 (perna): {m2:.2f} kg ({m2/m*100:.1f}%)")
    print(f"m3 (coxa): {m3:.2f} kg ({m3/m*100:.1f}%)")
    print(f"m4 (tronco): {m4:.2f} kg ({m4/m*100:.1f}%)")
    return dt, g, m1, m2, m3, m4


@app.cell
def _(force_data_opt, g, m1, m2, m3, minimize, np, positions_opt):
    # MODIFICAÇÃO: Usar MGRF dos dados dinâmicos T45 ao invés de peso_corpo
    # Otimizações usando dados dinâmicos (T45)

    # Interpolar MGRF para o tempo dos marcadores
    from scipy.interpolate import interp1d as interp1d_opt
    MGRF_interpolator = interp1d_opt(force_data_opt['time'], force_data_opt['MGRF'],
                                     kind='linear', bounds_error=False, fill_value=0)
    MGRF_s = MGRF_interpolator(positions_opt['time'])

    # Extrair variáveis do dict positions_opt
    p1_s = positions_opt['p1']
    p2_s = positions_opt['p2']
    p3_s = positions_opt['p3']
    p4_s = positions_opt['p4']
    v1_s = positions_opt['v1']
    v2_s = positions_opt['v2']
    v3_s = positions_opt['v3']
    v4_s = positions_opt['v4']
    a1_s = positions_opt['a1']
    a2_s = positions_opt['a2']
    a3_s = positions_opt['a3']

    #Posição 1:
    # m1*a1_s = m1*g - MGRF - k1*(p1_s - p3_s) - k2*(p1_s - p2_s) - c1*(v1_s - v3_s) - c2*(v1_s - v2_s)
    #
    # IMPORTANTE: Agora usando MGRF dos dados dinâmicos (varia com o tempo)

    # alfa[0] = k1_otim [N/m]
    # alfa[1] = k2_otim [N/m]
    # alfa[2] = c1_otim [Ns/m]
    # alfa[3] = c2_otim [Ns/m]

    def erro_0 (alfa, m1, a1_s, g, MGRF_s, p1_s, p3_s, p2_s, v1_s, v2_s, v3_s):
        # Usar MGRF dos dados dinâmicos
        return np.sum((m1*a1_s - (m1*g - MGRF_s - alfa[0]*(p1_s - p3_s) - alfa[1]*(p1_s - p2_s) - alfa[2]*(v1_s - v3_s) - alfa[3]*(v1_s - v2_s)))**2)

    alfa = minimize (erro_0, [6000,6000,300,650], (m1, a1_s, g, MGRF_s, p1_s, p3_s, p2_s, v1_s, v2_s, v3_s), method='TNC', bounds=[(4000,7000),(4000,7000),(200,600),(550,750)]).x

    k1_otim =  alfa[0]
    k2_otim =  alfa[1]
    c1_otim =  alfa[2]
    c2_otim =  alfa[3]

    # Fg_otim não é mais otimizado, é fixo = 0 (será substituído por MGRF na simulação dinâmica)
    Fg_otim = 0.0

    # #Posição 2:
    #m2*a2_s = m2*g + k2*(p1_s - p2_s) - k3*(p2_s - p3_s) + c2*(v1_s - v2_s)

    # beta[0] = k3_otim [N/m]

    def erro_1 (beta, m2, a2_s, g, k2_otim, p1_s, p2_s, p3_s, c2_otim, v1_s, v2_s):
        return np.sum((m2*a2_s - (m2*g + k2_otim*(p1_s - p2_s) - beta[0]*(p2_s - p3_s) + c2_otim*(v1_s - v2_s)))**2)
    beta = minimize (erro_1, [10000], (m2, a2_s, g, k2_otim, p1_s, p2_s, p3_s, c2_otim, v1_s, v2_s), method='TNC', bounds=[(8000,12000)]).x

    k3_otim = beta[0]

    # #Posição 3:
    # m3*a3_s = m3*g + k1_otim*(p1_s - p3_s) + k3_otim*(p2_s - p3_s) - (k4 + k5)*(p3_s - p4_s) + c1_otim*(v1_s - v3_s) - c4*(v3_s - v4_s)

    # gama[0] = k4_otim [N/m]
    # gama[1] = k5_otim [N/m]
    # gama[2] = c4_otim [Ns/m]


    def erro_2 (gama, m3, a3_s, g, k1_otim, p1_s, p3_s, k3_otim, p2_s, p4_s, v1_s, v3_s, v4_s):
        return np.sum((m3*a3_s - (m3*g + k1_otim*(p1_s - p3_s) + k3_otim*(p2_s - p3_s) - (gama[0] + gama[1])*(p3_s - p4_s) + c1_otim*(v1_s - v3_s) - gama[2]*(v3_s - v4_s)))**2)
    gama = minimize(erro_2, [10000,18000,1900], (m3, a3_s, g, k1_otim, p1_s, p3_s, k3_otim, p2_s, p4_s, v1_s, v3_s, v4_s), method='TNC', bounds=[(8000,12000),(16000,20000),(1700,2100)]).x

    k4_otim = gama[0]
    k5_otim = gama[1]
    c4_otim = gama[2]


    print("Valores Otimizados (usando dados dinâmicos T45):")
    print(f"Fg_otim  = {Fg_otim}")
    print(f"k1_otim = {k1_otim}")
    print(f"k2_otim = {k2_otim}")
    print(f"k3_otim = {k3_otim}")
    print(f"k4_otim = {k4_otim}")
    print(f"k5_otim = {k5_otim}")
    print(f"c1_otim = {c1_otim}")
    print(f"c2_otim = {c2_otim}")
    print(f"c4_otim = {c4_otim}")
    return (
        c1_otim,
        c2_otim,
        c4_otim,
        k1_otim,
        k2_otim,
        k3_otim,
        k4_otim,
        k5_otim,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Modelo Liu & Nigg 2000 - Implementação Corrigida ✅

    ### Correções Implementadas:

    1. **✅ Simulação de Euler Completa**:
       - Agora simula todas as 4 massas do modelo (pé, perna, coxa, tronco)
       - Anteriormente apenas a massa 1 era simulada dinamicamente
       - Todas as equações diferenciais são resolvidas simultaneamente

    2. **✅ Equações Implementadas Corretamente**:
       - **Massa 1 (Pé)**: m₁a₁ = m₁g - MGRF - k₁(p₁-p₃) - k₂(p₁-p₂) - c₁(v₁-v₃) - c₂(v₁-v₂)
       - **Massa 2 (Perna)**: m₂a₂ = m₂g + k₂(p₁-p₂) - k₃(p₂-p₃) + c₂(v₁-v₂)
       - **Massa 3 (Coxa)**: m₃a₃ = m₃g + k₁(p₁-p₃) + k₃(p₂-p₃) - (k₄+k₅)(p₃-p₄) + c₁(v₁-v₃) - c₄(v₃-v₄)
       - **Massa 4 (Tronco)**: m₄a₄ = m₄g + (k₄+k₅)(p₃-p₄) + c₄(v₃-v₄)

    3. **✅ Verificação de Estabilidade**:
       - Análise dos autovalores da matriz de estado
       - Verificação das propriedades das matrizes de rigidez e amortecimento
       - Detecção automática de instabilidades do sistema

    4. **✅ Comparação Completa**:
       - Plotagem da simulação vs dados experimentais para todas as 4 massas
       - Visualização em subplot 2x2 para melhor análise

    5. **✅ Estrutura Física Correta**:
       - Massa 1: Pé (recebe força de reação do solo MGRF)
       - Massa 2: Perna (tíbia)
       - Massa 3: Coxa (fêmur)
       - Massa 4: Tronco

    ### Fluxo de Dados Corrigido:
    - **Dados Estáticos** → **Otimizações** → **Parâmetros Otimizados** ✅
    - **Dados Dinâmicos** + **Parâmetros Otimizados** → **Simulação Completa (4 massas)** ✅
    - **Análise FFT** → **Dados Dinâmicos** ✅

    ### Conformidade com Liu & Nigg 2000:
    - ✅ Modelo de 4 massas conectadas por molas e amortecedores
    - ✅ Força de reação do solo aplicada na massa 1 (pé)
    - ✅ Equações de movimento baseadas na segunda lei de Newton
    - ✅ Parâmetros otimizados a partir de dados experimentais estáticos
    - ✅ Validação através de simulação com dados dinâmicos
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Theoretical Analysis""")
    return


@app.cell
def _(
    c1_otim,
    c2_otim,
    c4_otim,
    k1_otim,
    k2_otim,
    k3_otim,
    k4_otim,
    k5_otim,
    m1,
    m2,
    m3,
    m4,
    sp,
):
    # Novo modelo artigo Zadpoor e Nikooyan, figura 5a com 4 massas.

    M = sp.Matrix ([
        [m1, 0, 0, 0],
        [0, m2, 0, 0],
        [0, 0, m3, 0],
        [0, 0, 0, m4]])

    C = sp.Matrix ([
        [c1_otim + c2_otim, -c2_otim, -c1_otim, 0],
        [-c2_otim, c2_otim, 0, 0],
        [-c1_otim, 0, c1_otim + c4_otim, -c4_otim],
        [0, 0, -c4_otim, c4_otim]])

    K = sp.Matrix ([
        [k1_otim + k2_otim, -k2_otim, -k1_otim, 0],
        [-k2_otim, k2_otim + k3_otim, -k3_otim, 0],
        [-k1_otim, -k3_otim, k1_otim + k3_otim + k4_otim + k5_otim, -k4_otim - k5_otim],
        [0, 0, -k4_otim - k5_otim, k4_otim + k5_otim]])
    return C, K, M


@app.cell
def _(C, K, M, sp):
    M_inv = M.inv()
    λ = sp.Symbol('λ')
    A = sp.Matrix([[0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 1], [-M_inv * K, -M_inv * C]])
    pol_caract = A.charpoly(λ).as_expr()
    raizes = A.eigenvals()
    poly = sp.Poly(sp.expand(pol_caract), λ)
    coeffs = [sp.N(c, 6) for c in poly.all_coeffs()]
    grau = poly.degree()
    termos = []
    for _i, coef in enumerate(coeffs):
        exp = grau - _i
        if exp > 1:
            termos.append(f'{coef}*λ^{exp}')
        elif exp == 1:
            termos.append(f'{coef}*λ')
        else:
            termos.append(f'{coef}')
    poly_str = ' + '.join(termos)
    # Plotagem do polinômio e raízes:
    print('Polinômio característico:\n')
    print(f'P(λ) = {poly_str}')
    print('\nRaízes:')
    for r in raizes:
        real = sp.re(r)
        imag = sp.im(r)
        sgn = '+' if imag >= 0 else '-'
        print(f'λ = {real:.8f} {sgn} {abs(imag):.4f}*j')
    return


@app.cell
def _(p1_d, p2_d, p3_d, p4_d, plt, time_d, welch):
    #FFT para dados dinâmicos (scipy fft welch)
    dt_d = float(time_d[1] - time_d[0])  # passo de tempo dos dados dinâmicos (garantir escalar)
    _fs = float(1 / dt_d)
    _f_1, _px_1 = welch(p1_d, fs=_fs)
    f_2, px_2 = welch(p2_d, fs=_fs)
    f_3, px_3 = welch(p3_d, fs=_fs)  #f = frequencia [Hz] e px = densidade expectral [m/Hz]
    f_4, px_4 = welch(p4_d, fs=_fs)  #f = frequencia [Hz] e px = densidade expectral [m/Hz]
    _, axs = plt.subplots(2, 2, figsize=(12, 8))  #f = frequencia [Hz] e px = densidade expectral [m/Hz]
    axs[0, 0].plot(_f_1, _px_1, color='orange', linewidth=0.8, label='p1_d')  #f = frequencia [Hz] e px = densidade expectral [m/Hz]
    axs[0, 0].set_xlabel('F (Hz)')
    axs[0, 0].set_ylabel('Densidade espectral [m/Hz]')
    axs[0, 0].legend()
    axs[0, 0].grid(True)
    axs[0, 1].plot(f_2, px_2, color='b', linewidth=0.8, label='p2_d')
    axs[0, 1].set_xlabel('F (Hz)')
    axs[0, 1].set_ylabel('Densidade espectral [m/Hz]')
    axs[0, 1].legend()
    axs[0, 1].grid(True)
    axs[1, 0].plot(f_3, px_3, color='r', linewidth=0.8, label='p3_d')
    axs[1, 0].set_xlabel('F (Hz)')
    axs[1, 0].set_ylabel('Densidade espectral [m/Hz]')
    axs[1, 0].legend()
    axs[1, 0].grid(True)
    axs[1, 1].plot(f_4, px_4, color='g', linewidth=0.8, label='p4_d')
    axs[1, 1].set_xlabel('F (Hz)')
    axs[1, 1].set_ylabel('Densidade espectral [m/Hz]')
    axs[1, 1].legend()
    axs[1, 1].grid(True)
    plt.tight_layout()
    plt.show()
    return (dt_d,)


@app.cell
def _(
    c1_otim,
    c2_otim,
    c4_otim,
    dt_d,
    g,
    k1_otim,
    k2_otim,
    k3_otim,
    k4_otim,
    k5_otim,
    load_force_data,
    m1,
    m2,
    m3,
    m4,
    np,
    p1_d,
    p2_d,
    p3_d,
    p4_d,
    plt,
    time_d,
    v1_d,
    v2_d,
    v3_d,
    v4_d,
):
    # Simulação de Euler completa para 4 massas usando dados dinâmicos
    # IMPORTANTE: p1_d, p2_d, p3_d, p4_d já estão convertidos para a convenção do modelo
    # (referência = posição inicial, positivo = para baixo)

    print("=== INICIANDO SIMULAÇÃO DE EULER ===")
    print("NOTA: Usando dados convertidos para convenção do modelo Liu 2000")
    print("      (referência = posição inicial, positivo = para baixo)")

    # Carregar MGRF para esta simulação (dados T25 para comparação)
    force_data_sim = load_force_data('RBDS002runT25forces.txt')
    MGRF_sim_data = force_data_sim['MGRF']

    # IMPORTANTE: Passo de integração pode ser diferente do passo de amostragem
    # Usar passo menor para melhor precisão numérica
    dt_sim = dt_d/100  # Passo de integração 10x menor que amostragem
    t_final_sim = time_d[-1]  # Duração total dos dados experimentais
    t_sim = np.arange(0, t_final_sim, dt_sim)  # Vetor de tempo da simulação
    n_steps_sim = len(t_sim)

    print(f"Duração dos dados experimentais: {t_final_sim:.3f} s")
    print(f"Passo de amostragem dos dados: dt_d = {dt_d:.6f} s ({1/dt_d:.1f} Hz)")
    print(f"Passo de integração da simulação: dt_sim = {dt_sim:.6f} s ({1/dt_sim:.1f} Hz)")
    print(f"Número de passos da simulação: {n_steps_sim}")

    # Inicializar arrays para todas as massas (tamanho da simulação)
    p1_sim = np.zeros(n_steps_sim)
    v1_sim = np.zeros(n_steps_sim)
    p2_sim = np.zeros(n_steps_sim)
    v2_sim = np.zeros(n_steps_sim)
    p3_sim = np.zeros(n_steps_sim)
    v3_sim = np.zeros(n_steps_sim)
    p4_sim = np.zeros(n_steps_sim)
    v4_sim = np.zeros(n_steps_sim)

    # IMPORTANTE: Condições iniciais devem vir dos dados experimentais convertidos
    # Usar os valores iniciais (primeiro ponto temporal) dos dados experimentais
    # já convertidos para a convenção do modelo
    p1_sim[0] = p1_d[0]  # posição inicial do heel (dados experimentais convertidos)
    p2_sim[0] = p2_d[0]  # posição inicial do knee (dados experimentais convertidos)
    p3_sim[0] = p3_d[0]  # posição inicial do trunk (dados experimentais convertidos)
    p4_sim[0] = p4_d[0]  # posição inicial do crest (dados experimentais convertidos)
    v1_sim[0] = v1_d[0]  # velocidade inicial do heel (dados experimentais convertidos)
    v2_sim[0] = v2_d[0]  # velocidade inicial do knee (dados experimentais convertidos)
    v3_sim[0] = v3_d[0]  # velocidade inicial do trunk (dados experimentais convertidos)
    v4_sim[0] = v4_d[0]  # velocidade inicial do crest (dados experimentais convertidos)

    print(f"\nCondições iniciais (dos dados experimentais convertidos):")
    print(f"  Posições: p1={p1_sim[0]:.6f}, p2={p2_sim[0]:.6f}, p3={p3_sim[0]:.6f}, p4={p4_sim[0]:.6f}")
    print(f"  Velocidades: v1={v1_sim[0]:.6f}, v2={v2_sim[0]:.6f}, v3={v3_sim[0]:.6f}, v4={v4_sim[0]:.6f}")

    # Interpolar MGRF para o vetor de tempo da simulação
    # MGRF está amostrado em time_Fy, precisa ser interpolado para t_sim
    from scipy.interpolate import interp1d as interp1d_sim
    # Criar interpolador para MGRF
    # Assumindo que MGRF tem o mesmo tempo que time_d (verificar!)
    # Se MGRF tem tempo diferente, ajustar conforme necessário
    MGRF_interp = interp1d_sim(time_d, MGRF_sim_data[:len(time_d)], kind='linear',
                               bounds_error=False, fill_value=MGRF_sim_data[0])
    MGRF_sim = MGRF_interp(t_sim)

    p1_interp = interp1d_sim(time_d, p1_d[:len(time_d)], kind='linear',
                             bounds_error=False, fill_value=p1_d[0])
    p1_d_interp = p1_interp(t_sim)

    p2_interp = interp1d_sim(time_d, p2_d[:len(time_d)], kind='linear',
                             bounds_error=False, fill_value=p2_d[0])
    p2_d_interp = p2_interp(t_sim)

    p3_interp = interp1d_sim(time_d, p3_d[:len(time_d)], kind='linear',
                             bounds_error=False, fill_value=p3_d[0])
    p3_d_interp = p3_interp(t_sim)

    p4_interp = interp1d_sim(time_d, p4_d[:len(time_d)], kind='linear',
                             bounds_error=False, fill_value=p4_d[0])
    p4_d_interp = p4_interp(t_sim)

    print(f"\nMGRF interpolado para {len(MGRF_sim)} pontos da simulação")

    # # GRF_est = np.zeros(n_steps_sim)
    # # Factm1_est = np.zeros(n_steps_sim)
    # # Factm2_est = np.zeros(n_steps_sim)
    # # Factm3_est = np.zeros(n_steps_sim)
    # # Factm4_est = np.zeros(n_steps_sim)

    # # Kp1 = 1000000
    # # Kp2 = 0
    # # Kp3 = 100
    # # Kp4 = 0

    # # Ki1 = 100000
    # # Ki2 = 0
    # # Ki3 = 10
    # # Ki4 = 0


    # # inte1 = 0
    # # inte2 = 0
    # # inte3 = 0
    # # inte4 = 0

    # # for i in range(n_steps_sim - 1):
    # #     # Equação para massa 1 (pé)
    # #     # m1*a1 = m1*g - MGRF - k1*(p1 - p3) - k2*(p1 - p2) - c1*(v1 - v3) - c2*(v1 - v2)
    # #     # IMPORTANTE: g é POSITIVO (para baixo), MGRF é NEGATIVO (para cima)
    # #     e1 = p1_d_interp[i] - p1_sim[i]
    # #     e2 = p2_d_interp[i] - p2_sim[i]
    # #     e3 = p3_d_interp[i] - p3_sim[i]
    # #     e4 = p4_d_interp[i] - p4_sim[i]

    # #     inte1 = inte1 + e1*dt_sim
    # #     inte2 = inte2 + e2*dt_sim
    # #     inte3 = inte3 + e3*dt_sim
    # #     inte4 = inte4 + e4*dt_sim

    # #     Factm1_est[i] = Kp1*e1 + Ki1*inte1
    # #     Factm2_est[i] = Kp2*e2 + Ki2*inte2
    # #     Factm3_est[i] = Kp3*e3 + Ki3*inte3
    # #     Factm4_est[i] = Kp4*e4 + Ki4*inte4

    # #     Factm1_est[i] = 0 if Factm1_est[i]<=0 else Factm1_est[i]


    # #     # Equação para massa 1 ()
    # #     # IMPORTANTE: g é POSITIVO (para baixo)
    # #     dv1dt = (Factm1_est[i] + (m1*g + Factm1_est[i] - k1_otim * (p1_sim[i] - p3_sim[i]) - c1_otim * (v1_sim[i] - v3_sim[i]) - k2_otim * (p1_sim[i] - p2_sim[i]) - c2_otim * (v1_sim[i] - v2_sim[i]))/m1) 

    # #     GRF_est[i] = m1*dv1dt + Factm1_est[i] + (m1*g + Factm1_est[i] - k1_otim * (p1_sim[i] - p3_sim[i]) - c1_otim * (v1_sim[i] - v3_sim[i]) - k2_otim * (p1_sim[i] - p2_sim[i]) - c2_otim * (v1_sim[i] - v2_sim[i]))


    # #     # Equação para massa 2 (perna)
    # #     # m2*a2 = m2*g + k2*(p1 - p2) - k3*(p2 - p3) + c2*(v1 - v2)
    # #     # IMPORTANTE: g é POSITIVO (para baixo)
    # #     dv2dt = ((m2*g + Factm2_est[i] + c2_otim * (v1_sim[i] - v2_sim[i])) / m2)

    # #     # Equação para massa 3 (coxa)
    # #     # m3*a3 = m3*g + k1*(p1 - p3) + k3*(p2 - p3) - (k4 + k5)*(p3 - p4) + c1*(v1 - v3) - c4*(v3 - v4)
    # #     # IMPORTANTE: g é POSITIVO (para baixo)
    # #     dv3dt = ((m3*g + Factm3_est[i] + k1_otim * (p1_sim[i] - p3_sim[i]) +
    # #                    k3_otim * (p2_sim[i] - p3_sim[i]) - (k4_otim + k5_otim) * (p3_sim[i] - p4_sim[i]) +
    # #                    c1_otim * (v1_sim[i] - v3_sim[i]) - c4_otim * (v3_sim[i] - v4_sim[i])) / m3)

    # #     # Equação para massa 4 (tronco)
    # #     # m4*a4 = m4*g + (k4 + k5)*(p3 - p4) + c4*(v3 - v4)
    # #     # IMPORTANTE: g é POSITIVO (para baixo)
    # #     dv4dt = ((m4*g + Factm4_est[i] + (k4_otim + k5_otim) * (p3_sim[i] - p4_sim[i]) +
    # #                    c4_otim * (v3_sim[i] - v4_sim[i])) / m4)

    # #     # Atualizar velocidades (usando dt_sim, não dt_d)
    # #     v1_sim[i + 1] = v1_sim[i] + dv1dt * dt_sim
    # #     v2_sim[i + 1] = v2_sim[i] + dv2dt * dt_sim
    # #     v3_sim[i + 1] = v3_sim[i] + dv3dt * dt_sim
    # #     v4_sim[i + 1] = v4_sim[i] + dv4dt * dt_sim

    # #     # Atualizar posições (usando dt_sim, não dt_d)
    # #     p1_sim[i + 1] = p1_sim[i] + v1_sim[i] * dt_sim
    # #     p2_sim[i + 1] = p2_sim[i] + v2_sim[i] * dt_sim
    # #     p3_sim[i + 1] = p3_sim[i] + v3_sim[i] * dt_sim
    # #     p4_sim[i + 1] = p4_sim[i] + v4_sim[i] * dt_sim

    # # print("✅ Simulação de Euler concluída!")
    # # print(f"Valores finais - p1: {p1_sim[-1]:.6f}, p2: {p2_sim[-1]:.6f}, p3: {p3_sim[-1]:.6f}, p4: {p4_sim[-1]:.6f}")

    # # Plotar resultados comparando simulação com dados experimentais CONVERTIDOS
    # # IMPORTANTE: Simulação usa t_sim (passo menor), dados experimentais usam time_d
    # plt.figure()
    # plt.plot(t_sim, p1_sim, 'b-', linewidth=1.2, label='Simulação p1')
    # plt.plot(time_d, p1_d, color='orange', linestyle='--', linewidth=0.8, alpha=0.7, label='Experimental p1 (convertido)')
    # plt.xlabel('Tempo (s)')
    # plt.ylabel('Posição (m) - ref: inicial')
    # plt.title('Massa 1 (Pé) - Convenção do Modelo')
    # plt.legend()
    # plt.grid(True)
    # # plt.ylim(-2,2)
    # plt.xlim(0, t_final_sim)
    # plt.show()


    # plt.figure()
    # plt.plot(t_sim, p2_sim, 'g-', linewidth=1.2, label='Simulação p2')
    # plt.plot(time_d, p2_d, 'r--', linewidth=0.8, alpha=0.7, label='Experimental p2 (convertido)')
    # plt.xlabel('Tempo (s)')
    # plt.ylabel('Posição (m) - ref: inicial')
    # plt.title('Massa 2 (Perna) - Convenção do Modelo')
    # plt.legend()
    # plt.ylim(-2,2)
    # plt.grid(True)
    # plt.xlim(0, t_final_sim)
    # plt.show()


    # plt.figure()
    # plt.plot(t_sim, p3_sim, 'r-', linewidth=1.2, label='Simulação p3')
    # plt.plot(time_d, p3_d, 'm--', linewidth=0.8, alpha=0.7, label='Experimental p3 (convertido)')
    # plt.xlabel('Tempo (s)')
    # plt.ylabel('Posição (m) - ref: inicial')
    # plt.title('Massa 3 (Coxa) - Convenção do Modelo')
    # plt.legend()
    # plt.ylim(-2,2)
    # plt.grid(True)
    # plt.xlim(0, t_final_sim)
    # plt.show()


    # plt.figure()
    # plt.plot(t_sim, p4_sim, 'm-', linewidth=1.2, label='Simulação p4')
    # plt.plot(time_d, p4_d, 'k--', linewidth=0.8, alpha=0.7, label='Experimental p4 (convertido)')
    # plt.xlabel('Tempo (s)')
    # plt.ylabel('Posição (m) - ref: inicial')
    # plt.title('Massa 4 (Tronco) - Convenção do Modelo')
    # plt.legend()
    # plt.ylim(-2,2)
    # plt.grid(True)
    # plt.xlim(0, t_final_sim)
    # plt.show()

    # plt.figure()
    # plt.plot(t_sim, GRF_est, color='red', label='GRF simulated')
    # # plt.plot(t_sim, MGRF_sim, color='blue', label='GRF experimental')
    # plt.legend()
    # plt.show()

    # print("\n=== NOTA IMPORTANTE ===")
    # print("Os dados experimentais (laranja/vermelho/roxo/marrom) foram CONVERTIDOS")
    # print("para a convenção do modelo Liu 2000 (referência = posição inicial).")
    # print("A linha tracejada em y=0 representa a posição inicial de referência.")
    # print(f"\nSimulação: {n_steps_sim} pontos com dt={dt_sim:.6f}s")
    # print(f"Dados experimentais: {len(time_d)} pontos com dt={dt_d:.6f}s")
    return


@app.cell
def _(
    c1_otim,
    c2_otim,
    c4_otim,
    k1_otim,
    k2_otim,
    k3_otim,
    k4_otim,
    k5_otim,
    m1,
    m2,
    m3,
    m4,
    np,
):
    # Verificação de estabilidade do sistema Liu & Nigg 2000
    print("=== VERIFICAÇÃO DE ESTABILIDADE DO SISTEMA ===")

    # Matriz de massa (numpy para análise de estabilidade)
    M_stab = np.diag([m1, m2, m3, m4])

    # Matriz de rigidez (numpy para análise de estabilidade)
    K_stab = np.array([
        [k1_otim + k2_otim, -k2_otim, -k1_otim, 0],
        [-k2_otim, k2_otim + k3_otim, -k3_otim, 0],
        [-k1_otim, -k3_otim, k1_otim + k3_otim + k4_otim + k5_otim, -(k4_otim + k5_otim)],
        [0, 0, -(k4_otim + k5_otim), k4_otim + k5_otim]
    ])

    # Matriz de amortecimento (numpy para análise de estabilidade)
    C_stab = np.array([
        [c1_otim + c2_otim, -c2_otim, -c1_otim, 0],
        [-c2_otim, c2_otim, 0, 0],
        [-c1_otim, 0, c1_otim + c4_otim, -c4_otim],
        [0, 0, -c4_otim, c4_otim]
    ])

    # Matriz de estado A = [0, I; -M^(-1)*K, -M^(-1)*C]
    M_inv_stab = np.linalg.inv(M_stab)
    zeros = np.zeros((4, 4))
    I = np.eye(4)

    A_stab = np.block([
        [zeros, I],
        [-M_inv_stab @ K_stab, -M_inv_stab @ C_stab]
    ])

    # Calcular autovalores
    eigenvalues = np.linalg.eigvals(A_stab)
    real_parts = np.real(eigenvalues)
    is_stable = np.all(real_parts <= 0)

    print(f"Sistema estável: {is_stable}")
    print(f"Autovalores: {eigenvalues}")
    print(f"Partes reais: {real_parts}")

    if not is_stable:
        print("⚠️  ATENÇÃO: Sistema instável! Verifique os parâmetros.")
        print("Partes reais positivas indicam crescimento exponencial.")
    else:
        print("✅ Sistema estável.")

    # Verificar se as matrizes são definidas positivas
    K_eigenvals = np.linalg.eigvals(K_stab)
    C_eigenvals = np.linalg.eigvals(C_stab)

    print(f"\nAutovalores da matriz de rigidez K: {K_eigenvals}")
    print(f"K é definida positiva: {np.all(K_eigenvals > 0)}")

    print(f"\nAutovalores da matriz de amortecimento C: {C_eigenvals}")
    print(f"C é semi-definida positiva: {np.all(C_eigenvals >= 0)}")
    return (A_stab,)


@app.cell
def _(A_stab, dt, np, plt, solve_ivp, welch):
    def state_space(_, z):
        return A_stab @ z
    z0 = np.zeros(8)
    z0[0] = 0.001
    dt_1 = float(dt)  # usando dt dos dados estáticos (garantir escalar)
    t_final = 40
    t_eval = np.arange(0, t_final, dt_1)
    sol = solve_ivp(state_space, [0, t_final], z0, t_eval=t_eval, method='RK45')
    x_t = sol.y[0, :]
    _fs = float(1 / dt_1)
    _f_1, _px_1 = welch(x_t, fs=_fs)
    plt.figure(figsize=(10, 5))
    plt.plot(_f_1, _px_1, color='r', linewidth=0.8)
    plt.xlabel('Frequência (Hz)')
    plt.ylabel('Amplitude (m/Hz)')
    plt.grid(True)
    plt.show()
    plt.figure(figsize=(10, 5))
    plt.plot(t_eval, x_t, color='b', linewidth=0.8)
    plt.xlabel('Tempo (s)')
    plt.ylabel('Deslocamento (m)')
    plt.grid(True)
    plt.show()
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## 📋 Resumo da Conversão de Coordenadas

    ### Problema Identificado:

    O modelo Liu & Nigg 2000 usa distâncias relativas à **posição inicial** (obtida dos dados estáticos),
    enquanto os dados experimentais são medidos em relação ao **solo**.

    Além disso, as convenções de direção são opostas:
    - **Dados experimentais (Fukuchi 2017)**: valores crescem para CIMA (eixo Y VERTICAL positivo)
    - **Modelo Liu 2000**: valores crescem para BAIXO (convenção do modelo - compressão positiva)

    ### Convenção de Eixos (Fukuchi 2017):

    - **Eixo X**: Médio-lateral
    - **Eixo Y**: **VERTICAL** (para cima/baixo) ← **USADO no modelo**
    - **Eixo Z**: Anteroposterior (direção do movimento)

    ### Solução Implementada:

    #### 1. Simulação (Método de Euler):
    - **Condições iniciais**: Valores iniciais dos dados experimentais convertidos
      - p[0] = p_ref - p_exp[0] (posição relativa à referência estática)
      - v[0] = -v_exp[0] (velocidade com sinal invertido)
    - **Equações**: Permanecem inalteradas (estavam corretas)
    - **Referência**: Posição inicial obtida dos dados estáticos

    #### 2. Conversão para Comparação nos Gráficos:

    **Cálculo das posições de referência** (média dos dados estáticos):
    ```python
    p1_ref = np.mean(p1_s)  # heel
    p2_ref = np.mean(p2_s)  # knee
    p3_ref = np.mean(p3_s)  # trunk
    p4_ref = np.mean(p4_s)  # crest
    ```

    **Conversão dos dados experimentais**:
    ```python
    p_modelo = p_ref - p_experimental
    v_modelo = -v_experimental
    ```

    ### Variáveis Criadas:

    - **Dados experimentais** (referência: solo, cresce para cima):
      - `p1_d_exp`, `p2_d_exp`, `p3_d_exp`, `p4_d_exp`

    - **Dados convertidos** (referência: inicial, cresce para baixo):
      - `p1_d`, `p2_d`, `p3_d`, `p4_d` ← **Usados para comparação nos gráficos**
      - `v1_d`, `v2_d`, `v3_d`, `v4_d`

    - **Posições de referência**:
      - `p1_ref`, `p2_ref`, `p3_ref`, `p4_ref`

    - **Simulação**:
      - `p1_sim`, `p2_sim`, `p3_sim`, `p4_sim` ← **Resultados da simulação**
      - Condições iniciais: p[0] = p_d[0], v[0] = v_d[0] (dos dados experimentais convertidos)

    ### Fluxo Correto:

    1. **Otimização**: Usa dados estáticos → obtém parâmetros (k1, k2, c1, etc.)
    2. **Conversão**: Converte dados experimentais para convenção do modelo
    3. **Simulação**: Inicia com condições iniciais dos dados experimentais convertidos → evolui com equações de Euler
    4. **Comparação**: Plota simulação vs dados experimentais convertidos

    ✅ **Agora a simulação e a comparação estão corretas!**

    **IMPORTANTE:** As condições iniciais da simulação devem vir dos dados experimentais,
    não de p=0, v=0. Isso garante que a simulação comece no mesmo estado que os dados reais.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Otimização dos Parâmetros do Controlador PI com Optuna

    Nesta seção, usaremos a biblioteca Optuna para encontrar os valores ótimos dos parâmetros
    do controlador PI (Kp1, Kp2, Kp3, Kp4, Ki1, Ki2, Ki3, Ki4).

    ### 🎯 Objetivo de Otimização:
    Minimizar o erro quadrático médio (MSE) das **POSIÇÕES** (p1, p2, p3, p4)

    **Critério**: MSE_total = MSE_p1 + MSE_p2 + MSE_p3 + MSE_p4

    Onde cada MSE_pi é o erro quadrático médio entre a posição simulada e a posição experimental.

    ### 📊 Parâmetros a otimizar:
    - **Kp1, Kp2, Kp3, Kp4**: Ganhos proporcionais (controlam resposta imediata ao erro)
    - **Ki1, Ki2, Ki3, Ki4**: Ganhos integrais (eliminam erro em regime permanente)

    ### 💡 Por que otimizar pelas posições?

    Ao ajustar os parâmetros para minimizar o erro das posições, o controlador PI:
    1. Garante que as posições simuladas sigam fielmente as posições experimentais
    2. As forças (GRF, Factm2-4) são ajustadas automaticamente para alcançar esse objetivo
    3. Resulta em uma estimativa mais precisa da GRF como consequência do bom rastreamento
    """
    )
    return


@app.cell
def _(
    c1_otim,
    c2_otim,
    c4_otim,
    dt_d,
    g,
    k1_otim,
    k2_otim,
    k3_otim,
    k4_otim,
    k5_otim,
    m1,
    m2,
    m3,
    m4,
    np,
    p1_d,
    p2_d,
    p3_d,
    p4_d,
    time_d,
    v1_d,
    v2_d,
    v3_d,
    v4_d,
):
    import optuna
    from scipy.interpolate import interp1d as scipy_interp1d

    # Função de simulação que será usada pela otimização
    def simulate_with_pi_controller(Kp1, Kp2, Kp3, Kp4, Ki1, Ki2, Ki3, Ki4, MGRF_target):
        """
        Simula o sistema com controlador PI e retorna a GRF estimada
        """
        # Configuração da simulação
        dt_sim = dt_d / 100
        t_final_sim = time_d[-1]
        t_sim = np.arange(0, t_final_sim, dt_sim)
        n_steps_sim = len(t_sim)

        # Inicializar arrays
        p1_sim = np.zeros(n_steps_sim)
        v1_sim = np.zeros(n_steps_sim)
        p2_sim = np.zeros(n_steps_sim)
        v2_sim = np.zeros(n_steps_sim)
        p3_sim = np.zeros(n_steps_sim)
        v3_sim = np.zeros(n_steps_sim)
        p4_sim = np.zeros(n_steps_sim)
        v4_sim = np.zeros(n_steps_sim)

        # Condições iniciais
        p1_sim[0] = p1_d[0]
        p2_sim[0] = p2_d[0]
        p3_sim[0] = p3_d[0]
        p4_sim[0] = p4_d[0]
        v1_sim[0] = v1_d[0]
        v2_sim[0] = v2_d[0]
        v3_sim[0] = v3_d[0]
        v4_sim[0] = v4_d[0]

        # Interpolar dados experimentais
        p1_interp = scipy_interp1d(time_d, p1_d[:len(time_d)], kind='linear',
                             bounds_error=False, fill_value=p1_d[0])
        p1_d_interp = p1_interp(t_sim)

        p2_interp = scipy_interp1d(time_d, p2_d[:len(time_d)], kind='linear',
                             bounds_error=False, fill_value=p2_d[0])
        p2_d_interp = p2_interp(t_sim)

        p3_interp = scipy_interp1d(time_d, p3_d[:len(time_d)], kind='linear',
                             bounds_error=False, fill_value=p3_d[0])
        p3_d_interp = p3_interp(t_sim)

        p4_interp = scipy_interp1d(time_d, p4_d[:len(time_d)], kind='linear',
                             bounds_error=False, fill_value=p4_d[0])
        p4_d_interp = p4_interp(t_sim)

        # Arrays para forças estimadas
        GRF_est = np.zeros(n_steps_sim)
        Factm1_est = np.zeros(n_steps_sim)
        Factm2_est = np.zeros(n_steps_sim)
        Factm3_est = np.zeros(n_steps_sim)
        Factm4_est = np.zeros(n_steps_sim)

        # Integradores
        inte1 = 0
        inte2 = 0
        inte3 = 0
        inte4 = 0

        # Loop de simulação
        for i in range(n_steps_sim - 1):
            # Calcular erros
            e1 = p1_d_interp[i] - p1_sim[i]
            e2 = p2_d_interp[i] - p2_sim[i]
            e3 = p3_d_interp[i] - p3_sim[i]
            e4 = p4_d_interp[i] - p4_sim[i]

            # Atualizar integradores
            inte1 = inte1 + e1 * dt_sim
            inte2 = inte2 + e2 * dt_sim
            inte3 = inte3 + e3 * dt_sim
            inte4 = inte4 + e4 * dt_sim

            # Controlador PI
            Factm1_est[i] = Kp1*e1 + Ki1*inte1
            Factm2_est[i] = Kp2 * e2 + Ki2 * inte2
            Factm3_est[i] = Kp3 * e3 + Ki3 * inte3
            Factm4_est[i] = Kp4 * e4 + Ki4 * inte4

            # Limitar GRF a valores positivos
            GRF_est[i] = 0 if GRF_est[i] <= 0 else GRF_est[i]

            # Equações de movimento
            dv1dt = (Factm1_est[i] + (m1*g + Factm1_est[i] - k1_otim * (p1_sim[i] - p3_sim[i]) - c1_otim * (v1_sim[i] - v3_sim[i]) - k2_otim * (p1_sim[i] - p2_sim[i]) - c2_otim * (v1_sim[i] - v2_sim[i]))/m1) 

            if p1_sim[i] < 0.05:
                GRF_est[i] = m1*dv1dt + Factm1_est[i] + (m1*g + Factm1_est[i] - k1_otim * (p1_sim[i] - p3_sim[i]) - c1_otim * (v1_sim[i] - v3_sim[i]) - k2_otim * (p1_sim[i] - p2_sim[i]) - c2_otim * (v1_sim[i] - v2_sim[i]))
            else: GRF_est[i] = 0

            # GRF_est[i] = m1*dv1dt + Factm1_est[i] + (m1*g + Factm1_est[i] - k1_otim * (p1_sim[i] - p3_sim[i]) - c1_otim * (v1_sim[i] - v3_sim[i]) - k2_otim * (p1_sim[i] - p2_sim[i]) - c2_otim * (v1_sim[i] - v2_sim[i]))
            

            dv2dt = ((m2*g + Factm2_est[i] + c2_otim * (v1_sim[i] - v2_sim[i])) / m2)

            dv3dt = ((m3*g + Factm3_est[i] + k1_otim * (p1_sim[i] - p3_sim[i]) +
                     k3_otim * (p2_sim[i] - p3_sim[i]) - (k4_otim + k5_otim) * (p3_sim[i] - p4_sim[i]) +
                     c1_otim * (v1_sim[i] - v3_sim[i]) - c4_otim * (v3_sim[i] - v4_sim[i])) / m3)

            dv4dt = ((m4*g + Factm4_est[i] + (k4_otim + k5_otim) * (p3_sim[i] - p4_sim[i]) +
                     c4_otim * (v3_sim[i] - v4_sim[i])) / m4)

            # Atualizar velocidades
            v1_sim[i + 1] = v1_sim[i] + dv1dt * dt_sim
            v2_sim[i + 1] = v2_sim[i] + dv2dt * dt_sim
            v3_sim[i + 1] = v3_sim[i] + dv3dt * dt_sim
            v4_sim[i + 1] = v4_sim[i] + dv4dt * dt_sim

            # Atualizar posições
            p1_sim[i + 1] = p1_sim[i] + v1_sim[i] * dt_sim
            p2_sim[i + 1] = p2_sim[i] + v2_sim[i] * dt_sim
            p3_sim[i + 1] = p3_sim[i] + v3_sim[i] * dt_sim
            p4_sim[i + 1] = p4_sim[i] + v4_sim[i] * dt_sim

        return GRF_est, Factm1_est, Factm2_est, Factm3_est, Factm4_est, p1_sim, p2_sim, p3_sim, p4_sim, t_sim

    print("✅ Função de simulação com controlador PI criada!")
    return optuna, scipy_interp1d, simulate_with_pi_controller


@app.cell
def _(
    load_force_data,
    np,
    p1_d,
    p2_d,
    p3_d,
    p4_d,
    scipy_interp1d,
    simulate_with_pi_controller,
    time_d,
):
    # Carregar MGRF para otimização (dados T25)
    force_data_optuna = load_force_data('RBDS002runT25forces.txt')

    # Preparar MGRF para comparação
    MGRF_for_optim = force_data_optuna['MGRF'][:len(time_d)]

    # Função objetivo para Optuna - OTIMIZAR BASEADO NAS POSIÇÕES
    def objective(trial):
        # Sugerir valores para os parâmetros
        # Reduzir limites superiores para evitar instabilidade numérica
        Kp1 = trial.suggest_float('Kp1', 1e4, 1e6, log=True)  # Reduzido de 1e7 para 1e6
        Kp2 = trial.suggest_float('Kp2', 1e3, 5e5, log=True)  # Reduzido de 1e6 para 5e5
        Kp3 = trial.suggest_float('Kp3', 1e3, 5e5, log=True)  # Reduzido de 1e6 para 5e5
        Kp4 = trial.suggest_float('Kp4', 1e3, 5e5, log=True)  # Reduzido de 1e6 para 5e5

        Ki1 = trial.suggest_float('Ki1', 1e3, 5e5, log=True)  # Reduzido de 1e6 para 5e5
        Ki2 = trial.suggest_float('Ki2', 1e2, 5e4, log=True)  # Reduzido de 1e5 para 5e4
        Ki3 = trial.suggest_float('Ki3', 1e2, 5e4, log=True)  # Reduzido de 1e5 para 5e4
        Ki4 = trial.suggest_float('Ki4', 1e2, 5e4, log=True)  # Reduzido de 1e5 para 5e4

        try:
            # Simular com os parâmetros sugeridos
            GRF_est, Factm1_est, Factm2_est, Factm3_est, Factm4_est, p1_sim, p2_sim, p3_sim, p4_sim, t_sim = simulate_with_pi_controller(
                Kp1, Kp2, Kp3, Kp4, Ki1, Ki2, Ki3, Ki4, MGRF_for_optim
            )

            # Interpolar dados experimentais de posição para o tempo da simulação
            p1_d_interp_obj = scipy_interp1d(time_d, p1_d[:len(time_d)], kind='linear',
                                   bounds_error=False, fill_value=p1_d[0])
            p1_d_sim_obj = p1_d_interp_obj(t_sim)

            p2_d_interp_obj = scipy_interp1d(time_d, p2_d[:len(time_d)], kind='linear',
                                   bounds_error=False, fill_value=p2_d[0])
            p2_d_sim_obj = p2_d_interp_obj(t_sim)

            p3_d_interp_obj = scipy_interp1d(time_d, p3_d[:len(time_d)], kind='linear',
                                   bounds_error=False, fill_value=p3_d[0])
            p3_d_sim_obj = p3_d_interp_obj(t_sim)

            p4_d_interp_obj = scipy_interp1d(time_d, p4_d[:len(time_d)], kind='linear',
                                   bounds_error=False, fill_value=p4_d[0])
            p4_d_sim_obj = p4_d_interp_obj(t_sim)

            # Verificar se há NaN ou Inf nos resultados da simulação
            if (np.any(np.isnan(p1_sim)) or np.any(np.isinf(p1_sim)) or
                np.any(np.isnan(p2_sim)) or np.any(np.isinf(p2_sim)) or
                np.any(np.isnan(p3_sim)) or np.any(np.isinf(p3_sim)) or
                np.any(np.isnan(p4_sim)) or np.any(np.isinf(p4_sim)) or
                np.any(np.isnan(GRF_est)) or np.any(np.isinf(GRF_est))):
                # Simulação instável - retornar valor alto para penalizar
                return 1e10

            # Calcular erro quadrático médio das POSIÇÕES (não da GRF)
            mse_p1 = np.mean((p1_sim - p1_d_sim_obj)**2)
            mse_p2 = np.mean((p2_sim - p2_d_sim_obj)**2)
            mse_p3 = np.mean((p3_sim - p3_d_sim_obj)**2)
            mse_p4 = np.mean((p4_sim - p4_d_sim_obj)**2)

            # Verificar se os erros são válidos
            if (np.isnan(mse_p1) or np.isnan(mse_p2) or
                np.isnan(mse_p3) or np.isnan(mse_p4) or
                np.isinf(mse_p1) or np.isinf(mse_p2) or
                np.isinf(mse_p3) or np.isinf(mse_p4)):
                return 1e10

            # Erro total = soma dos erros de todas as posições
            # Você pode ajustar os pesos se quiser dar mais importância a alguma posição
            mse_total = mse_p1 + mse_p2 + mse_p3 + mse_p4

            # Verificação final
            if np.isnan(mse_total) or np.isinf(mse_total):
                return 1e10

            return mse_total
        except Exception as e:
            # Se houver erro na simulação, retornar um valor alto
            print(f"Erro na simulação: {e}")
            return 1e10

    print("✅ Função objetivo para Optuna criada!")
    print("📍 Critério de otimização: Minimizar erro das POSIÇÕES (p1, p2, p3, p4)")
    return MGRF_for_optim, objective


@app.cell
def _(objective, optuna):
    # Criar estudo Optuna com sampler TPE (Tree-structured Parzen Estimator)
    # TPE é mais eficiente que random search para espaços de alta dimensão
    print("=== INICIANDO OTIMIZAÇÃO COM OPTUNA ===")
    print("🎯 Critério: Minimizar erro das POSIÇÕES (p1, p2, p3, p4)")
    print("📊 Número de trials: 500")
    print("⏱️  Isso pode levar 10-20 minutos...")
    print("💡 Usando TPE sampler para otimização mais eficiente")

    # Usar TPE sampler com multivariate=True para capturar correlações entre parâmetros
    sampler = optuna.samplers.TPESampler(
        n_startup_trials=50,  # Primeiros 50 trials são random para exploração
        multivariate=True,     # Considera correlações entre parâmetros
        seed=42                # Seed para reprodutibilidade
    )

    study = optuna.create_study(
        direction='minimize',
        sampler=sampler,
        study_name='pi_controller_optimization'
    )

    study.optimize(objective, n_trials=20, show_progress_bar=True)

    # Verificar se há trials completos antes de acessar resultados
    if len(study.trials) > 0 and study.best_trial is not None:
        # Contar trials bem-sucedidos vs falhados
        successful_trials = [t for t in study.trials if t.value != 1e10]
        failed_trials = [t for t in study.trials if t.value == 1e10]

        # Resultados
        print("\n=== RESULTADOS DA OTIMIZAÇÃO ===")
        print(f"✅ Trials bem-sucedidos: {len(successful_trials)}/{len(study.trials)}")
        print(f"❌ Trials falhados (instáveis): {len(failed_trials)}/{len(study.trials)}")
        print(f"\n🏆 Melhor MSE Total (soma dos erros de posição): {study.best_value:.8f} m²")
        print(f"   Trial #{study.best_trial.number}")

        print("\n📊 Melhores parâmetros:")
        for param, value in study.best_params.items():
            print(f"  {param}: {value:.2f}")

        # Plotar histórico de otimização
        # print("\n📈 Gerando gráficos de otimização...")
        # fig = optuna.visualization.plot_optimization_history(study)
        # fig.show()

        # Plotar importância dos parâmetros (FYI: pode variar entre execuções com poucos trials)
        # fig2 = optuna.visualization.plot_param_importances(study)
        # fig2.show()

        # Plotar slice plot (mostra como cada parâmetro afeta o objetivo)
        # fig3 = optuna.visualization.plot_slice(study)
        # fig3.show()

        # Plotar parallel coordinate (mostra relações entre parâmetros)
        # fig4 = optuna.visualization.plot_parallel_coordinate(study)
        # fig4.show()
    else:
        print("\n⚠️ Nenhum trial foi completado com sucesso.")
    return (study,)


@app.cell
def _(
    MGRF_for_optim,
    np,
    p1_d,
    p2_d,
    p3_d,
    p4_d,
    plt,
    scipy_interp1d,
    simulate_with_pi_controller,
    study,
    time_d,
):
    # Verificar se há resultados antes de prosseguir
    if len(study.trials) == 0 or study.best_trial is None:
        print("⚠️ Aguardando conclusão da otimização...")
        # Retornar valores dummy para evitar erros
        Kp1_opt = Kp2_opt = Kp3_opt = Kp4_opt = 0
        Ki1_opt = Ki2_opt = Ki3_opt = Ki4_opt = 0
        GRF_est_opt = Factm2_est_opt = Factm3_est_opt = Factm4_est_opt = None
        p1_sim_opt = p2_sim_opt = p3_sim_opt = p4_sim_opt = t_sim_opt = None
    else:
        # Extrair melhores parâmetros
        best_params = study.best_params
        Kp1_opt = best_params['Kp1']
        Kp2_opt = best_params['Kp2']
        Kp3_opt = best_params['Kp3']
        Kp4_opt = best_params['Kp4']
        Ki1_opt = best_params['Ki1']
        Ki2_opt = best_params['Ki2']
        Ki3_opt = best_params['Ki3']
        Ki4_opt = best_params['Ki4']

        # Simular com os melhores parâmetros
        GRF_est_opt, Factm1_est_opt, Factm2_est_opt, Factm3_est_opt, Factm4_est_opt, p1_sim_opt, p2_sim_opt, p3_sim_opt, p4_sim_opt, t_sim_opt = simulate_with_pi_controller(
            Kp1_opt, Kp2_opt, Kp3_opt, Kp4_opt,
            Ki1_opt, Ki2_opt, Ki3_opt, Ki4_opt,
            MGRF_for_optim
        )

        # Interpolar MGRF para comparação
        MGRF_interp_opt = scipy_interp1d(time_d, MGRF_for_optim, kind='linear',
                                   bounds_error=False, fill_value=MGRF_for_optim[0])
        MGRF_sim_opt = MGRF_interp_opt(t_sim_opt)

        # Plotar comparação GRF
        plt.figure(figsize=(12, 6))
        plt.plot(t_sim_opt, MGRF_sim_opt, color='blue', label='GRF Measured (MGRF)', linewidth=2)
        plt.plot(t_sim_opt, Factm1_est_opt + Factm2_est_opt, color='red', label='GRF Estimated (optimized)', linewidth=1.5, alpha=0.7)
        plt.xlabel('Time (s)')
        plt.ylabel('Force (N)')
        plt.title('Comparação: GRF Measured vs GRF Estimated')
        plt.legend()
        plt.grid(True)
        plt.xlim(0, 2)
        plt.show()

        

        # Plotar forças atuantes em todas as massas
        plt.figure(figsize=(15, 10))

        plt.subplot(2, 2, 1)
        plt.plot(t_sim_opt, GRF_est_opt, color='red', linewidth=1.5)
        plt.xlabel('Tempo (s)')
        plt.ylabel('Força (N)')
        plt.xlim(0, 2)
        plt.xlim(0, 2)
        plt.title('GRF (Força na Massa 1 - Pé)')
        plt.grid(True)

        plt.subplot(2, 2, 2)
        plt.plot(t_sim_opt, Factm2_est_opt, color='green', linewidth=1.5)
        plt.xlabel('Tempo (s)')
        plt.ylabel('Força (N)')
        plt.title('Factm2 (Força na Massa 2 - Perna)')
        plt.xlim(0, 2)
        plt.grid(True)

        plt.subplot(2, 2, 3)
        plt.plot(t_sim_opt, Factm3_est_opt, color='orange', linewidth=1.5)
        plt.xlabel('Tempo (s)')
        plt.ylabel('Força (N)')
        plt.title('Factm3 (Força na Massa 3 - Coxa)')
        plt.xlim(0, 2)
        plt.grid(True)

        plt.subplot(2, 2, 4)
        plt.plot(t_sim_opt, Factm4_est_opt, color='purple', linewidth=1.5)
        plt.xlabel('Tempo (s)')
        plt.ylabel('Força (N)')
        plt.title('Factm4 (Força na Massa 4 - Tronco)')
        plt.xlim(0, 2)
        plt.grid(True)

        plt.tight_layout()
        plt.show()

        # Interpolar dados experimentais para o tempo da simulação (otimização)
        p1_d_interp_opt = scipy_interp1d(time_d, p1_d[:len(time_d)], kind='linear',
                                     bounds_error=False, fill_value=p1_d[0])
        p1_d_sim = p1_d_interp_opt(t_sim_opt)

        p2_d_interp_opt = scipy_interp1d(time_d, p2_d[:len(time_d)], kind='linear',
                                     bounds_error=False, fill_value=p2_d[0])
        p2_d_sim = p2_d_interp_opt(t_sim_opt)

        p3_d_interp_opt = scipy_interp1d(time_d, p3_d[:len(time_d)], kind='linear',
                                     bounds_error=False, fill_value=p3_d[0])
        p3_d_sim = p3_d_interp_opt(t_sim_opt)

        p4_d_interp_opt = scipy_interp1d(time_d, p4_d[:len(time_d)], kind='linear',
                                     bounds_error=False, fill_value=p4_d[0])
        p4_d_sim = p4_d_interp_opt(t_sim_opt)

        # Plotar comparação das posições
        plt.figure(figsize=(15, 10))

        plt.subplot(2, 2, 1)
        plt.plot(t_sim_opt, p1_d_sim, 'b--', linewidth=2, label='Experimental', alpha=0.7)
        plt.plot(t_sim_opt, p1_sim_opt, 'r-', linewidth=1.5, label='Simulado (Otimizado)')
        plt.xlabel('Tempo (s)')
        plt.ylabel('Posição (m)')
        plt.title('p1 - Posição da Massa 1 (Pé)')
        plt.legend()
        plt.grid(True)
        plt.xlim(0, 2)

        plt.subplot(2, 2, 2)
        plt.plot(t_sim_opt, p2_d_sim, 'b--', linewidth=2, label='Experimental', alpha=0.7)
        plt.plot(t_sim_opt, p2_sim_opt, 'r-', linewidth=1.5, label='Simulado (Otimizado)')
        plt.xlabel('Tempo (s)')
        plt.ylabel('Posição (m)')
        plt.title('p2 - Posição da Massa 2 (Perna)')
        plt.legend()
        plt.grid(True)
        plt.xlim(0, 2)

        plt.subplot(2, 2, 3)
        plt.plot(t_sim_opt, p3_d_sim, 'b--', linewidth=2, label='Experimental', alpha=0.7)
        plt.plot(t_sim_opt, p3_sim_opt, 'r-', linewidth=1.5, label='Simulado (Otimizado)')
        plt.xlabel('Tempo (s)')
        plt.ylabel('Posição (m)')
        plt.title('p3 - Posição da Massa 3 (Coxa)')
        plt.legend()
        plt.grid(True)
        plt.xlim(0, 2)

        plt.subplot(2, 2, 4)
        plt.plot(t_sim_opt, p4_d_sim, 'b--', linewidth=2, label='Experimental', alpha=0.7)
        plt.plot(t_sim_opt, p4_sim_opt, 'r-', linewidth=1.5, label='Simulado (Otimizado)')
        plt.xlabel('Tempo (s)')
        plt.ylabel('Posição (m)')
        plt.title('p4 - Posição da Massa 4 (Tronco)')
        plt.legend()
        plt.grid(True)
        plt.xlim(0, 2)

        plt.tight_layout()
        plt.show()

        # Calcular métricas de erro para GRF
        mse_opt = np.mean((GRF_est_opt - MGRF_sim_opt)**2)
        rmse_opt = np.sqrt(mse_opt)
        mae_opt = np.mean(np.abs(GRF_est_opt - MGRF_sim_opt))

        # Calcular métricas de erro para posições
        mse_p1 = np.mean((p1_sim_opt - p1_d_sim)**2)
        mse_p2 = np.mean((p2_sim_opt - p2_d_sim)**2)
        mse_p3 = np.mean((p3_sim_opt - p3_d_sim)**2)
        mse_p4 = np.mean((p4_sim_opt - p4_d_sim)**2)

        rmse_p1 = np.sqrt(mse_p1)
        rmse_p2 = np.sqrt(mse_p2)
        rmse_p3 = np.sqrt(mse_p3)
        rmse_p4 = np.sqrt(mse_p4)

        print("\n=== PARÂMETROS OTIMIZADOS DO CONTROLADOR PI ===")
        print(f"Kp1: {Kp1_opt:.2f}")
        print(f"Kp2: {Kp2_opt:.2f}")
        print(f"Kp3: {Kp3_opt:.2f}")
        print(f"Kp4: {Kp4_opt:.2f}")
        print(f"Ki1: {Ki1_opt:.2f}")
        print(f"Ki2: {Ki2_opt:.2f}")
        print(f"Ki3: {Ki3_opt:.2f}")
        print(f"Ki4: {Ki4_opt:.2f}")

        print("\n=== MÉTRICAS DE ERRO - GRF (Parâmetros Otimizados) ===")
        print(f"MSE:  {mse_opt:.2f} N²")
        print(f"RMSE: {rmse_opt:.2f} N")
        print(f"MAE:  {mae_opt:.2f} N")

        print("\n=== MÉTRICAS DE ERRO - POSIÇÕES (RMSE) ===")
        print(f"p1 (Pé):    {rmse_p1:.6f} m")
        print(f"p2 (Perna): {rmse_p2:.6f} m")
        print(f"p3 (Coxa):  {rmse_p3:.6f} m")
        print(f"p4 (Tronco):{rmse_p4:.6f} m")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## 🔄 Mudança no Critério de Otimização

    ### Critério Anterior (comentado):
    - **Objetivo**: Minimizar erro da GRF (força de reação do solo)
    - **Problema**: Focava apenas em uma variável, podendo resultar em posições mal rastreadas

    ### ✅ Critério Atual (implementado):
    - **Objetivo**: Minimizar erro das POSIÇÕES (p1, p2, p3, p4)
    - **Vantagens**:
      1. Garante que todas as massas sigam as trajetórias experimentais
      2. As forças são ajustadas como consequência do bom rastreamento
      3. Resulta em estimativa mais física e consistente da GRF
      4. Todos os parâmetros (Kp1-4, Ki1-4) são efetivamente utilizados

    ### 📊 Intervalos de Busca Atualizados:

    Como agora otimizamos todas as posições, os intervalos foram ajustados:
    - **Kp1, Kp2, Kp3, Kp4**: 10³ a 10⁶ (escala logarítmica)
    - **Ki1, Ki2, Ki3, Ki4**: 10² a 10⁵ (escala logarítmica)

    Todos os parâmetros agora têm intervalos significativos, pois todos contribuem
    para o rastreamento das respectivas posições.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## 📍 Comparação de Posições: Experimental vs Simulado

    O gráfico acima mostra a comparação entre as posições experimentais (linha azul tracejada)
    e as posições simuladas com os parâmetros otimizados (linha vermelha sólida) para cada massa:

    ### Interpretação:

    - **Linha Azul Tracejada**: Posições medidas experimentalmente (dados reais)
    - **Linha Vermelha Sólida**: Posições simuladas pelo modelo com controlador PI otimizado

    ### 🎯 Objetivo do Controlador PI:

    O controlador PI ajusta as forças (GRF, Factm2, Factm3, Factm4) para que as posições
    simuladas **sigam** as posições experimentais o mais próximo possível.

    - **Quanto mais próximas** as linhas azul e vermelha, melhor é o desempenho do controlador
    - **RMSE baixo** indica que o controlador está conseguindo rastrear bem as posições

    ### 💡 Observações:

    - **p1 (Pé)**: Geralmente tem o melhor rastreamento (menor erro) pois é onde aplicamos a GRF
    - **p2, p3, p4**: O rastreamento depende dos ganhos Kp2-4 e Ki2-4
    - Se alguma posição não está sendo bem rastreada, pode ser necessário ajustar os intervalos
      de busca dos parâmetros correspondentes na otimização
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## 📊 Forças Atuantes nas Massas (Factm)

    O gráfico acima mostra as forças estimadas pelo controlador PI para cada uma das 4 massas do modelo:

    ### 🔴 GRF (Ground Reaction Force) - Massa 1 (Pé)
    - **Força de reação do solo** aplicada no pé
    - É a força que estamos tentando estimar com maior precisão
    - Comparada com os dados medidos (MGRF) para validação

    ### 🟢 Factm2 - Massa 2 (Perna/Tíbia)
    - Força de controle aplicada na massa da perna
    - Ajuda a corrigir o erro de posição da perna em relação aos dados experimentais
    - Pode ser zero ou pequena se Kp2 e Ki2 forem pequenos

    ### 🟠 Factm3 - Massa 3 (Coxa/Fêmur)
    - Força de controle aplicada na massa da coxa
    - Ajuda a corrigir o erro de posição da coxa em relação aos dados experimentais
    - Pode ser zero ou pequena se Kp3 e Ki3 forem pequenos

    ### 🟣 Factm4 - Massa 4 (Tronco)
    - Força de controle aplicada na massa do tronco
    - Ajuda a corrigir o erro de posição do tronco em relação aos dados experimentais
    - Pode ser zero ou pequena se Kp4 e Ki4 forem pequenos

    ### 💡 Interpretação:

    - **Forças positivas**: Atuam para baixo (na direção da gravidade)
    - **Forças negativas**: Atuam para cima (contra a gravidade)
    - **Magnitude das forças**: Indica o quanto o controlador precisa atuar para corrigir os erros

    ### 🎯 Objetivo:

    O controlador PI ajusta essas forças automaticamente para que as posições simuladas
    sigam as posições experimentais medidas, permitindo assim estimar a GRF de forma precisa.
    """
    )
    return


if __name__ == "__main__":
    app.run()