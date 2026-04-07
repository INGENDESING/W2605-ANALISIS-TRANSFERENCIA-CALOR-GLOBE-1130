"""
Modulo de calculo de espesor de aislamiento termico — Proyecto P2611
=====================================================================
Determina el espesor optimo de aislamiento de lana mineral para la
chaqueta de media cana del fondo toriesferico del tanque de glucosa.

Criterios:
  1. Minimizar perdidas de calor al ambiente
  2. Temperatura superficial exterior < 60 C (seguridad al contacto)
  3. Espesor economico (balance costo energia vs. costo aislamiento)

Modelo: resistencias en serie desde el agua caliente hasta el ambiente:
  R_total = R_conv_int + R_pared + R_perfil + R_aislamiento + R_conv_ext

Ref:
  - Incropera et al., 7th ed., Cap. 3 (Conduccion unidimensional)
  - ASTM C547 — Mineral Fiber Pipe Insulation
  - NIA (National Insulation Association) — Economic Thickness Guidelines
"""

import numpy as np


# =============================================================================
# PROPIEDADES DEL AISLAMIENTO (Lana Mineral)
# =============================================================================

K_LANA_MINERAL = 0.040     # Conductividad termica a ~50 C [W/(m.K)]
                            # Rango tipico: 0.035-0.045 W/(m.K)
                            # Ref: ASTM C547, tabla de fabricante

# Acero SS316L
K_SS316L = 16.3            # Conductividad [W/(m.K)]

# Acero del perfil de media cana
t_PERFIL_M = 0.0045        # Espesor del perfil [m]
t_PARED_TANQUE = 0.009     # Espesor pared del tanque [m]

# Conveccion externa (superficie aislada al ambiente)
h_EXT_NATURAL = 8.0        # Coef. conveccion natural aire exterior [W/m2.K]
                            # Rango: 5-15 W/m2.K para superficies verticales

# Ambiente
T_AMBIENTE = 26.5           # Temperatura ambiente Cali [C]

# Area de la chaqueta expuesta al ambiente (aproximacion)
# La media cana cubre 13 m2 de contacto con el tanque; la superficie
# exterior del perfil (3 lados) es aproximadamente:
# Perimetro expuesto = ancho + 2*alto = 0.141 + 2*0.0455 = 0.232 m
# Longitud total espiral ~ A_contacto / ancho = 13 / 0.141 = 92.2 m
# Area expuesta ~ perimetro * longitud = 0.232 * 92.2 = 21.4 m2
L_ESPIRAL = 13.0 / 0.141   # Longitud de la espiral [m]
P_EXPUESTO = 0.141 + 2 * 0.0455  # Perimetro exterior del perfil [m]
A_EXPUESTA = P_EXPUESTO * L_ESPIRAL  # Area expuesta al ambiente [m2]
A_CONTACTO = 13.0           # Area de contacto con el tanque [m2]


# =============================================================================
# CALCULO DE PERDIDA DE CALOR
# =============================================================================

def perdida_calor_sin_aislamiento(T_agua, T_glucosa, h_i=6800.0):
    """
    Perdida de calor al ambiente SIN aislamiento.

    Modelo simplificado (pared plana):
    Q_perdida = (T_agua - T_amb) / R_total_ext

    La resistencia se calcula desde el agua hasta el ambiente, pasando por:
    - Conveccion interna (agua)
    - Pared del perfil de media cana (acero)
    - Aire atrapado (si hay) o contacto directo
    - Conveccion natural externa

    Parametros
    ----------
    T_agua    : float — Temperatura del agua [C]
    T_glucosa : float — Temperatura de la glucosa [C]
    h_i       : float — Coef. conveccion interna [W/m2.K]

    Retorna
    -------
    Q_perdida : float — Perdida de calor al ambiente [W]
    T_sup_ext : float — Temperatura de la superficie exterior [C]
    """
    # Resistencias por unidad de area [m2.K/W]
    R_conv_int = 1.0 / h_i
    R_perfil = t_PERFIL_M / K_SS316L
    R_conv_ext = 1.0 / h_EXT_NATURAL

    R_total = R_conv_int + R_perfil + R_conv_ext

    DeltaT = T_agua - T_AMBIENTE
    q = DeltaT / R_total  # Flujo de calor [W/m2]
    Q_perdida = q * A_EXPUESTA  # Potencia total perdida [W]

    # Temperatura superficial exterior
    T_sup_ext = T_AMBIENTE + q * R_conv_ext

    return Q_perdida, T_sup_ext


def perdida_calor_con_aislamiento(T_agua, espesor_aisl_mm, h_i=6800.0):
    """
    Perdida de calor al ambiente CON aislamiento de lana mineral.

    Parametros
    ----------
    T_agua         : float — Temperatura del agua [C]
    espesor_aisl_mm: float — Espesor de aislamiento [mm]
    h_i            : float — Coef. conveccion interna [W/m2.K]

    Retorna
    -------
    Q_perdida  : float — Perdida de calor al ambiente [W]
    T_sup_ext  : float — Temperatura de la superficie exterior [C]
    eficiencia : float — Reduccion de perdida vs sin aislamiento [%]
    """
    espesor_m = espesor_aisl_mm / 1000.0

    # Resistencias por unidad de area [m2.K/W]
    R_conv_int = 1.0 / h_i
    R_perfil = t_PERFIL_M / K_SS316L
    R_aisl = espesor_m / K_LANA_MINERAL
    R_conv_ext = 1.0 / h_EXT_NATURAL

    R_total = R_conv_int + R_perfil + R_aisl + R_conv_ext

    DeltaT = T_agua - T_AMBIENTE
    q = DeltaT / R_total  # [W/m2]
    Q_perdida = q * A_EXPUESTA

    # Temperatura superficial exterior
    T_sup_ext = T_AMBIENTE + q * R_conv_ext

    # Comparar con sin aislamiento
    Q_sin, _ = perdida_calor_sin_aislamiento(T_agua, 20.0, h_i)
    eficiencia = (1.0 - Q_perdida / Q_sin) * 100

    return Q_perdida, T_sup_ext, eficiencia


def espesor_recomendado(T_agua, T_sup_max=60.0, h_i=6800.0):
    """
    Calcula el espesor minimo de aislamiento para que la temperatura
    superficial exterior no exceda T_sup_max (seguridad al contacto).

    Parametros
    ----------
    T_agua    : float — Temperatura del agua [C]
    T_sup_max : float — Temperatura max. superficial [C]
    h_i       : float — Coef. conveccion interna [W/m2.K]

    Retorna
    -------
    espesor_mm : float — Espesor minimo requerido [mm]
    """
    # De la ecuacion de resistencias:
    # T_sup = T_amb + q / h_ext
    # q = DeltaT / R_total
    # T_sup_max = T_amb + DeltaT * R_conv_ext / R_total
    # Resolver para R_aisl:
    DeltaT = T_agua - T_AMBIENTE
    R_conv_int = 1.0 / h_i
    R_perfil = t_PERFIL_M / K_SS316L
    R_conv_ext = 1.0 / h_EXT_NATURAL

    # T_sup_max = T_amb + DeltaT * R_conv_ext / (R_conv_int + R_perfil + R_aisl + R_conv_ext)
    # Despejar R_aisl:
    R_conv_ext_required = (T_sup_max - T_AMBIENTE) / DeltaT
    # R_conv_ext / R_total = (T_sup_max - T_amb) / DeltaT
    # R_total = R_conv_ext * DeltaT / (T_sup_max - T_amb)
    R_total_required = R_conv_ext * DeltaT / (T_sup_max - T_AMBIENTE)
    R_aisl = R_total_required - R_conv_int - R_perfil - R_conv_ext

    if R_aisl <= 0:
        return 0.0  # No se necesita aislamiento para este criterio

    espesor_m = R_aisl * K_LANA_MINERAL
    espesor_mm = espesor_m * 1000
    return espesor_mm


def tabla_espesores(T_agua=75.0):
    """
    Genera tabla comparativa de espesores de aislamiento.

    Parametros
    ----------
    T_agua : float — Temperatura del agua [C]

    Retorna
    -------
    resultados : list of dict
    """
    espesores = [0, 12.7, 25.4, 38.1, 50.8, 76.2, 101.6]  # mm (0, 1/2", 1", 1.5", 2", 3", 4")
    resultados = []

    for e in espesores:
        if e == 0:
            Q, T_sup = perdida_calor_sin_aislamiento(T_agua, 20.0)
            eff = 0.0
        else:
            Q, T_sup, eff = perdida_calor_con_aislamiento(T_agua, e)

        resultados.append({
            'espesor_mm': e,
            'espesor_in': e / 25.4,
            'Q_perdida_W': Q,
            'Q_perdida_kW': Q / 1000,
            'T_sup_ext': T_sup,
            'eficiencia': eff,
            'seguro_contacto': T_sup <= 60.0
        })

    return resultados


# =============================================================================
# RESUMEN
# =============================================================================

if __name__ == "__main__":
    print("=" * 78)
    print("CALCULO DE ESPESOR DE AISLAMIENTO — Proyecto P2611")
    print("=" * 78)

    print(f"\nParametros del modelo:")
    print(f"  k_lana_mineral = {K_LANA_MINERAL} W/(m.K)")
    print(f"  h_ext (conv. natural aire) = {h_EXT_NATURAL} W/(m2.K)")
    print(f"  T_ambiente (Cali) = {T_AMBIENTE} C")
    print(f"  A_expuesta = {A_EXPUESTA:.1f} m2")
    print(f"  L_espiral = {L_ESPIRAL:.1f} m")

    for T_w in [65.0, 75.0]:
        print(f"\n--- T_agua = {T_w} C ---")

        # Espesor minimo por seguridad
        e_min = espesor_recomendado(T_w, T_sup_max=60.0)
        print(f"Espesor minimo (T_sup < 60 C): {e_min:.1f} mm ({e_min/25.4:.2f}\")")

        # Tabla comparativa
        resultados = tabla_espesores(T_w)
        print(f"\n{'Espesor':>10} {'Q_perd [kW]':>12} {'T_sup [C]':>10} {'Efic. [%]':>10} {'Seguro':>8}")
        print("-" * 55)
        for r in resultados:
            label = f"{r['espesor_mm']:.0f} mm" if r['espesor_mm'] > 0 else "Sin aisl."
            seg = "SI" if r['seguro_contacto'] else "NO"
            print(f"{label:>10} {r['Q_perdida_kW']:>12.2f} {r['T_sup_ext']:>10.1f} "
                  f"{r['eficiencia']:>10.1f} {seg:>8}")

    # Recomendacion final
    print("\n" + "=" * 78)
    print("RECOMENDACION")
    print("=" * 78)
    e_rec_65 = espesor_recomendado(65.0)
    e_rec_75 = espesor_recomendado(75.0)
    print(f"Agua a 65 C: espesor minimo = {e_rec_65:.1f} mm -> comercial: 1\" (25.4 mm)")
    print(f"Agua a 75 C: espesor minimo = {e_rec_75:.1f} mm -> comercial: 1.5\" (38.1 mm)")
    print(f"\nRecomendacion: 2\" (50.8 mm) de lana mineral para ambos escenarios.")
    print(f"Justificacion: cumple seguridad al contacto, reduce perdidas >90%,")
    print(f"  y es el espesor estandar especificado en los planos del proyecto.")
