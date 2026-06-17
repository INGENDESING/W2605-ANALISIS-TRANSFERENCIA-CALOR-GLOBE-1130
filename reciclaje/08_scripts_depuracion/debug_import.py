import sys
print('sys path')
sys.path.insert(0, 'src')
sys.path.insert(0, 'webapp')
print('importing numpy...')
import numpy as np
print('numpy ok')
print('importing scipy...')
from scipy.integrate import solve_ivp
print('scipy ok')
print('importing src modules...')
from propiedades_glucosa import rho_glucosa, mu_glucosa, Cp_glucosa, k_glucosa, Pr_glucosa, rho_agua, Cp_agua
from coeficiente_U import coeficiente_U
from geometria_tanque import A_CONTACTO, volumen_total, caudal_desde_velocidad_media_cana
print('src modules ok')
print('A_CONTACTO:', A_CONTACTO)
print('volumen_total:', volumen_total())
