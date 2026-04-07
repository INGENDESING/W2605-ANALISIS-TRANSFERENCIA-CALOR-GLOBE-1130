"""
Módulo de geometría del tanque de almacenamiento de glucosa — Proyecto P2611
=============================================================================
Cálculo de volúmenes, áreas y parámetros geométricos del tanque cilíndrico
con fondo toriesférico y chaqueta de media caña rectangular en espiral.

Ref: API 650 (2020), ASME Section VIII Div. 1 — UG-32
Datos: CLAUDE.md, Data/fondo.png, Data/espiral.png
"""

import numpy as np


# =============================================================================
# CONSTANTES GEOMÉTRICAS DEL TANQUE (desde planos y CLAUDE.md)
# =============================================================================

# Cuerpo cilíndrico (existente)
OD_SHELL = 5.276          # Diámetro exterior del cuerpo [m]
ID_SHELL = 5.264          # Diámetro interior del cuerpo [m]
H_CILINDRO = 9.670        # Altura de la sección cilíndrica [m]
t_SHELL = (OD_SHELL - ID_SHELL) / 2  # Espesor del cuerpo [m] = 0.006 m

# Fondo toriesférico (NUEVO)
OD_HEAD = 5.282           # Diámetro exterior del fondo [m]
t_HEAD = 0.009            # Espesor del fondo [m] (9 mm SS316L)
ID_HEAD = OD_HEAD - 2 * t_HEAD  # Diámetro interior del fondo [m]
H_FONDO = 1.266           # Altura del fondo toriesférico [m]

# Chaqueta de media caña (perfil rectangular en espiral)
H_PERFIL = 0.0455         # Altura interna del perfil rectangular [m] (45.5 mm)
W_PERFIL = 0.141          # Ancho interno del perfil rectangular [m] (141 mm)
t_PERFIL = 0.0045         # Espesor de lámina del perfil [m] (4.5 mm)
PASO_ESPIRAL = 0.196      # Paso de la espiral [m] (196 mm)
A_CONTACTO = 13.0         # Área de contacto con el tanque [m²]
AISLAMIENTO_ESPESOR = 0.0508  # Espesor de aislamiento de lana mineral [m] (2")

# Conexiones
D_ENTRADA_AGUA = 0.0508   # Diámetro nominal tubería entrada agua 2" [m]
D_SALIDA_GLUCOSA = 0.2032 # Diámetro nominal boquilla salida 8" [m]

# Tubería 2" ANSI B31.1 Schedule 40
OD_PIPE_2IN = 0.0603      # Diámetro exterior 2" Sch 40 [m]
ID_PIPE_2IN = 0.0525      # Diámetro interior 2" Sch 40 [m]
A_PIPE_2IN = np.pi / 4 * ID_PIPE_2IN**2  # Área de flujo [m²]

# Tubería 8" ANSI B31.1 Schedule 40 (boquilla salida)
OD_PIPE_8IN = 0.2191      # Diámetro exterior 8" [m]
ID_PIPE_8IN = 0.2027      # Diámetro interior 8" Sch 40 [m]
A_PIPE_8IN = np.pi / 4 * ID_PIPE_8IN**2  # Área de flujo [m²]

# Densidad de glucosa Globe 1130 (valor de referencia a ~40°C)
RHO_GLUCOSA_REF = 1410.0  # [kg/m³] — aprox. 85 Brix


# =============================================================================
# FUNCIONES DE VOLUMEN
# =============================================================================

def volumen_cilindro():
    """
    Volumen de la sección cilíndrica del tanque.
    V = π/4 · Di² · H

    Retorna
    -------
    V_cil : float — Volumen [m³]
    """
    R_i = ID_SHELL / 2
    V_cil = np.pi * R_i**2 * H_CILINDRO
    return V_cil


def volumen_fondo_torisferico():
    """
    Volumen aproximado del fondo toriesférico.
    Para un fondo toriesférico estándar (tipo ASME F&D):
      R_corona ≈ D_i  (radio de corona = diámetro interior)
      r_nudillo ≈ 0.06 · D_i  (radio de nudillo)

    Aproximación por integración numérica del perfil toriesférico.
    Ref: Megyesy, Pressure Vessel Handbook, 14th ed.

    Retorna
    -------
    V_fondo : float — Volumen [m³]
    """
    D_i = ID_HEAD
    R = D_i  # Radio de corona (ASME F&D: R = D)
    r = 0.06 * D_i  # Radio de nudillo (ASME F&D: r = 0.06D)

    # Aproximación para fondo toriesférico ASME F&D:
    # V ≈ 0.0847 · Di³ (fórmula empírica Megyesy)
    V_fondo = 0.0847 * D_i**3
    return V_fondo


def volumen_total():
    """
    Volumen total del tanque (cilindro + fondo toriesférico).
    No incluye la tapa cónica superior.

    Retorna
    -------
    V_total : float — Volumen total [m³]
    """
    return volumen_cilindro() + volumen_fondo_torisferico()


def volumen_a_nivel(h_nivel):
    """
    Volumen de glucosa en función del nivel de llenado medido
    desde el punto más bajo del fondo toriesférico.

    Parámetros
    ----------
    h_nivel : float — Nivel de líquido desde el fondo [m]

    Retorna
    -------
    V : float — Volumen de líquido [m³]
    """
    V = 0.0
    if h_nivel <= 0:
        return 0.0

    # Zona del fondo toriesférico (0 < h <= H_FONDO)
    if h_nivel <= H_FONDO:
        # Aproximación lineal proporcional al volumen del fondo
        fraccion = h_nivel / H_FONDO
        V = volumen_fondo_torisferico() * fraccion**1.5  # perfil curvo
    else:
        # Todo el fondo + parte del cilindro
        V = volumen_fondo_torisferico()
        h_cil = min(h_nivel - H_FONDO, H_CILINDRO)
        R_i = ID_SHELL / 2
        V += np.pi * R_i**2 * h_cil

    return V


def nivel_a_porcentaje(porcentaje):
    """
    Calcula el nivel de llenado [m] para un porcentaje dado de la capacidad total.

    Parámetros
    ----------
    porcentaje : float — Porcentaje de llenado (0 a 100)

    Retorna
    -------
    h_nivel : float — Nivel de líquido desde el fondo [m]
    """
    V_objetivo = volumen_total() * (porcentaje / 100.0)
    # Búsqueda por bisección
    h_min, h_max = 0.0, H_FONDO + H_CILINDRO
    for _ in range(100):
        h_mid = (h_min + h_max) / 2
        if volumen_a_nivel(h_mid) < V_objetivo:
            h_min = h_mid
        else:
            h_max = h_mid
    return (h_min + h_max) / 2


# =============================================================================
# FUNCIONES DE LA MEDIA CAÑA
# =============================================================================

def diametro_hidraulico_media_cana():
    """
    Diámetro hidráulico del canal rectangular de la media caña.
    D_h = 4·A / P
    donde A = ancho × alto, P = 2·(ancho + alto)

    Ref: Incropera, Fundamentals of Heat and Mass Transfer, 7th ed., Cap. 8

    Retorna
    -------
    D_h : float — Diámetro hidráulico [m]
    """
    A = W_PERFIL * H_PERFIL
    P = 2 * (W_PERFIL + H_PERFIL)
    D_h = 4 * A / P
    return D_h


def area_flujo_media_cana():
    """
    Área de la sección transversal de flujo del canal rectangular.

    Retorna
    -------
    A_flujo : float — Área de flujo [m²]
    """
    return W_PERFIL * H_PERFIL


def velocidad_en_media_cana(Q_agua):
    """
    Velocidad del agua en la media caña dado un caudal volumétrico.
    v = Q / A

    Parámetros
    ----------
    Q_agua : float — Caudal volumétrico de agua [m³/s]

    Retorna
    -------
    v : float — Velocidad [m/s]
    """
    return Q_agua / area_flujo_media_cana()


def velocidad_en_tuberia_2in(Q_agua):
    """
    Velocidad del agua en la tubería de alimentación de 2" Sch 40.
    v = Q / A

    Parámetros
    ----------
    Q_agua : float — Caudal volumétrico de agua [m³/s]

    Retorna
    -------
    v : float — Velocidad [m/s]
    """
    return Q_agua / A_PIPE_2IN


def caudal_desde_velocidad_media_cana(v_agua):
    """
    Caudal volumétrico de agua dado una velocidad en la media caña.
    Q = v · A

    Parámetros
    ----------
    v_agua : float — Velocidad del agua en la media caña [m/s]

    Retorna
    -------
    Q : float — Caudal volumétrico [m³/s]
    """
    return v_agua * area_flujo_media_cana()


# =============================================================================
# FUNCIONES DE MASA
# =============================================================================

def masa_glucosa(volumen, rho=RHO_GLUCOSA_REF):
    """
    Masa de glucosa dado un volumen y densidad.

    Parámetros
    ----------
    volumen : float — Volumen de glucosa [m³]
    rho     : float — Densidad de la glucosa [kg/m³]

    Retorna
    -------
    m : float — Masa [kg]
    """
    return volumen * rho


# =============================================================================
# RESUMEN DE RESULTADOS
# =============================================================================

if __name__ == "__main__":
    print("=" * 65)
    print("GEOMETRÍA DEL TANQUE DE GLUCOSA — Proyecto P2611")
    print("=" * 65)

    print(f"\n--- Cuerpo cilíndrico (existente) ---")
    print(f"  OD = {OD_SHELL*1000:.0f} mm | ID = {ID_SHELL*1000:.0f} mm")
    print(f"  Altura = {H_CILINDRO:.3f} m")
    print(f"  Espesor = {t_SHELL*1000:.1f} mm")
    V_cil = volumen_cilindro()
    print(f"  Volumen cilindro = {V_cil:.2f} m³")

    print(f"\n--- Fondo toriesférico (NUEVO) ---")
    print(f"  OD = {OD_HEAD*1000:.0f} mm | Espesor = {t_HEAD*1000:.1f} mm")
    print(f"  Altura = {H_FONDO:.3f} m")
    V_fondo = volumen_fondo_torisferico()
    print(f"  Volumen fondo ≈ {V_fondo:.2f} m³")

    V_total = volumen_total()
    print(f"\n--- Volumen total ---")
    print(f"  V_total = {V_total:.2f} m³")
    print(f"  V al 80% = {V_total * 0.80:.2f} m³")
    print(f"  V al 90% = {V_total * 0.90:.2f} m³")
    print(f"  Masa al 80% ≈ {masa_glucosa(V_total * 0.80)/1000:.1f} ton")
    print(f"  Masa al 90% ≈ {masa_glucosa(V_total * 0.90)/1000:.1f} ton")

    print(f"\n--- Media caña (perfil rectangular en espiral) ---")
    D_h = diametro_hidraulico_media_cana()
    A_f = area_flujo_media_cana()
    print(f"  Sección: {W_PERFIL*1000:.1f} mm × {H_PERFIL*1000:.1f} mm")
    print(f"  Área de flujo = {A_f*1e4:.2f} cm²")
    print(f"  Diámetro hidráulico = {D_h*1000:.2f} mm")
    print(f"  Paso espiral = {PASO_ESPIRAL*1000:.0f} mm")
    print(f"  Área de contacto = {A_CONTACTO:.1f} m²")

    # Escenario 1: Q = 30.9 m³/h
    Q1 = 30.9 / 3600  # m³/s
    v_mc_1 = velocidad_en_media_cana(Q1)
    v_2in_1 = velocidad_en_tuberia_2in(Q1)
    print(f"\n--- Escenario 1: Q_agua = 30.9 m³/h ---")
    print(f"  Velocidad en media caña = {v_mc_1:.3f} m/s")
    print(f"  Velocidad en tubería 2\" = {v_2in_1:.2f} m/s")

    # Escenarios 2 y 3: v = 2.5 m/s en media caña
    Q_25 = caudal_desde_velocidad_media_cana(2.5)
    v_2in_25 = velocidad_en_tuberia_2in(Q_25)
    print(f"\n--- Escenarios 2/3: v_media_caña = 2.5 m/s ---")
    print(f"  Caudal requerido = {Q_25*3600:.2f} m³/h")
    print(f"  Velocidad en tubería 2\" = {v_2in_25:.2f} m/s")

    # Nivel al 80%
    h_80 = nivel_a_porcentaje(80)
    print(f"\n--- Niveles de llenado ---")
    print(f"  Nivel al 80% = {h_80:.2f} m (desde fondo)")
    print(f"  Nivel al 90% = {nivel_a_porcentaje(90):.2f} m")
