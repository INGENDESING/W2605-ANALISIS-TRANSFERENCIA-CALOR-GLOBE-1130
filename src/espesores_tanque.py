"""
Modulo de calculo de espesores del tanque — Proyecto W2605
==========================================================
Calculo de espesores requeridos para el cuerpo cilindrico (API 650) y
el fondo toriesferico (ASME VIII Div.1 UG-32(e)).

Normativas:
  - API 650 (2020), Seccion 5.6.3.2 — One-Foot Method
  - ASME Section VIII Div.1 (2021), UG-32(e) — Torispherical Heads
  - ASME Section II Part D — Allowable Stresses
  - NSR-10 — Norma Sismo Resistente de Colombia
  - Informe P2543-PR-INF-002 REV0 — Corrosion allowance

Datos del tanque:
  Material:     SS316L (UNS S31603)
  OD cuerpo:    5276 mm, espesor original 6 mm
  OD fondo:     5282 mm, espesor 9 mm (NUEVO)
  H cilindro:   9670 mm
  H fondo:      1266 mm
  Llenado max:  90% para diseno
  Fluido:       Glucosa Globe 42 DE (~80.6 Brix, G = 1.42)
"""

import numpy as np


# =============================================================================
# CONSTANTES DEL MATERIAL — SS316L
# =============================================================================

# Propiedades mecanicas SS316L (ASME Section II Part D)
Fy_RT = 170.0       # Limite elastico a temperatura ambiente [MPa]
Fu_RT = 485.0       # Resistencia a la traccion a RT [MPa]
Fy_75C = 147.0      # Limite elastico a 75 C [MPa] (interpolado ASME II-D)
Fu_75C = 470.0      # Resistencia a la traccion a 75 C [MPa]

# Esfuerzo admisible API 650 (Table 5-2a, SS316L)
# Sd = min(2/3 * Fy, 2/5 * Fu) segun API 650 5.6.2.1
Sd_API650 = min(2/3 * Fy_RT, 2/5 * Fu_RT)  # [MPa] = min(113.3, 194.0)
Sd_API650_psi = Sd_API650 * 145.038  # Convertir a psi

# Esfuerzo admisible ASME VIII a 75 C (ASME II-D, Table 1A)
S_ASME_75C = 115.0   # [MPa] — valor interpolado

# Eficiencia de junta soldada
E_JUNTA = 0.85       # Junta tipo 1, radiografiada parcialmente (ASME VIII UW-12)

# Corrosion Allowance (Informe P2543)
CA_MM = 1.875         # [mm] — 30 anos a 0.0625 mm/ano
CA_M = CA_MM / 1000   # [m]
CA_IN = CA_MM / 25.4  # [in]


# =============================================================================
# GEOMETRIA DEL TANQUE
# =============================================================================

# Cuerpo cilindrico (existente)
OD_SHELL_MM = 5276.0     # Diametro exterior [mm]
OD_SHELL_FT = OD_SHELL_MM / 304.8  # [ft]
ID_SHELL_MM = 5264.0     # Diametro interior [mm]
t_SHELL_MM = 6.0         # Espesor original del cuerpo [mm]
t_SHELL_IN = t_SHELL_MM / 25.4  # [in]
H_CILINDRO_MM = 9670.0   # Altura del cilindro [mm]
H_CILINDRO_FT = H_CILINDRO_MM / 304.8  # [ft]

# Fondo toriesferico (NUEVO)
OD_HEAD_MM = 5282.0      # Diametro exterior [mm]
t_HEAD_MM = 9.0           # Espesor del fondo [mm]
t_HEAD_IN = t_HEAD_MM / 25.4  # [in]
ID_HEAD_MM = OD_HEAD_MM - 2 * t_HEAD_MM  # Diametro interior [mm]

# Fondo toriesferico — parametros geometricos (ASME F&D)
R_CORONA_MM = ID_HEAD_MM     # Radio de corona L = D_i (ASME standard)
r_NUDILLO_MM = 0.06 * ID_HEAD_MM  # Radio de nudillo r = 0.06*D_i
H_FONDO_MM = 1266.0          # Altura del fondo [mm]

# Propiedades del fluido
G_GLUCOSA = 1.42       # Gravedad especifica de la glucosa a ~20 C (ficha Ingredion)
RHO_GLUCOSA = 1425.0   # Densidad de referencia [kg/m3] (rho(20C) = 1424.6)


# =============================================================================
# API 650 — ONE-FOOT METHOD (CUERPO CILINDRICO)
# =============================================================================

def espesor_virola_api650(D_ft, H_ft, G, Sd_psi, CA_in, n_virola=1, h_virola_ft=None):
    """
    Espesor requerido para una virola del cuerpo cilindrico.
    API 650, Seccion 5.6.3.2 — One-Foot Method.

    td = 2.6 * D * (H - 1) * G / Sd + CA

    Parametros
    ----------
    D_ft      : float — Diametro nominal del tanque [ft]
    H_ft      : float — Altura del liquido medida desde el fondo de la virola
                        hasta el nivel maximo de diseno [ft]
    G         : float — Gravedad especifica del fluido
    Sd_psi    : float — Esfuerzo admisible de diseno [psi]
    CA_in     : float — Corrosion allowance [in]
    n_virola  : int   — Numero de virola (1 = inferior)
    h_virola_ft : float — Altura de cada virola [ft] (para calculo automatico de H)

    Retorna
    -------
    td_in : float — Espesor de diseno requerido [in]
    td_mm : float — Espesor de diseno requerido [mm]
    """
    # One-Foot Method: evaluar presion a 1 ft por encima del fondo de la virola
    td_in = 2.6 * D_ft * (H_ft - 1.0) * G / Sd_psi + CA_in
    td_mm = td_in * 25.4
    return td_in, td_mm


def analisis_cuerpo_cilindrico(n_virolas=4, h_virola_mm=2500.0, llenado_pct=90.0):
    """
    Analisis de espesores de todas las virolas del cuerpo cilindrico.
    API 650 One-Foot Method.

    Parametros
    ----------
    n_virolas   : int   — Numero de virolas
    h_virola_mm : float — Altura de cada virola [mm]
    llenado_pct : float — Porcentaje de llenado para diseno

    Retorna
    -------
    resultados : list of dict — Resultados por virola
    """
    D_ft = OD_SHELL_FT
    Sd_psi = Sd_API650_psi
    h_virola_ft = h_virola_mm / 304.8

    # Altura total de liquido al porcentaje de llenado
    H_total_mm = H_FONDO_MM + H_CILINDRO_MM * (llenado_pct / 100.0)
    H_total_ft = H_total_mm / 304.8

    resultados = []
    for i in range(n_virolas):
        # Elevacion del fondo de la virola (desde el fondo del cilindro)
        elev_fondo_virola_mm = i * h_virola_mm
        elev_fondo_virola_ft = elev_fondo_virola_mm / 304.8

        # Altura de liquido sobre el fondo de esta virola
        H_liquido_ft = H_total_ft - elev_fondo_virola_ft
        if H_liquido_ft < 0:
            H_liquido_ft = 0

        td_in, td_mm = espesor_virola_api650(D_ft, H_liquido_ft, G_GLUCOSA,
                                              Sd_psi, CA_IN)

        # Espesor minimo API 650 Table 5-6a (para D > 60 ft: 5/16")
        # Para D = 17.3 ft: minimo = 3/16" = 4.76 mm
        t_min_in = 3.0 / 16.0  # 0.1875 in = 4.76 mm
        t_min_mm = t_min_in * 25.4

        td_mm_final = max(td_mm, t_min_mm)
        td_in_final = td_mm_final / 25.4

        # Margen respecto al espesor existente
        margen_mm = t_SHELL_MM - td_mm_final
        margen_pct = (margen_mm / t_SHELL_MM) * 100

        resultados.append({
            'virola': i + 1,
            'elevacion_mm': elev_fondo_virola_mm,
            'H_liquido_ft': H_liquido_ft,
            'td_calc_mm': td_mm,
            'td_min_mm': t_min_mm,
            'td_requerido_mm': td_mm_final,
            'td_requerido_in': td_in_final,
            't_existente_mm': t_SHELL_MM,
            'margen_mm': margen_mm,
            'margen_pct': margen_pct,
            'cumple': margen_mm >= 0
        })

    return resultados


# =============================================================================
# ASME VIII — FONDO TORIESFERICO
# =============================================================================

def espesor_fondo_torisferico(P_MPa, L_mm, S_MPa, E, CA_mm):
    """
    Espesor requerido para fondo toriesferico.
    ASME VIII Div.1, UG-32(e):

    t = 0.885 * P * L / (S * E - 0.1 * P) + CA

    Parametros
    ----------
    P_MPa  : float — Presion de diseno interna [MPa]
    L_mm   : float — Radio de corona interior [mm]
    S_MPa  : float — Esfuerzo admisible a temperatura de diseno [MPa]
    E      : float — Eficiencia de junta soldada
    CA_mm  : float — Corrosion allowance [mm]

    Retorna
    -------
    t_req_mm : float — Espesor requerido [mm]
    """
    t_calc = 0.885 * P_MPa * L_mm / (S_MPa * E - 0.1 * P_MPa)
    t_req = t_calc + CA_mm
    return t_req


def analisis_fondo_torisferico(llenado_pct=90.0, factor_seguridad=1.5):
    """
    Analisis de espesor del fondo toriesferico por ASME VIII.

    La presion de diseno se calcula como la presion hidrostatica de la
    columna de glucosa al nivel de llenado mas un factor de seguridad.

    Parametros
    ----------
    llenado_pct       : float — Porcentaje de llenado para diseno
    factor_seguridad  : float — Factor de seguridad sobre la presion hidrostatica

    Retorna
    -------
    info : dict — Resultados detallados
    """
    # Presion hidrostatica en el fondo
    H_total_m = (H_FONDO_MM + H_CILINDRO_MM * (llenado_pct / 100.0)) / 1000.0
    g = 9.81  # [m/s2]
    P_hidro_Pa = RHO_GLUCOSA * g * H_total_m
    P_hidro_MPa = P_hidro_Pa / 1e6
    P_hidro_bar = P_hidro_Pa / 1e5

    # Presion de diseno con factor de seguridad
    P_diseno_MPa = P_hidro_MPa * factor_seguridad

    # Espesor requerido por ASME VIII UG-32(e)
    L_mm = R_CORONA_MM
    S_MPa = S_ASME_75C
    t_req_mm = espesor_fondo_torisferico(P_diseno_MPa, L_mm, S_MPa, E_JUNTA, CA_MM)

    # Margen
    margen_mm = t_HEAD_MM - t_req_mm
    margen_pct = (margen_mm / t_HEAD_MM) * 100

    info = {
        'H_total_m': H_total_m,
        'P_hidro_MPa': P_hidro_MPa,
        'P_hidro_bar': P_hidro_bar,
        'P_diseno_MPa': P_diseno_MPa,
        'P_diseno_bar': P_diseno_MPa * 10,
        'factor_seguridad': factor_seguridad,
        'L_corona_mm': L_mm,
        'r_nudillo_mm': r_NUDILLO_MM,
        'S_admisible_MPa': S_MPa,
        'E_junta': E_JUNTA,
        'CA_mm': CA_MM,
        't_calc_mm': t_req_mm - CA_MM,
        't_requerido_mm': t_req_mm,
        't_existente_mm': t_HEAD_MM,
        'margen_mm': margen_mm,
        'margen_pct': margen_pct,
        'cumple': margen_mm >= 0
    }
    return info


# =============================================================================
# VIDA UTIL Y CORROSION
# =============================================================================

def vida_util_corrosion(t_existente_mm, t_requerido_mm, tasa_corrosion_mm_anio=0.0625):
    """
    Calcula la vida util estimada por corrosion.

    Parametros
    ----------
    t_existente_mm       : float — Espesor existente [mm]
    t_requerido_mm       : float — Espesor minimo requerido (sin CA) [mm]
    tasa_corrosion_mm_anio : float — Tasa de corrosion [mm/ano]

    Retorna
    -------
    vida_anios : float — Vida util estimada [anos]
    """
    margen_corrosible = t_existente_mm - t_requerido_mm
    if margen_corrosible <= 0:
        return 0.0
    vida_anios = margen_corrosible / tasa_corrosion_mm_anio
    return vida_anios


# =============================================================================
# CARGAS DE VIENTO Y SISMO
# =============================================================================

def carga_viento_api650(V_kmh, D_m, H_m):
    """
    Presion de viento sobre el tanque segun API 650 Sec. 5.2.1.
    P_viento = 0.5 * rho_aire * V^2 * Cf

    Parametros
    ----------
    V_kmh : float — Velocidad maxima del viento [km/h]
    D_m   : float — Diametro del tanque [m]
    H_m   : float — Altura total del tanque [m]

    Retorna
    -------
    info : dict — Fuerzas y momentos por viento
    """
    V_ms = V_kmh / 3.6
    rho_aire = 1.057  # kg/m3 (Cali, 960 msnm)
    Cf = 0.6  # Factor de forma para cilindro (API 650)

    # Presion de viento
    P_viento = 0.5 * rho_aire * V_ms**2 * Cf  # [Pa]

    # Fuerza sobre el cuerpo cilindrico
    A_proyectada = D_m * H_m  # Area proyectada [m2]
    F_viento = P_viento * A_proyectada  # [N]
    M_volcamiento = F_viento * H_m / 2  # Momento en la base [N*m]

    info = {
        'V_ms': V_ms,
        'P_viento_Pa': P_viento,
        'P_viento_kPa': P_viento / 1000,
        'F_viento_kN': F_viento / 1000,
        'M_volcamiento_kNm': M_volcamiento / 1000
    }
    return info


def carga_sismica_nsr10(masa_total_kg, zona='intermedia'):
    """
    Fuerza sismica de diseno segun NSR-10.
    Simplificacion: F_sismo = Cs * W

    Parametros
    ----------
    masa_total_kg : float — Masa total del tanque + contenido [kg]
    zona          : str   — Zona sismica ('alta', 'intermedia', 'baja')

    Retorna
    -------
    info : dict — Fuerzas sismicas
    """
    g = 9.81
    W = masa_total_kg * g  # Peso total [N]

    # Coeficientes sismicos NSR-10 para Cali
    # Aa = 0.25, Av = 0.25 (zona intermedia)
    # Para tanque rigido: T < 0.5 s, Sa = 2.5 * Aa * Fa
    Aa = 0.25
    Fa = 1.0  # Suelo tipo C (asumido)
    R = 2.0   # Factor de reduccion para tanque (estructura no disipativa)
    I = 1.25  # Factor de importancia (almacenamiento de alimentos)

    Cs = 2.5 * Aa * Fa * I / R

    F_sismo = Cs * W  # [N]
    M_sismo = F_sismo * (H_CILINDRO_MM / 1000) * 0.5  # Momento en la base

    info = {
        'Aa': Aa,
        'Fa': Fa,
        'R': R,
        'I': I,
        'Cs': Cs,
        'W_kN': W / 1000,
        'F_sismo_kN': F_sismo / 1000,
        'M_sismo_kNm': M_sismo / 1000
    }
    return info


# =============================================================================
# RESUMEN COMPLETO
# =============================================================================

if __name__ == "__main__":
    print("=" * 78)
    print("ANALISIS DE ESPESORES — Proyecto W2605")
    print("=" * 78)

    # --- Cuerpo cilindrico ---
    print("\n--- CUERPO CILINDRICO (API 650 One-Foot Method) ---")
    print(f"Material: SS316L | Sd = {Sd_API650:.1f} MPa ({Sd_API650_psi:.0f} psi)")
    print(f"Diametro: OD = {OD_SHELL_MM:.0f} mm ({OD_SHELL_FT:.2f} ft)")
    print(f"Espesor existente: {t_SHELL_MM:.1f} mm ({t_SHELL_IN:.4f} in)")
    print(f"Corrosion allowance: {CA_MM:.3f} mm ({CA_IN:.4f} in)")
    print(f"Gravedad especifica: {G_GLUCOSA}")

    resultados_cuerpo = analisis_cuerpo_cilindrico(n_virolas=4, h_virola_mm=2417.5,
                                                    llenado_pct=90.0)

    print(f"\n{'Virola':>7} {'Elev [mm]':>10} {'H_liq [ft]':>10} {'t_req [mm]':>10} "
          f"{'t_exist [mm]':>12} {'Margen [mm]':>12} {'Cumple':>8}")
    print("-" * 75)
    for r in resultados_cuerpo:
        cumple_str = "SI" if r['cumple'] else "** NO **"
        print(f"{r['virola']:>7} {r['elevacion_mm']:>10.0f} {r['H_liquido_ft']:>10.2f} "
              f"{r['td_requerido_mm']:>10.2f} {r['t_existente_mm']:>12.1f} "
              f"{r['margen_mm']:>12.2f} {cumple_str:>8}")

    # --- Fondo toriesferico ---
    # ASME VIII ya incluye FS ~3.5 en el esfuerzo admisible S.
    # La presion de diseno es la presion hidrostatica real (sin factor adicional).
    # Se analizan dos condiciones: 90% fill (operacion) y 100% fill (prueba).
    for fill, fs_label in [(90.0, "Diseno (90%)"), (100.0, "Prueba (100%)")]:
        print(f"\n--- FONDO TORIESFERICO — {fs_label} (ASME VIII UG-32(e)) ---")
        info_fondo = analisis_fondo_torisferico(llenado_pct=fill, factor_seguridad=1.0)

        print(f"Altura total de liquido: {info_fondo['H_total_m']:.2f} m")
        print(f"Presion hidrostatica: {info_fondo['P_hidro_MPa']:.4f} MPa "
              f"({info_fondo['P_hidro_bar']:.3f} bar)")
        print(f"Presion de diseno: {info_fondo['P_diseno_MPa']:.4f} MPa")
        print(f"L = {info_fondo['L_corona_mm']:.0f} mm | "
              f"r = {info_fondo['r_nudillo_mm']:.1f} mm | "
              f"S = {info_fondo['S_admisible_MPa']:.0f} MPa | "
              f"E = {info_fondo['E_junta']}")
        print(f"Espesor calculado (sin CA): {info_fondo['t_calc_mm']:.2f} mm")
        print(f"Espesor requerido (+ CA): {info_fondo['t_requerido_mm']:.2f} mm")
        print(f"Espesor existente: {info_fondo['t_existente_mm']:.1f} mm")
        print(f"Margen: {info_fondo['margen_mm']:.2f} mm ({info_fondo['margen_pct']:.1f}%)")
        print(f"Cumple: {'SI' if info_fondo['cumple'] else '** NO **'}")

    # Caso critico: guardar referencia para vida util
    info_fondo = analisis_fondo_torisferico(llenado_pct=100.0, factor_seguridad=1.0)

    # --- Vida util ---
    print("\n--- VIDA UTIL POR CORROSION ---")
    # Cuerpo
    t_req_sin_CA = max(r['td_requerido_mm'] - CA_MM for r in resultados_cuerpo)
    vida_cuerpo = vida_util_corrosion(t_SHELL_MM, t_req_sin_CA)
    print(f"Cuerpo cilindrico: {vida_cuerpo:.0f} anos")

    # Fondo
    vida_fondo = vida_util_corrosion(t_HEAD_MM, info_fondo['t_calc_mm'])
    print(f"Fondo toriesferico: {vida_fondo:.0f} anos")

    # --- Cargas de viento ---
    print("\n--- CARGA DE VIENTO (API 650) ---")
    H_total_m = (H_FONDO_MM + H_CILINDRO_MM) / 1000
    info_viento = carga_viento_api650(120, OD_SHELL_MM/1000, H_total_m)
    print(f"Velocidad: 120 km/h ({info_viento['V_ms']:.1f} m/s)")
    print(f"Presion de viento: {info_viento['P_viento_kPa']:.3f} kPa")
    print(f"Fuerza sobre el tanque: {info_viento['F_viento_kN']:.1f} kN")
    print(f"Momento de volcamiento: {info_viento['M_volcamiento_kNm']:.1f} kN*m")

    # --- Carga sismica ---
    print("\n--- CARGA SISMICA (NSR-10, Cali) ---")
    # Masa del tanque vacio aprox + contenido
    masa_tanque = 5000  # kg (estimado acero)
    masa_glucosa = 1410 * 0.90 * 222.8  # kg al 90%
    info_sismo = carga_sismica_nsr10(masa_tanque + masa_glucosa)
    print(f"Coeficiente sismico Cs: {info_sismo['Cs']:.4f}")
    print(f"Peso total: {info_sismo['W_kN']:.0f} kN")
    print(f"Fuerza sismica: {info_sismo['F_sismo_kN']:.1f} kN")
    print(f"Momento sismico en la base: {info_sismo['M_sismo_kNm']:.1f} kN*m")

    print("\n" + "=" * 78)
    print("ANALISIS COMPLETADO")
    print("=" * 78)
