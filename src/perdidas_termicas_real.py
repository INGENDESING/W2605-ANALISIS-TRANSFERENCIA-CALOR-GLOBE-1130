"""
Cálculo de pérdidas térmicas con área real expuesta — Proyecto W2605
====================================================================
Recalcula las pérdidas térmicas del tanque de glucosa usando el área
total real expuesta al ambiente (fondo toriesférico + cilindro cubierto
al 80 % de llenado), aislamiento de 50,8 mm de lana mineral, y
comparando operación a 57 °C y 60 °C.

Modelo: resistencias térmicas en serie desde la glucosa hasta el ambiente.

Referencias:
  - Incropera et al., Fundamentals of Heat and Mass Transfer, 7th ed.
  - API 650, Anexo H (aislamiento de tanques de almacenamiento).
  - ASTM C547 — Mineral Fiber Pipe Insulation.
  - Geometría del tanque: src/geometria_tanque.py
  - Propiedades de la glucosa: src/propiedades_glucosa.py
"""

import csv
import os
import sys

import numpy as np

sys.path.append(os.path.dirname(__file__))

from geometria_tanque import (
    H_FONDO,
    OD_SHELL,
    t_HEAD,
    volumen_total,
)
from propiedades_glucosa import Cp_glucosa, K_SS316L, rho_glucosa
from calculo_calor_perdido_80 import (
    area_cilindrica_al_80porciento,
    area_fondo_torisferico,
)

# =============================================================================
# PARÁMETROS DEL MODELO
# =============================================================================

T_AMBIENTE = 26.5           # Temperatura ambiente [°C] — Cali, Colombia
PORCENTAJE_LLENADO = 80.0   # Nivel de operación [%]

# Aislamiento de lana mineral
ESPESOR_AISLAMIENTO = 0.0508   # Espesor [m] — 2 pulgadas
K_AISLAMIENTO = 0.045          # Conductividad térmica [W/(m·K)]
                               # Valor conservador con humedad (ASTM C547)

# Coeficientes convectivos
H_EXT_VIENTO = 15.0         # Convección externa [W/(m²·K)] — viento ligero + radiación
H_INT_GLUCOSA = 28.0        # Convección interna glucosa-pared [W/(m²·K)]

# Temperaturas de evaluación
TEMPERATURAS_EVALUACION = [57.0, 60.0]


def calcular_area_real_expuesta():
    """
    Área total real expuesta al ambiente al 80 % de llenado.
    Suma del fondo toriesférico más el área cilíndrica cubierta por el líquido.
    """
    A_fondo = area_fondo_torisferico()
    A_cil_80, h_cil_cubierto, h_nivel_total = area_cilindrica_al_80porciento()
    A_total = A_fondo + A_cil_80
    return {
        'A_fondo': A_fondo,
        'A_cil_80': A_cil_80,
        'A_total': A_total,
        'h_cil_cubierto': h_cil_cubierto,
        'h_nivel_total': h_nivel_total,
    }


def calcular_resistencias(espesor_aisl=ESPESOR_AISLAMIENTO, k_aisl=K_AISLAMIENTO):
    """
    Resistencias térmicas por unidad de área [m²·K/W].
    """
    R_conv_int = 1.0 / H_INT_GLUCOSA
    R_pared = t_HEAD / K_SS316L
    R_aislamiento = espesor_aisl / k_aisl
    R_conv_ext = 1.0 / H_EXT_VIENTO

    R_total = R_conv_int + R_pared + R_aislamiento + R_conv_ext

    return {
        'R_conv_int': R_conv_int,
        'R_pared': R_pared,
        'R_aislamiento': R_aislamiento,
        'R_conv_ext': R_conv_ext,
        'R_total': R_total,
    }


def calcular_perdidas(T_glucosa, espesor_aisl=ESPESOR_AISLAMIENTO, k_aisl=K_AISLAMIENTO):
    """
    Pérdidas térmicas totales para una temperatura de glucosa dada.

    Retorna
    -------
    dict con Q_W, Q_kW, Q_MJ_h, U, R_total, Delta_T, áreas, etc.
    """
    areas = calcular_area_real_expuesta()
    resistencias = calcular_resistencias(espesor_aisl, k_aisl)

    U = 1.0 / resistencias['R_total']
    Delta_T = T_glucosa - T_AMBIENTE
    Q_W = U * areas['A_total'] * Delta_T

    return {
        'T_glucosa': T_glucosa,
        'T_ambiente': T_AMBIENTE,
        'Delta_T': Delta_T,
        'A_total': areas['A_total'],
        'A_fondo': areas['A_fondo'],
        'A_cil_80': areas['A_cil_80'],
        'U_perdidas': U,
        'R_total': resistencias['R_total'],
        'R_conv_int': resistencias['R_conv_int'],
        'R_pared': resistencias['R_pared'],
        'R_aislamiento': resistencias['R_aislamiento'],
        'R_conv_ext': resistencias['R_conv_ext'],
        'Q_W': Q_W,
        'Q_kW': Q_W / 1000.0,
        'Q_MJ_h': Q_W * 3600.0 / 1.0e6,
    }


def calcular_tiempo_perdida_3C(T_glucosa, Q_W, porcentaje=PORCENTAJE_LLENADO):
    """
    Tiempo necesario para que la masa de glucosa pierda 3 °C por efecto
    de las pérdidas térmicas calculadas.
    """
    V_total = volumen_total()
    V_op = V_total * (porcentaje / 100.0)
    rho_op = rho_glucosa(T_glucosa)
    Cp_op = Cp_glucosa(T_glucosa)

    masa = V_op * rho_op
    C_termica = masa * Cp_op  # J/°C
    Q_3C_J = C_termica * 3.0  # J

    tiempo_s = Q_3C_J / Q_W
    tiempo_h = tiempo_s / 3600.0
    tiempo_d = tiempo_h / 24.0

    return {
        'masa_kg': masa,
        'C_termica': C_termica,
        'Q_3C_MJ': Q_3C_J / 1.0e6,
        'tiempo_h': tiempo_h,
        'tiempo_d': tiempo_d,
    }


def analisis_sensibilidad_espesor(T_glucosa):
    """
    Análisis de sensibilidad del espesor de aislamiento para una temperatura.
    """
    espesores_mm = [0.0, 12.7, 25.4, 38.1, 50.8, 76.2, 101.6]
    resultados = []

    for e_mm in espesores_mm:
        e_m = e_mm / 1000.0
        res = calcular_perdidas(T_glucosa, espesor_aisl=e_m)
        tiempo = calcular_tiempo_perdida_3C(T_glucosa, res['Q_W'])
        resultados.append({
            'espesor_mm': e_mm,
            'U': res['U_perdidas'],
            'Q_MJ_h': res['Q_MJ_h'],
            'tiempo_3C_d': tiempo['tiempo_d'],
        })

    return resultados


def exportar_csv(resultados_principales, resultados_sensibilidad, csv_path):
    """
    Exporta los resultados a un archivo CSV.
    """
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        writer.writerow(['Perdidas termicas con area real expuesta — W2605'])
        writer.writerow([])
        writer.writerow(['Parametros del modelo'])
        writer.writerow(['Temperatura ambiente (°C)', T_AMBIENTE])
        writer.writerow(['Nivel de llenado (%)', PORCENTAJE_LLENADO])
        writer.writerow(['Espesor aislamiento (mm)', ESPESOR_AISLAMIENTO * 1000])
        writer.writerow(['Conductividad aislamiento (W/m·K)', K_AISLAMIENTO])
        writer.writerow(['h_ext (W/m²·K)', H_EXT_VIENTO])
        writer.writerow(['h_int (W/m²·K)', H_INT_GLUCOSA])
        writer.writerow([])

        # Resultados principales
        writer.writerow(['Resultados principales'])
        writer.writerow([
            'T_glucosa (°C)', 'T_ambiente (°C)', 'Delta_T (K)',
            'A_total (m²)', 'U (W/m²·K)', 'R_total (m²·K/W)',
            'Q (W)', 'Q (kW)', 'Q (MJ/h)',
            'Masa glucosa (ton)', 'Cp (J/kg·°C)', 't_3C (h)', 't_3C (d)'
        ])

        for r in resultados_principales:
            writer.writerow([
                r['T_glucosa'], r['T_ambiente'], r['Delta_T'],
                round(r['A_total'], 2), round(r['U_perdidas'], 3), round(r['R_total'], 4),
                round(r['Q_W'], 1), round(r['Q_kW'], 3), round(r['Q_MJ_h'], 2),
                round(r['masa_ton'], 1), round(r['Cp'], 1),
                round(r['tiempo_3C_h'], 1), round(r['tiempo_3C_d'], 2)
            ])

        writer.writerow([])

        # Análisis de sensibilidad
        writer.writerow(['Analisis de sensibilidad — espesor de aislamiento'])
        writer.writerow(['T_glucosa (°C)', 'Espesor (mm)', 'U (W/m²·K)', 'Q (MJ/h)', 't_3C (dias)'])

        for T_gluc, filas in resultados_sensibilidad.items():
            for fila in filas:
                writer.writerow([
                    T_gluc,
                    fila['espesor_mm'],
                    round(fila['U'], 3),
                    round(fila['Q_MJ_h'], 2),
                    round(fila['tiempo_3C_d'], 2)
                ])


def main():
    print("=" * 78)
    print("PERDIDAS TERMICAS CON AREA REAL EXPUESTA — W2605")
    print("=" * 78)

    # Geometría
    areas = calcular_area_real_expuesta()
    print("\n1. GEOMETRIA Y AREA EXPUESTA")
    print("-" * 78)
    print(f"  Area fondo torisferico:     {areas['A_fondo']:.2f} m2")
    print(f"  Area cilindrica al 80%:     {areas['A_cil_80']:.2f} m2")
    print(f"  Area TOTAL expuesta:        {areas['A_total']:.2f} m2")
    print(f"  Nivel de liquido al 80%:    {areas['h_nivel_total']:.2f} m")
    print(f"  Altura cilindrica cubierta: {areas['h_cil_cubierto']:.2f} m")

    # Resistencias
    resistencias = calcular_resistencias()
    print("\n2. RESISTENCIAS TERMICAS (50,8 mm lana mineral)")
    print("-" * 78)
    print(f"  R_conv_int:   {resistencias['R_conv_int']:.4f} m2.K/W")
    print(f"  R_pared:      {resistencias['R_pared']:.6f} m2.K/W")
    print(f"  R_aislamiento:{resistencias['R_aislamiento']:.4f} m2.K/W")
    print(f"  R_conv_ext:   {resistencias['R_conv_ext']:.4f} m2.K/W")
    print(f"  R_total:      {resistencias['R_total']:.4f} m2.K/W")
    print(f"  U_perdidas:   {1.0/resistencias['R_total']:.3f} W/(m2.K)")

    # Resultados principales
    print("\n3. PERDIDAS TERMICAS A 57 °C Y 60 °C")
    print("-" * 78)

    resultados_principales = []
    resultados_sensibilidad = {}

    for T_g in TEMPERATURAS_EVALUACION:
        res = calcular_perdidas(T_g)
        t_3c = calcular_tiempo_perdida_3C(T_g, res['Q_W'])

        res_completo = {**res, **{
            'masa_ton': t_3c['masa_kg'] / 1000.0,
            'Cp': Cp_glucosa(T_g),
            'tiempo_3C_h': t_3c['tiempo_h'],
            'tiempo_3C_d': t_3c['tiempo_d'],
        }}
        resultados_principales.append(res_completo)

        print(f"\n  T_glucosa = {T_g:.1f} °C")
        print(f"    Delta T:        {res['Delta_T']:.1f} K")
        print(f"    U_perdidas:     {res['U_perdidas']:.3f} W/(m2.K)")
        print(f"    Q_perdida:      {res['Q_W']:.1f} W = {res['Q_kW']:.3f} kW = {res['Q_MJ_h']:.2f} MJ/h")
        print(f"    Masa glucosa:   {res_completo['masa_ton']:.1f} ton")
        print(f"    Cp glucosa:     {res_completo['Cp']:.1f} J/(kg.°C)")
        print(f"    Tiempo 3 °C:    {res_completo['tiempo_3C_h']:.1f} h = {res_completo['tiempo_3C_d']:.2f} dias")

        # Sensibilidad
        sens = analisis_sensibilidad_espesor(T_g)
        resultados_sensibilidad[T_g] = sens

        print(f"\n  Analisis de sensibilidad — T_glucosa = {T_g:.1f} °C")
        print(f"    {'Espesor (mm)':>14} {'U (W/m2.K)':>12} {'Q (MJ/h)':>12} {'t_3C (dias)':>12}")
        for fila in sens:
            print(f"    {fila['espesor_mm']:>14.1f} {fila['U']:>12.3f} {fila['Q_MJ_h']:>12.2f} {fila['tiempo_3C_d']:>12.2f}")

    # Exportar CSV
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'results', 'perdidas_termicas_real.csv')
    csv_path = os.path.abspath(csv_path)
    exportar_csv(resultados_principales, resultados_sensibilidad, csv_path)
    print(f"\n4. EXPORTACION")
    print("-" * 78)
    print(f"  Resultados exportados a: {csv_path}")

    print("\n" + "=" * 78)


if __name__ == "__main__":
    main()
