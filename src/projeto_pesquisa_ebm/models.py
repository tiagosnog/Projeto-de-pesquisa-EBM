"""
Modelos biomecânicos para análise de corrida
"""

import numpy as np
from scipy.optimize import minimize


class MassSpringDamperModel:
    """
    Modelo massa-mola-amortecedor de 2 graus de liberdade
    
    Baseado em Nedergaard et al. e outros trabalhos de modelamento
    de impacto na corrida.
    """
    
    def __init__(self, m1, m2, k1, k2, c, g=-9.81):
        """
        Inicializa o modelo MSD
        
        Parameters
        ----------
        m1 : float
            Massa superior (kg)
        m2 : float
            Massa inferior (kg)
        k1 : float
            Constante da mola superior (N/m)
        k2 : float
            Constante da mola inferior (N/m)
        c : float
            Coeficiente de amortecimento (N.s/m)
        g : float
            Aceleração da gravidade (m/s²)
        """
        self.m1 = m1
        self.m2 = m2
        self.k1 = k1
        self.k2 = k2
        self.c = c
        self.g = g
        
    def acceleration_m1(self, x1, x2, x3, x4):
        """
        Calcula aceleração da massa superior
        
        Parameters
        ----------
        x1 : float
            Posição da massa 1
        x2 : float
            Velocidade da massa 1
        x3 : float
            Posição da massa 2
        x4 : float
            Velocidade da massa 2
            
        Returns
        -------
        float
            Aceleração da massa 1
        """
        return self.g - (self.k1 * (x1 - x3)) / self.m1
    
    def acceleration_m2(self, x1, x2, x3, x4, l2=0):
        """
        Calcula aceleração da massa inferior
        
        Parameters
        ----------
        x1 : float
            Posição da massa 1
        x2 : float
            Velocidade da massa 1
        x3 : float
            Posição da massa 2
        x4 : float
            Velocidade da massa 2
        l2 : float
            Comprimento de repouso da mola inferior
            
        Returns
        -------
        float
            Aceleração da massa 2
        """
        omega2 = np.sqrt(self.k2 / self.m2)
        return (self.g + (self.k1 * (x1 - x3)) / self.m2 - 
                omega2**2 * (x3 - l2) - 
                (self.c / self.m2) * x4)
    
    def simulate(self, t_max, dt, x1_0, x2_0, x3_0, x4_0, F_impulse=None):
        """
        Simula o sistema usando método de Euler
        
        Parameters
        ----------
        t_max : float
            Tempo total de simulação (s)
        dt : float
            Passo de tempo (s)
        x1_0 : float
            Posição inicial da massa 1
        x2_0 : float
            Velocidade inicial da massa 1
        x3_0 : float
            Posição inicial da massa 2
        x4_0 : float
            Velocidade inicial da massa 2
        F_impulse : callable or None
            Função que retorna força de impulso em função do tempo
            
        Returns
        -------
        dict
            Dicionário com arrays de tempo, posições, velocidades e forças
        """
        n_steps = int(t_max / dt)
        
        # Inicializar arrays
        t = np.linspace(0, t_max, n_steps)
        x1 = np.zeros(n_steps)
        x2 = np.zeros(n_steps)
        x3 = np.zeros(n_steps)
        x4 = np.zeros(n_steps)
        
        # Condições iniciais
        x1[0] = x1_0
        x2[0] = x2_0
        x3[0] = x3_0
        x4[0] = x4_0
        
        # Método de Euler
        for i in range(n_steps - 1):
            a1 = self.acceleration_m1(x1[i], x2[i], x3[i], x4[i])
            a2 = self.acceleration_m2(x1[i], x2[i], x3[i], x4[i])
            
            x2[i+1] = x2[i] + a1 * dt
            x1[i+1] = x1[i] + x2[i] * dt
            
            x4[i+1] = x4[i] + a2 * dt
            x3[i+1] = x3[i] + x4[i] * dt
        
        return {
            'time': t,
            'x1': x1,
            'x2': x2,
            'x3': x3,
            'x4': x4
        }
    
    def optimize_parameters(self, measured_grf, measured_acc, initial_guess=None):
        """
        Otimiza parâmetros k1 e k2 para ajustar aos dados medidos
        
        Parameters
        ----------
        measured_grf : np.ndarray
            GRF medida
        measured_acc : np.ndarray
            Aceleração medida
        initial_guess : list or None
            Chute inicial para [k1, k2]
            
        Returns
        -------
        dict
            Dicionário com parâmetros otimizados e erro
        """
        if initial_guess is None:
            initial_guess = [self.k1, self.k2]
        
        def objective(params):
            k1, k2 = params
            # Implementar função objetivo aqui
            # (comparação entre modelo e dados medidos)
            return 0  # Placeholder
        
        result = minimize(objective, initial_guess, method='Nelder-Mead')
        
        return {
            'k1': result.x[0],
            'k2': result.x[1],
            'error': result.fun,
            'success': result.success
        }

