#!/usr/bin/env python3
"""Script de depuración para verificar valores de U."""

import sys
import os
import numpy as np

sys.path.append('src')

from coeficiente_U import coeficiente_U
from calcular_areas import calcular_U_corregido

print("=" * 80)
print("DEPURACIÓN DE VALORES DE U")
print("=" * 80)

# Verificar U directamente con coeficiente_U
print("\n1. VALORES DIRECTOS DE coeficiente_U():")
print("T_g [°C] | U [W/m2K] | 1/U [m2K/W]")
print("-" * 40)
U_directos = []
inv_U_directos = []
for T_g in [25, 30, 35, 40, 45, 50, 55, 57]:
    U, _, _, _ = coeficiente_U(2.5, 75.0, T_g)
    inv_U = 1.0 / U
    U_directos.append(U)
    inv_U_directos.append(inv_U)
    print(f"{T_g:8.1f} | {U:9.2f} | {inv_U:11.6f}")

print("-" * 40)
U_prom_directo = np.mean(U_directos)
inv_U_prom_directo = np.mean(inv_U_directos)
U_prom_from_inv = 1.0 / inv_U_prom_directo
print(f"Promedio U = {U_prom_directo:.2f} W/m2K")
print(f"Promedio 1/U = {inv_U_prom_directo:.6f} m2K/W")
print(f"U desde 1/U = {U_prom_from_inv:.2f} W/m2K")
print(f"Rango U: [{min(U_directos):.2f}, {max(U_directos):.2f}]")

# Verificar U con calcular_U_corregido
print("\n2. VALORES DE calcular_U_corregido():")
print("T_g [°C] | U [W/m2K] | 1/U [m2K/W]")
print("-" * 40)
U_corregidos = []
inv_U_corregidos = []
for T_g in [25, 30, 35, 40, 45, 50, 55, 57]:
    U, T_agua, T_pared, h_i, h_o = calcular_U_corregido(2.5, 75.0, T_g, usar_temperatura_media=False)
    inv_U = 1.0 / U
    U_corregidos.append(U)
    inv_U_corregidos.append(inv_U)
    print(f"{T_g:8.1f} | {U:9.2f} | {inv_U:11.6f}")

print("-" * 40)
U_prom_corregido = np.mean(U_corregidos)
inv_U_prom_corregido = np.mean(inv_U_corregidos)
U_prom_from_inv_corregido = 1.0 / inv_U_prom_corregido
print(f"Promedio U = {U_prom_corregido:.2f} W/m2K")
print(f"Promedio 1/U = {inv_U_prom_corregido:.6f} m2K/W")
print(f"U desde 1/U = {U_prom_from_inv_corregido:.2f} W/m2K")
print(f"Rango U: [{min(U_corregidos):.2f}, {max(U_corregidos):.2f}]")

# Comparar
print("\n" + "=" * 80)
print("CONCLUSIÓN:")
print("=" * 80)
print(f"✓ U directo (min, max): {min(U_directos):.2f} - {max(U_directos):.2f}")
print(f"✓ U corregido (min, max): {min(U_corregidos):.2f} - {max(U_corregidos):.2f}")
print(f"✓ Deben ser iguares si calcular_U_corregido funciona correctamente")
print(f"✓ U_prom desde 1/U directo: {U_prom_from_inv:.2f}")
print(f"✓ U_prom debe estar entre 23.7 y 36.2")
print("=" * 80)
