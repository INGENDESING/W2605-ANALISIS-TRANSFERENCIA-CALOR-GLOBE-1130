"""
Calculo de calor perdido - Tanque al 80% lleno
Proyecto P2611 - Analisis Termico del Tanque de Glucosa

El usuario reporta que el tanque aislado al 80% lleno pierde 3°C por el 
area cilindrica y conica (fondo toriesferico).

Este script calcula:
1. Areas de transferencia de calor (cilindrica + fondo)
2. Masa de glucosa al 80% de capacidad
3. Calor perdido basado en los 3°C de perdida
"""

import numpy as np
import sys
import os

# Anadir directorio padre al path para importar modulos del proyecto
sys.path.append(os.path.dirname(__file__))

from propiedades_glucosa import rho_glucosa, Cp_glucosa
from geometria_tanque import (
    OD_SHELL, ID_SHELL, H_CILINDRO, t_SHELL,
    OD_HEAD, ID_HEAD, H_FONDO, t_HEAD,
    volumen_total, volumen_a_nivel, nivel_a_porcentaje, masa_glucosa
)

# =============================================================================
# PARAMETROS DE CALCULO
# =============================================================================

# Datos del problema
T_OPERACION = 57.0          # Temperatura de operacion tipica [°C]
DELTA_T_PERDIDA = 3.0       # Perdida de temperatura reportada [°C]
PORCENTAJE_LLENADO = 80.0   # Nivel de llenado [%]

# Propiedades del aislamiento (lana mineral)
K_AISLAMIENTO = 0.045       # Conductividad termica [W/(m.K)] (valor conservador con humedad)
ESPESOR_AISLAMIENTO = 0.0508  # Espesor de aislamiento [m] (2 pulgadas)

# Conveccion exterior
H_EXT_NATURAL = 8.0         # Coef. conveccion natural [W/m2.K]
H_EXT_VIENTO = 15.0         # Coef. conveccion con viento ligero [W/m2.K]

# Temperatura ambiente
T_AMBIENTE = 26.5           # [°C] - Cali, Colombia


# =============================================================================
# PROPIEDADES DEL AIRE (para conveccion externa con viento)
# =============================================================================

def propiedades_aire(T_celsius):
    """
    Propiedades termofisicas del aire a temperatura dada.
    Correlaciones simplificadas para rango 20-60°C.
    
    Ref: Incropera, Fundamentals of Heat and Mass Transfer, 7th ed.
    
    Parametros
    ----------
    T_celsius : float - Temperatura [°C]
    
    Retorna
    -------
    dict : {k, rho, cp, mu, nu, Pr}
    """
    # Conductividad termica [W/(m·K)]
    k = 0.02364 + 7.0e-5 * T_celsius
    
    # Densidad [kg/m³] - gas ideal a ~1 atm
    rho = 1.287 - 0.0045 * T_celsius
    
    # Calor especifico [J/(kg·K)]
    cp = 1005.0  # Aproximadamente constante
    
    # Viscosidad dinamica [Pa·s] - correlacion Sutherland simplificada
    mu = 1.716e-5 * (1 + 0.0048 * (T_celsius - 20))
    
    # Viscosidad cinematica [m²/s]
    nu = mu / rho
    
    # Numero de Prandtl
    Pr = mu * cp / k
    
    return {'k': k, 'rho': rho, 'cp': cp, 'mu': mu, 'nu': nu, 'Pr': Pr}


def h_conveccion_viento(v_viento, T_pelicula, D_caracteristico):
    """
    Coeficiente de conveccion externo por viento sobre cilindro.
    Usa correlacion de Churchill-Bernstein para flujo externo.
    
    Churchill-Bernstein (valido para todo Re):
    Nu_D = 0.3 + (0.62*Re^0.5*Pr^(1/3))/(1+(0.4/Pr)^(2/3))^0.25 
           * [1+(Re/282000)^0.625]^0.8
    
    Ref: Churchill & Bernstein, J. Heat Transfer, 1977
         Incropera, 7th ed., Ec. 7.52
    
    Parametros
    ----------
    v_viento : float - Velocidad del viento [m/s]
    T_pelicula : float - Temperatura de pelicula [°C]
    D_caracteristico : float - Diametro exterior del cilindro [m]
    
    Retorna
    -------
    h_ext : float - Coeficiente convectivo [W/(m²·K)]
    Re : float - Numero de Reynolds
    Nu : float - Numero de Nusselt
    """
    # Propiedades del aire
    props = propiedades_aire(T_pelicula)
    k = props['k']
    nu = props['nu']
    Pr = props['Pr']
    
    # Numero de Reynolds
    Re = v_viento * D_caracteristico / nu
    
    # Correlacion Churchill-Bernstein
    term1 = 0.62 * (Re**0.5) * (Pr**(1.0/3.0))
    term2 = (1 + (0.4/Pr)**(2.0/3.0))**0.25
    term3 = (1 + (Re/282000.0)**0.625)**0.8
    
    Nu = 0.3 + (term1 / term2) * term3
    
    # Coeficiente convectivo
    h_ext = Nu * k / D_caracteristico
    
    return h_ext, Re, Nu


# =============================================================================
# FUNCIONES DE CALCULO DE AREAS
# =============================================================================

def area_cilindrica_exterior(h_cilindro=None):
    """
    Calcula el area exterior cilindrica del tanque.
    A = pi * OD * H
    
    Si h_cilindro es None, usa toda la altura del cilindro.
    """
    if h_cilindro is None:
        h_cilindro = H_CILINDRO
    
    A_cil = np.pi * OD_SHELL * h_cilindro
    return A_cil


def area_fondo_torisferico():
    """
    Calcula el area exterior del fondo toriesferico (aproximacion).
    
    Para un fondo toriesferico ASME F&D:
    - R_corona ~ Di (radio de corona = diametro interior)
    - r_nudillo ~ 0.06 * Di (radio de nudillo)
    
    Aproximacion del area superficial:
    A ~ 0.842 * Di^2 (formula empirica para ASME F&D)
    
    Ref: Megyesy, Pressure Vessel Handbook
    """
    D_i = ID_HEAD
    
    # Aproximacion del area de fondo toriesferico ASME F&D
    # Factor basado en relacion R/D = 1, r/D = 0.06
    A_fondo = 0.842 * D_i**2
    
    return A_fondo


def area_cilindrica_al_80porciento():
    """
    Calcula el area cilindrica correspondiente al 80% de llenado.
    
    El tanque tiene:
    - Fondo toriesferico: H_FONDO = 1.266 m
    - Cilindro: H_CILINDRO = 9.670 m
    - Altura total: ~10.936 m
    
    Al 80% de llenado, calculamos cuanto del cilindro esta cubierto.
    """
    from geometria_tanque import nivel_a_porcentaje
    
    # Obtener el nivel de liquido al 80%
    h_nivel = nivel_a_porcentaje(80.0)
    
    # El fondo tiene altura H_FONDO
    # Si el nivel esta por encima del fondo, el resto es cilindro
    if h_nivel > H_FONDO:
        h_cilindro_cubierto = h_nivel - H_FONDO
    else:
        h_cilindro_cubierto = 0.0
    
    # Area cilindrica cubierta por el liquido
    A_cil_cubierta = np.pi * OD_SHELL * h_cilindro_cubierto
    
    return A_cil_cubierta, h_cilindro_cubierto, h_nivel


def calcular_resistencia_termica_total():
    """
    Calcula la resistencia termica total por unidad de area.
    
    Resistencias en serie:
    R_total = R_conv_int + R_pared + R_aislamiento + R_conv_ext
    """
    from propiedades_glucosa import K_SS316L
    from geometria_tanque import t_HEAD
    
    # Conveccion interna (glucosa a pared) - valor conservador
    h_int = 28.0  # W/m2.K (conveccion natural glucosa viscosa)
    R_conv_int = 1.0 / h_int
    
    # Conduccion pared del tanque (SS316L)
    R_pared = t_HEAD / K_SS316L
    
    # Conduccion aislamiento
    R_aislamiento = ESPESOR_AISLAMIENTO / K_AISLAMIENTO
    
    # Conveccion externa
    R_conv_ext = 1.0 / H_EXT_VIENTO
    
    R_total = R_conv_int + R_pared + R_aislamiento + R_conv_ext
    
    return R_total, {
        'R_conv_int': R_conv_int,
        'R_pared': R_pared,
        'R_aislamiento': R_aislamiento,
        'R_conv_ext': R_conv_ext
    }


def calcular_perdida_temporal_5mm(v_viento, tiempo_horas=1.0, T_glucosa=None, T_ambiente=None):
    """
    Calcula la perdida de temperatura de la glucosa en un tiempo determinado
    con aislamiento de 5 mm y velocidad de viento dada.
    
    Parametros
    ----------
    v_viento : float - Velocidad del viento [m/s]
    tiempo_horas : float - Tiempo de exposicion [h] (default = 1)
    T_glucosa : float - Temperatura de operacion de la glucosa [°C] (default = T_OPERACION)
    T_ambiente : float - Temperatura ambiente [°C] (default = T_AMBIENTE)
    
    Retorna
    -------
    dict : Resultados del calculo termico
    """
    from propiedades_glucosa import K_SS316L
    from geometria_tanque import OD_SHELL
    
    # Usar valores por defecto si no se especifican
    if T_glucosa is None:
        T_glucosa = T_OPERACION
    if T_ambiente is None:
        T_ambiente = T_AMBIENTE
    
    # Parametros del escenario
    espesor_aisl_5mm = 0.005  # 5 mm en metros
    h_int = 28.0  # W/m2.K (conveccion natural glucosa, igual que en funcion original)
    
    # Temperatura de pelicula para propiedades del aire (aproximacion)
    T_pelicula = (T_glucosa + T_ambiente) / 2
    
    # Calcular h_ext con la velocidad del viento
    D_ext = OD_SHELL  # Diametro exterior del tanque
    h_ext, Re, Nu = h_conveccion_viento(v_viento, T_pelicula, D_ext)
    
    # Resistencias termicas
    R_conv_int = 1.0 / h_int
    R_pared = t_HEAD / K_SS316L
    R_aislamiento = espesor_aisl_5mm / K_AISLAMIENTO
    R_conv_ext = 1.0 / h_ext
    
    R_total = R_conv_int + R_pared + R_aislamiento + R_conv_ext
    
    # Coeficiente global U
    U_global = 1.0 / R_total
    
    # Areas de transferencia (igual que en main)
    A_fondo = area_fondo_torisferico()
    A_cil_80, h_cil_cubierto, h_nivel_total = area_cilindrica_al_80porciento()
    A_total = A_fondo + A_cil_80
    
    # Diferencia de temperatura driving
    Delta_T = T_glucosa - T_ambiente
    
    # Potencia perdida
    Q_perdida = U_global * A_total * Delta_T  # [W]
    
    # Masa de glucosa al 80%
    V_total = volumen_total()
    V_80 = V_total * 0.80
    rho_op = rho_glucosa(T_glucosa)
    Cp_op = Cp_glucosa(T_glucosa)
    masa_80 = V_80 * rho_op
    
    # Capacidad termica
    C_termica = masa_80 * Cp_op  # [J/°C]
    
    # Tiempo en segundos
    tiempo_seg = tiempo_horas * 3600.0
    
    # Perdida de temperatura en el tiempo
    # Q = C * delta_T / t  =>  delta_T = Q * t / C
    delta_T_glucosa = (Q_perdida * tiempo_seg) / C_termica  # [°C]
    
    # Energia perdida en el periodo [MJ]
    energia_perdida_MJ = (Q_perdida * tiempo_seg) / 1.0e6
    
    # Energia perdida por hora [MJ/h]
    energia_MJ_h = energia_perdida_MJ / tiempo_horas
    
    return {
        'v_viento': v_viento,
        'h_ext': h_ext,
        'Re': Re,
        'Nu': Nu,
        'U_global': U_global,
        'R_total': R_total,
        'R_aislamiento': R_aislamiento,
        'A_total': A_total,
        'Q_perdida_W': Q_perdida,
        'Q_perdida_kW': Q_perdida / 1000.0,
        'delta_T_glucosa': delta_T_glucosa,
        'energia_MJ': energia_perdida_MJ,
        'energia_MJ_h': energia_MJ_h,
        'tiempo_horas': tiempo_horas,
        'masa_glucosa': masa_80,
        'C_termica': C_termica
    }


# =============================================================================
# CALCULO PRINCIPAL
# =============================================================================

def main():
    print("=" * 78)
    print("CALCULO DE CALOR PERDIDO - TANQUE AL 80% LLENO")
    print("Proyecto P2611 - Analisis Termico del Tanque de Glucosa")
    print("=" * 78)
    
    # -------------------------------------------------------------------------
    # 1. GEOMETRIA Y AREAS
    # -------------------------------------------------------------------------
    print("\n1. GEOMETRIA DEL TANQUE")
    print("-" * 78)
    
    # Datos del tanque
    print("\n--- Dimensiones del tanque ---")
    print("  Cuerpo cilindrico:")
    print(f"    Diametro exterior (OD): {OD_SHELL:.3f} m")
    print(f"    Altura total: {H_CILINDRO:.3f} m")
    
    print("\n  Fondo toriesferico:")
    print(f"    Diametro exterior: {OD_HEAD:.3f} m")
    print(f"    Altura: {H_FONDO:.3f} m")
    
    # Area del fondo (siempre expuesto)
    A_fondo = area_fondo_torisferico()
    print(f"\n  Area fondo toriesferico: {A_fondo:.2f} m2")
    
    # Area cilindrica al 80%
    A_cil_80, h_cil_cubierto, h_nivel_total = area_cilindrica_al_80porciento()
    print("\n--- Al 80% de llenado ---")
    print(f"  Nivel total de liquido: {h_nivel_total:.2f} m desde el fondo")
    print(f"  Altura del fondo: {H_FONDO:.2f} m")
    print(f"  Altura cilindrica cubierta: {h_cil_cubierto:.2f} m")
    print(f"  Area cilindrica cubierta: {A_cil_80:.2f} m2")
    
    # Area total expuesta al liquido
    A_total_expuesta = A_fondo + A_cil_80
    print(f"\n  AREA TOTAL EXPUESTA (fondo + cilindro al 80%): {A_total_expuesta:.2f} m2")
    
    # -------------------------------------------------------------------------
    # 2. VOLUMEN Y MASA DE GLUCOSA
    # -------------------------------------------------------------------------
    print("\n\n2. CONTENIDO DE GLUCOSA AL 80%")
    print("-" * 78)
    
    V_total = volumen_total()
    V_80 = V_total * 0.80
    
    # Propiedades de la glucosa a temperatura de operacion
    rho_op = rho_glucosa(T_OPERACION)
    Cp_op = Cp_glucosa(T_OPERACION)
    
    masa_80 = V_80 * rho_op
    
    print(f"  Volumen total del tanque: {V_total:.2f} m3")
    print(f"  Volumen al 80%: {V_80:.2f} m3")
    print(f"\n  Propiedades de la glucosa a {T_OPERACION}°C:")
    print(f"    Densidad (rho): {rho_op:.1f} kg/m3")
    print(f"    Calor especifico (Cp): {Cp_op:.1f} J/(kg.C)")
    print(f"\n  Masa de glucosa al 80%: {masa_80/1000:.2f} toneladas")
    print(f"                         ({masa_80:.0f} kg)")
    
    # -------------------------------------------------------------------------
    # 3. CALCULO DEL CALOR PERDIDO (basado en DT = 3°C)
    # -------------------------------------------------------------------------
    print("\n\n3. CALCULO DEL CALOR PERDIDO")
    print("-" * 78)
    print("\n  Datos del problema:")
    print(f"    Temperatura de operacion: {T_OPERACION}°C")
    print(f"    Perdida de temperatura reportada: {DELTA_T_PERDIDA}°C")
    print(f"    Temperatura ambiente: {T_AMBIENTE}°C")
    
    # Calor perdido usando Q = m * Cp * DT
    # Esto representa la energia que debe perder la masa de glucosa para bajar 3°C
    Q_perdido_por_masa = masa_80 * Cp_op * DELTA_T_PERDIDA
    
    print("\n  --- Metodo 1: Basado en perdida de temperatura de la masa ---")
    print("    Q = m * Cp * DT")
    print(f"    Q = {masa_80:.0f} kg * {Cp_op:.1f} J/(kg.C) * {DELTA_T_PERDIDA}°C")
    print(f"    Q = {Q_perdido_por_masa:.2f} J")
    print(f"    Q = {Q_perdido_por_masa/1000:.2f} kJ")
    print(f"    Q = {Q_perdido_por_masa/3.6e6:.2f} kWh")
    
    # Convertir a potencia (si asumimos un tiempo de enfriamiento tipico)
    # Asumimos que la perdida de 3°C ocurre en un periodo de tiempo
    # Por ejemplo, si ocurre en 1 hora:
    tiempo_horas = 1.0
    P_perdida_kW = (Q_perdido_por_masa / 1000) / (tiempo_horas * 3600)
    
    print(f"\n    Si esta perdida ocurre en {tiempo_horas} hora:")
    print(f"    Potencia perdida = {P_perdida_kW:.2f} kW")
    
    # -------------------------------------------------------------------------
    # 4. ANALISIS TERMICO DETALLADO
    # -------------------------------------------------------------------------
    print("\n\n4. ANALISIS TERMICO DETALLADO")
    print("-" * 78)
    
    # Resistencias termicas
    R_total, resistencias = calcular_resistencia_termica_total()
    
    print("\n  Resistencias termicas por unidad de area:")
    print(f"    R_conv_interna:  {resistencias['R_conv_int']:.4f} m2.K/W")
    print(f"    R_pared (SS316L): {resistencias['R_pared']:.6f} m2.K/W")
    print(f"    R_aislamiento:   {resistencias['R_aislamiento']:.4f} m2.K/W")
    print(f"    R_conv_externa:  {resistencias['R_conv_ext']:.4f} m2.K/W")
    print(f"    R_TOTAL:         {R_total:.4f} m2.K/W")
    
    # Coeficiente global U
    U_global = 1.0 / R_total
    print("\n  Coeficiente global de transferencia de calor:")
    print(f"    U = 1/R_total = {U_global:.2f} W/(m2.K)")
    
    # Flujo de calor
    Delta_T = T_OPERACION - T_AMBIENTE
    q_flujo = U_global * Delta_T  # W/m2
    
    print("\n  Diferencia de temperatura:")
    print(f"    DT = T_op - T_amb = {T_OPERACION}°C - {T_AMBIENTE}°C = {Delta_T:.1f}°C")
    
    print("\n  Flujo de calor:")
    print(f"    q = U * DT = {U_global:.2f} * {Delta_T:.1f} = {q_flujo:.2f} W/m2")
    
    # Potencia total perdida
    Q_perdida_total = q_flujo * A_total_expuesta
    
    print("\n  Potencia total perdida:")
    print(f"    Q = q * A_total = {q_flujo:.2f} W/m2 * {A_total_expuesta:.2f} m2")
    print(f"    Q = {Q_perdida_total:.2f} W")
    print(f"    Q = {Q_perdida_total/1000:.2f} kW")
    
    # -------------------------------------------------------------------------
    # 5. TIEMPO PARA PERDER 3°C
    # -------------------------------------------------------------------------
    print("\n\n5. TIEMPO PARA PERDER 3°C")
    print("-" * 78)
    
    # Capacidad termica total
    C_total = masa_80 * Cp_op  # J/°C
    
    # Tiempo para perder 3°C con la potencia calculada
    # Q = C * DT, pero Q tambien = P * t
    # Entonces: t = C * DT / P
    
    tiempo_s = Q_perdido_por_masa / Q_perdida_total
    tiempo_h = tiempo_s / 3600
    tiempo_d = tiempo_h / 24
    
    print("\n  Capacidad termica total (C = m * Cp):")
    print(f"    C = {masa_80:.0f} kg * {Cp_op:.1f} J/(kg.C)")
    print(f"    C = {C_total:.2f} J/C = {C_total/1000:.2f} kJ/C")
    
    print("\n  Energia a perder para bajar 3°C:")
    print(f"    Q = C * DT = {C_total:.2f} * {DELTA_T_PERDIDA}")
    print(f"    Q = {Q_perdido_por_masa:.2f} J = {Q_perdido_por_masa/1000:.2f} kJ")
    
    print("\n  Tiempo estimado para perder 3°C:")
    print(f"    t = Q / P = {Q_perdido_por_masa/1000:.2f} kJ / {Q_perdida_total/1000:.2f} kW")
    print(f"    t = {tiempo_s:.0f} segundos")
    print(f"    t = {tiempo_h:.2f} horas")
    print(f"    t = {tiempo_d:.2f} dias")
    
    # -------------------------------------------------------------------------
    # 6. RESUMEN EJECUTIVO
    # -------------------------------------------------------------------------
    print("\n\n" + "=" * 78)
    print("RESUMEN EJECUTIVO")
    print("=" * 78)
    
    print(f"""
    CONDICIONES:
    - Tanque de glucosa al 80% de capacidad
    - Volumen de glucosa: {V_80:.2f} m3
    - Masa de glucosa: {masa_80/1000:.2f} toneladas
    - Temperatura de operacion: {T_OPERACION}°C
    - Perdida de temperatura reportada: {DELTA_T_PERDIDA}°C
    
    AREAS DE TRANSFERENCIA DE CALOR:
    - Area fondo toriesferico: {A_fondo:.2f} m2
    - Area cilindrica (al 80%): {A_cil_80:.2f} m2
    - Area TOTAL: {A_total_expuesta:.2f} m2
    
    RESULTADOS DEL CALCULO TERMICO:
    - Coeficiente global U: {U_global:.2f} W/(m2.K)
    - Potencia de perdida: {Q_perdida_total/1000:.2f} kW ({Q_perdida_total:.0f} W)
    - Flujo de calor: {q_flujo:.2f} W/m2
    
    CALOR PERDIDO PARA DT = 3°C:
    - Energia perdida: {Q_perdido_por_masa/1000:.2f} kJ ({Q_perdido_por_masa/3.6e6:.2f} kWh)
    - Tiempo estimado para perder 3°C: {tiempo_h:.1f} horas ({tiempo_d:.2f} dias)
    
    NOTA: Este calculo asume:
    - Aislamiento de 2" (50.8 mm) de lana mineral
    - Condiciones de viento ligero (h_ext = 15 W/m2K)
    - Temperatura ambiente de {T_AMBIENTE}°C (Cali, Colombia)
    """)
    
    # Escenarios con diferentes espesores de aislamiento
    print("\n" + "-" * 78)
    print("ANALISIS DE SENSIBILIDAD - ESPESOR DE AISLAMIENTO")
    print("-" * 78)
    
    espesores = [0.025, 0.038, 0.051, 0.076, 0.102]  # m
    print("\n{0:>12} {1:>12} {2:>12} {3:>15}".format("Espesor", "U_global", "P_perdida", "Tiempo (3°C)"))
    print("{0:>12} {1:>12} {2:>12} {3:>15}".format("[mm]", "[W/m2K]", "[kW]", "[horas]"))
    print("-" * 55)
    
    for esp in espesores:
        R_aisl = esp / K_AISLAMIENTO
        R_tot = resistencias['R_conv_int'] + resistencias['R_pared'] + R_aisl + resistencias['R_conv_ext']
        U = 1.0 / R_tot
        P = U * Delta_T * A_total_expuesta
        t_3c = (masa_80 * Cp_op * 3.0) / P / 3600
        
        print("{0:>12.1f} {1:>12.2f} {2:>12.2f} {3:>15.1f}".format(esp*1000, U, P/1000, t_3c))
    
    print("\n" + "=" * 78)

    # ==========================================================================
    # ESCENARIO 1: AISLAMIENTO 5mm - PERDIDA DE TEMPERATURA EN 1 HORA
    # Con condiciones ambientales de Cali (velocidades de viento variables)
    # ==========================================================================
    print("\n\n" + "=" * 78)
    print("ESCENARIO 1: AISLAMIENTO 5mm - PERDIDA DE TEMPERATURA EN 1 HORA")
    print("Condiciones ambientales de Cali, Colombia")
    print("=" * 78)
    
    print("\nParametros del escenario:")
    print(f"  - Aislamiento: 5 mm (lana mineral, k = {K_AISLAMIENTO} W/m.K)")
    print(f"  - Temperatura ambiente: {T_AMBIENTE}°C")
    print(f"  - Temperatura glucosa: {T_OPERACION}°C")
    print(f"  - Delta T driving: {T_OPERACION - T_AMBIENTE:.1f}°C")
    print(f"  - Masa glucosa al 80%: {masa_80/1000:.1f} toneladas")
    
    # Velocidades de viento a evaluar
    velocidades_viento = [1.0, 2.0, 2.5, 3.0]  # m/s
    
    print("\n" + "-" * 95)
    print("Resultados para diferentes velocidades de viento:")
    print("-" * 95)
    
    # Header de tabla estilo Elsevier
    header = "{0:>8} {1:>12} {2:>12} {3:>12} {4:>12} {5:>12} {6:>12}".format(
        "V_viento", "h_ext", "U_global", "Q_perdida", "Delta_T", "Energia", "Energia"
    )
    subheader = "{0:>8} {1:>12} {2:>12} {3:>12} {4:>12} {5:>12} {6:>12}".format(
        "(m/s)", "(W/m2.K)", "(W/m2.K)", "(kW)", "(°C/h)", "(MJ/h)", "(MJ/1h)"
    )
    print(header)
    print(subheader)
    print("-" * 95)
    
    # Almacenar resultados para CSV
    resultados_escenario1 = []
    
    for v in velocidades_viento:
        res = calcular_perdida_temporal_5mm(v, tiempo_horas=1.0)
        
        print("{0:>8.1f} {1:>12.2f} {2:>12.2f} {3:>12.2f} {4:>12.3f} {5:>12.2f} {6:>12.2f}".format(
            res['v_viento'],
            res['h_ext'],
            res['U_global'],
            res['Q_perdida_kW'],
            res['delta_T_glucosa'],
            res['energia_MJ_h'],
            res['energia_MJ']
        ))
        
        resultados_escenario1.append({
            'velocidad_viento_m_s': res['v_viento'],
            'h_ext_W_m2K': res['h_ext'],
            'U_global_W_m2K': res['U_global'],
            'Q_perdida_kW': res['Q_perdida_kW'],
            'delta_T_C_por_h': res['delta_T_glucosa'],
            'energia_MJ_por_h': res['energia_MJ_h']
        })
    
    print("-" * 95)
    
    # Guardar resultados en CSV
    import csv
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'results', 'perdidas_aislamiento_5mm_cali.csv')
    csv_path = os.path.abspath(csv_path)
    
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Escenario 1: Aislamiento 5mm - Condiciones Cali'])
        writer.writerow([''])
        writer.writerow(['Parametros'])
        writer.writerow(['Temperatura ambiente (°C)', T_AMBIENTE])
        writer.writerow(['Temperatura glucosa (°C)', T_OPERACION])
        writer.writerow(['Espesor aislamiento (mm)', 5])
        writer.writerow(['Conductividad aislamiento (W/m.K)', K_AISLAMIENTO])
        writer.writerow(['Masa glucosa al 80% (ton)', round(masa_80/1000, 2)])
        writer.writerow([''])
        writer.writerow(['Velocidad viento (m/s)', 'h_ext (W/m2.K)', 'U_global (W/m2.K)', 
                         'Q_perdida (kW)', 'Delta_T (°C/h)', 'Energia (MJ/h)'])
        
        for r in resultados_escenario1:
            writer.writerow([
                r['velocidad_viento_m_s'],
                round(r['h_ext_W_m2K'], 2),
                round(r['U_global_W_m2K'], 2),
                round(r['Q_perdida_kW'], 2),
                round(r['delta_T_C_por_h'], 3),
                round(r['energia_MJ_por_h'], 2)
            ])
    
    print(f"\nResultados exportados a: {csv_path}")
    
    # ======================================================================
    # ESCENARIO 2: ENERGIA PERDIDA POR DELTA T = 3°C
    # ======================================================================
    print("\n\n" + "=" * 78)
    print("ESCENARIO 2: ENERGIA PERDIDA SI LA GLUCOSA BAJA 3°C")
    print("(Independiente del tiempo y condiciones ambientales)")
    print("=" * 78)
    
    # Este calculo ya se hizo anteriormente, solo lo presentamos de nuevo
    Q_3C_J = masa_80 * Cp_op * 3.0
    Q_3C_MJ = Q_3C_J / 1.0e6
    Q_3C_kWh = Q_3C_J / 3.6e6
    
    print(f"\nCalculo:")
    print(f"  Q = m x Cp x DeltaT")
    print(f"  Q = {masa_80:.0f} kg x {Cp_op:.1f} J/(kg.C) x 3.0C")
    print(f"  Q = {Q_3C_J:.2f} J")
    print(f"\nResultado:")
    print(f"  Energia perdida = {Q_3C_MJ:.2f} MJ")
    print(f"                  = {Q_3C_kWh:.2f} kWh")
    
    # Comparacion entre escenarios
    print("\n" + "=" * 78)
    print("COMPARACION ENTRE ESCENARIOS")
    print("=" * 78)
    
    print("\nPara perder 3°C de temperatura:")
    print("-" * 60)
    
    # Usar el resultado de viento 2.5 m/s como referencia
    res_ref = calcular_perdida_temporal_5mm(2.5, tiempo_horas=1.0)
    tiempo_para_3C_h = 3.0 / res_ref['delta_T_glucosa']
    
    print(f"  Con aislamiento 5mm y viento 2.5 m/s:")
    print(f"    - Perdida de temperatura: {res_ref['delta_T_glucosa']:.3f}°C por hora")
    print(f"    - Tiempo para perder 3°C: {tiempo_para_3C_h:.1f} horas")
    print(f"    - Energia perdida en ese tiempo: {res_ref['energia_MJ_h'] * tiempo_para_3C_h:.2f} MJ")
    print(f"\n  Comparacion con escenario 2 (3°C):")
    print(f"    - Energia calculada (Esc. 2): {Q_3C_MJ:.2f} MJ")
    print(f"    - Coincidencia: {'Si' if abs(Q_3C_MJ - res_ref['energia_MJ_h'] * tiempo_para_3C_h) < 0.1 else 'Verificar'}")
    
    print("\n" + "=" * 78)


if __name__ == "__main__":
    main()
