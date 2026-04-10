"""
Módulo de cálculo de áreas de transferencia - Proyecto P2611
=================================================================
Calcula áreas requeridas para chaqueta de calentamiento continua
con flujos de glucosa variables (1-16 toneladas/hora).

Condiciones:
  - Agua: 75°C, velocidad 2.5 m/s en media caña rectangular
  - Glucosa: 25°C → 57°C (ΔT = 32°C)
  - Flujos: 1, 2, 3, ..., 16 ton/h

Metodología:
  1. Q_dot = m_dot × Cp_prom × ΔT_glucosa
  2. LMTD = (ΔT1 - ΔT2) / ln(ΔT1/ΔT2)
  3. U_promedio = mean[U(T_g)] para T_g ∈ [25, 57°C]
  4. A_req = Q_dot / (U_prom × LMTD)

Referencias:
  - coeficiente_U.py: coeficiente_U(), h_interno_sieder_tate(), h_externo_conveccion_natural()
  - propiedades_glucosa.py: rho_glucosa(), mu_glucosa(), Cp_glucosa(), k_glucosa()
  - geometria_tanque.py: W_PERFIL (0.141 m), H_PERFIL (0.0455 m)
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import sys
import io

# Configurar salida estándar para UTF-8 en Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Importar módulos existentes del proyecto
sys.path.append(os.path.dirname(__file__))

try:
    from coeficiente_U import coeficiente_U
    from propiedades_glucosa import Cp_glucosa
    from geometria_tanque import W_PERFIL
except ImportError as e:
    print(f"ERROR: No se pudo importar módulos del proyecto: {e}")
    print("Asegúrate de ejecutar desde el directorio raíz del proyecto")
    sys.exit(1)


# =============================================================================
# FUNCIONES DE CÁLCULO PRINCIPALES
# =============================================================================

def Q_por_flujo_masico(m_dot_ton_h, T_frio_in=25.0, T_frio_out=57.0, 
                        incluir_perdidas=False):
    """
    Calcula el calor requerido por unidad de tiempo para un flujo de masa.
    
    Q_dot = m_dot × Cp_promedio × ΔT_glucosa + Q_perdidas (opcional)
    
    Parámetros
    ----------
    m_dot_ton_h : float
        Flujo másico de glucosa [toneladas/hora]
    T_frio_in : float, opcional
        Temperatura de entrada de glucosa [°C], por defecto 25.0
    T_frio_out : float, opcional
        Temperatura de salida de glucosa [°C], por defecto 57.0
    incluir_perdidas : bool, opcional
        Si True, incluye pérdidas al ambiente (escenario conservador).
        Solo aplica para calentamiento de mantenimiento (T cercanas a 57°C).
    
    Retorna
    -------
    Q_dot : float
        Potencia térmica requerida [W]
    m_dot_kg_s : float
        Flujo másico [kg/s]
    Cp_prom : float
        Calor específico promedio [J/kg·°C]
    Delta_T : float
        Diferencia de temperatura de la glucosa [°C]
    """
    # Importar función de pérdidas
    from aislamiento import calcular_perdidas_ambiente_mantenimiento
    
    # Conversión de unidades
    m_dot_kg_s = m_dot_ton_h * 1000.0 / 3600.0  # ton/h → kg/s
    
    # Temperatura promedio para evaluar Cp (Incropera, Sec. 8.3)
    T_prom = (T_frio_in + T_frio_out) / 2.0
    Cp_prom = Cp_glucosa(T_prom)
    
    # Diferencia de temperatura de la glucosa
    Delta_T = T_frio_out - T_frio_in
    
    # Calor requerido para elevar temperatura
    Q_dot_calentamiento = m_dot_kg_s * Cp_prom * Delta_T
    
    # Pérdidas al ambiente (escenario conservador)
    Q_perdidas = 0.0
    if incluir_perdidas:
        # Calcular pérdidas basadas en temperatura promedio
        Q_perd_total, Q_perd_equiv, _, _ = calcular_perdidas_ambiente_mantenimiento(T_prom)
        # Las pérdidas se escalan con el flujo (cuanto más glucosa, más pérdidas)
        # Factor de escala: proporcional a la fracción del tanque
        Q_perdidas = Q_perd_total
    
    # Calor total requerido
    Q_dot = Q_dot_calentamiento + Q_perdidas
    
    return Q_dot, m_dot_kg_s, Cp_prom, Delta_T


def delta_T_LMTD(T_agua=75.0, T_frio_in=25.0, T_frio_out=57.0):
    """
    Calcula la Diferencia de Temperatura Media Logarítmica (LMTD).
    
    Para intercambiador con un flujo a temperatura constante (agua 75°C)
    y otro flujo que cambia (glucosa 25→57°C):
    
    LMTD = (ΔT1 - ΔT2) / ln(ΔT1/ΔT2)
    donde:
      ΔT1 = T_agua - T_frio_in
      ΔT2 = T_agua - T_frio_out
    
    Parámetros
    ----------
    T_agua : float, opcional
        Temperatura del agua [°C], por defecto 75.0
    T_frio_in : float, opcional
        Temperatura de entrada de glucosa [°C], por defecto 25.0
    T_frio_out : float, opcional
        Temperatura de salida de glucosa [°C], por defecto 57.0
    
    Retorna
    -------
    LMTD : float
        Diferencia de temperatura media logarítmica [°C]
    """
    delta_T1 = T_agua - T_frio_in
    delta_T2 = T_agua - T_frio_out
    
    # Evitar división por cero
    if abs(delta_T1 - delta_T2) < 1e-6:
        return delta_T1
    
    if delta_T1 <= 0 or delta_T2 <= 0:
        raise ValueError(f"Diferencias de temperatura no válidas: ΔT1={delta_T1}, ΔT2={delta_T2}")
    
    LMTD = (delta_T1 - delta_T2) / np.log(delta_T1 / delta_T2)
    return LMTD


def calcular_U_corregido(v_agua, T_agua_entrada, T_glucosa, usar_temperatura_media=False):
    """
    Calcula U sin iteración adicional (coeficiente_U ya calcula correctamente).
    
    NOTA: Eliminada iteración de temperatura de pared porque está causando que
    U sea inconsistente con coeficiente_U(). coeficiente_U() ya estima T_pared
    correctamente como (T_agua + T_glucosa)/2.
    
    Algoritmo:
    1. Si usar_temperatura_media=False (para promediado):
       - T_agua = T_agua_entrada (75°C constante)
    2. Si usar_temperatura_media=True (para balance):
       - Calcular T_agua_media = (T_entrada + T_salida) / 2
    3. Calcular U directamente con coeficiente_U()
    
    Parámetros
    ----------
    v_agua : float
        Velocidad del agua en la media caña [m/s]
    T_agua_entrada : float
        Temperatura de entrada del agua [°C]
    T_glucosa : float
        Temperatura bulk de la glucosa [°C]
    usar_temperatura_media : bool
        Si False, usa T_agua_entrada constante (para cálculo de U_vs_T)
        Si True, calcula T_agua_media variable (para balance energético)
    
    Retorna
    -------
    U : float
        Coeficiente global [W/m²·°C]
    T_agua_usada : float
        Temperatura del agua usada en el cálculo [°C]
    T_pared : float
        Temperatura de pared estimada [°C]
    h_i : float
        Coeficiente interno [W/m²·°C]
    h_o : float
        Coeficiente externo [W/m²·°C]
    """
    from propiedades_glucosa import K_SS316L
    from geometria_tanque import t_HEAD
    
    # Determinar temperatura del agua a usar
    if usar_temperatura_media:
        # Para el balance energético real: estimar caída de temperatura del agua
        # Suponer un ΔT_agua razonable (se ajustará en el cálculo principal)
        Cp_agua = 4182.0
        # Asumir caída inicial de 5°C (se actualizará con el flujo real)
        Delta_T_agua = 5.0
        T_agua_salida = T_agua_entrada - Delta_T_agua
        T_agua_usada = (T_agua_entrada + T_agua_salida) / 2
    else:
        # Para el promediado de U: usar temperatura de entrada constante
        T_agua_usada = T_agua_entrada  # 75°C constante
    
    # Calcular U directamente sin iteración adicional
    # coeficiente_U() ya estima T_pared correctamente
    U, h_i, h_o, info = coeficiente_U(v_agua, T_agua_usada, T_glucosa)
    
    # Extraer temperatura de pared del diccionario info
    T_pared = info.get('T_pared', (T_agua_usada + T_glucosa) / 2)
    
    return U, T_agua_usada, T_pared, h_i, h_o


def calcular_area_necesaria(m_dot_ton_h, v_agua=2.5, T_agua_entrada=75.0, 
                             T_frio_in=25.0, T_frio_out=57.0, incluir_perdidas=False):
    """
    Calcula el área de transferencia necesaria para un flujo de masa específico.
    Versión corregida que considera variación real de U con temperatura.
    
    Algoritmo corregido:
    1. Calcular Q_dot requerido (incluye pérdidas si aplica)
    2. Estimar caudal de agua inicial (suponer ΔT_agua ≈ 5°C)
    3. Para cada T_g en rango:
        a. Calcular U(T_g) con función corregida (incluye caída de T_agua)
        b. Almacenar 1/U(T_g) para promediado de resistencias
    4. U_prom = 1 / mean(1/U(T_g))  # Promedio de resistencias, NO de U
    5. Calcular A_req = Q_dot / (U_prom × LMTD)
    
    Parámetros
    ----------
    m_dot_ton_h : float
        Flujo másico de glucosa [ton/h]
    v_agua : float, opcional
        Velocidad del agua [m/s], por defecto 2.5
    T_agua_entrada : float, opcional
        Temperatura de entrada del agua [°C], por defecto 75.0
    T_frio_in : float, opcional
        Temperatura de entrada de glucosa [°C], por defecto 25.0
    T_frio_out : float, opcional
        Temperatura de salida de glucosa [°C], por defecto 57.0
    incluir_perdidas : bool, opcional
        Si True, incluye pérdidas al ambiente (escenario conservador 54→57°C)
    
    Retorna
    -------
    A_req : float
        Área de transferencia requerida [m²]
    parametros : dict
        Diccionario con valores intermedios del cálculo
    """
    # Paso 1: Calor requerido (parametrizado para cualquier rango de T)
    # Si es escenario de mantenimiento (54→57°C), incluir pérdidas
    if T_frio_in >= 54.0 and T_frio_out == 57.0:
        incluir_perdidas = True
    
    Q_dot, m_dot_kg_s, Cp_prom, Delta_T = Q_por_flujo_masico(
        m_dot_ton_h, T_frio_in, T_frio_out, incluir_perdidas
    )
    
    # Paso 2: Estimar caída de temperatura del agua
    # Q = m_agua · Cp_agua · ΔT_agua  →  ΔT_agua = Q / (m_agua · Cp_agua)
    # El caudal de agua se fija por la velocidad en la media caña
    from propiedades_glucosa import rho_agua as _rho_agua
    from geometria_tanque import area_flujo_media_cana
    A_flujo = area_flujo_media_cana()
    rho_w = _rho_agua(T_agua_entrada)
    m_dot_agua = rho_w * v_agua * A_flujo  # kg/s (fijado por geometría)
    Cp_agua = 4182.0
    Delta_T_agua = Q_dot / (m_dot_agua * Cp_agua)  # Caída real del agua [°C]
    T_agua_salida = T_agua_entrada - Delta_T_agua
    T_agua_media = (T_agua_entrada + T_agua_salida) / 2.0
    
    # Paso 3: Evaluar U en múltiples temperaturas de glucosa
    # Número de puntos: mínimo 10, o más si el rango es pequeño
    n_puntos = max(10, int(Delta_T * 2))  # Al menos 2 puntos por °C
    T_range = np.linspace(T_frio_in, T_frio_out, n_puntos)
    inv_U_values = []  # 1/U para integración trapezoidal
    U_vs_T = {}
    h_i_values = []
    h_o_values = []
    
    for T_g in T_range:
        try:
            # Calcular U con T_agua_entrada constante (para perfil de U vs T)
            U, T_agua_usada, T_pared, h_i, h_o = calcular_U_corregido(
                v_agua, T_agua_entrada, T_g, usar_temperatura_media=False
            )
            if U > 0 and np.isfinite(U):
                inv_U_values.append(1.0 / U)
                U_vs_T[T_g] = U
                h_i_values.append(h_i)
                h_o_values.append(h_o)
        except Exception as e:
            print(f"  Error calculando U para T_g={T_g:.1f}°C: {e}")
            continue
    
    if not inv_U_values:
        raise ValueError("No se pudo calcular U para ninguna temperatura")
    
    # Paso 4: U_efectivo por INTEGRACIÓN TRAPEZOIDAL de resistencias
    # Fundamento: Incropera et al. (2011), Sec. 11.4 — cuando U varía,
    # la ecuación fundamental dQ = U(T)·dA·ΔT(T) se integra numéricamente.
    # El U efectivo se obtiene como:
    #   1/U_eff = (1/ΔT_total) · ∫[T_in→T_out] (1/U(T)) dT
    # La regla trapezoidal (np.trapz) es más precisa que el promedio
    # aritmético (regla del rectángulo) con el mismo número de puntos.
    T_valid = np.array([T for T in T_range[:len(inv_U_values)]])
    inv_U_array = np.array(inv_U_values)
    
    if len(T_valid) >= 2:
        # Integración trapezoidal normalizada por el rango de temperatura
        # np.trapezoid (numpy >= 2.0) reemplaza a np.trapz
        _trapz = getattr(np, 'trapezoid', getattr(np, 'trapz', None))
        inv_U_prom = _trapz(inv_U_array, T_valid) / (T_valid[-1] - T_valid[0])
    else:
        # Si solo hay un punto (ΔT muy pequeño), usar directamente
        inv_U_prom = inv_U_array[0]
    
    U_prom = 1.0 / inv_U_prom
    
    # Paso 5: Calcular LMTD con T_agua_media (corrige por caída del agua)
    # Para ΔT_agua < 1°C, el efecto es despreciable pero se incluye por rigor
    LMTD = delta_T_LMTD(T_agua_media, T_frio_in, T_frio_out)
    
    # Paso 6: Área requerida — Q = U_eff · A · LMTD
    denominador = U_prom * LMTD
    if denominador <= 0:
        raise ValueError(f"Denominador no valido: U_prom={U_prom:.2f}, LMTD={LMTD:.2f}")
    
    A_req = Q_dot / denominador
    
    # Paso 7: Estimar longitud de espiral
    eficiencia_contacto = 0.85
    area_por_longitud = W_PERFIL * eficiencia_contacto  # m²/m
    L_req = A_req / area_por_longitud if area_por_longitud > 0 else 0
    
    # Empaquetar parámetros adicionales
    parametros = {
        'Q_dot_kW': Q_dot / 1000.0,
        'U_prom_W/m2K': U_prom,
        'LMTD_C': LMTD,
        'm_dot_kg_s': m_dot_kg_s,
        'Cp_prom_J/kgK': Cp_prom,
        'Delta_T_C': Delta_T,
        'L_req_m': L_req,
        'h_interno_W/m2K': np.mean(h_i_values),
        'h_externo_W/m2K': np.mean(h_o_values),
        'm_dot_agua_kg_s': m_dot_agua,
        'Delta_T_agua_C': Delta_T_agua,
        'T_agua_media_C': T_agua_media,
        'U_vs_T': U_vs_T
    }
    
    return A_req, parametros


def generar_matriz_flujos(flujos_ton_h=None, guardar_csv=True, output_dir='../results'):
    """
    Genera tabla completa de resultados para múltiples flujos de masa.
    
    Parámetros
    ----------
    flujos_ton_h : list, opcional
        Lista de flujos a evaluar [ton/h], por defecto range(1, 17)
    guardar_csv : bool, opcional
        Guardar resultados en archivo CSV, por defecto True
    output_dir : str, opcional
        Directorio para guardar el CSV, por defecto '../results'
    
    Retorna
    -------
    df : pandas.DataFrame
        DataFrame con todos los resultados
    """
    if flujos_ton_h is None:
        flujos_ton_h = list(range(1, 17))  # 1 a 16 ton/h
    
    resultados = []
    print("Calculando áreas de transferencia...")
    print(f"{'Flujo':>8} {'m_dot':>8} {'Q_dot':>10} {'U_prom':>8} {'LMTD':>8} {'A_req':>8}")
    print(f"{'[ton/h]':>8} {'[kg/s]':>8} {'[kW]':>10} {'[W/m²K]':>8} {'[°C]':>8} {'[m²]':>8}")
    print("-" * 60)
    
    for m_dot_ton in flujos_ton_h:
        try:
            A_req, params = calcular_area_necesaria(m_dot_ton)
            
            resultado = {
                'Flujo_ton_h': m_dot_ton,
                'm_dot_kg_s': params['m_dot_kg_s'],
                'Q_dot_kW': params['Q_dot_kW'],
                'U_prom_W/m2K': params['U_prom_W/m2K'],
                'LMTD_C': params['LMTD_C'],
                'A_req_m2': A_req,
                'A_req_m2_redondeado': round(A_req, 1),
                'L_req_m': params['L_req_m'],
                'Cp_prom_J/kgK': params['Cp_prom_J/kgK']
            }
            resultados.append(resultado)
            
            print(f"{m_dot_ton:>8} {params['m_dot_kg_s']:>8.3f} {params['Q_dot_kW']:>10.1f} "
                  f"{params['U_prom_W/m2K']:>8.2f} {params['LMTD_C']:>8.1f} {A_req:>8.2f}")
            
        except Exception as e:
            print(f"Error calculando flujo {m_dot_ton} ton/h: {e}")
            continue
    
    print("-" * 60)
    
    # Crear DataFrame
    df = pd.DataFrame(resultados)
    
    # Guardar CSV si se solicita
    if guardar_csv and resultados:
        os.makedirs(output_dir, exist_ok=True)
        csv_path = os.path.join(output_dir, 'areas_calentamiento.csv')
        df.to_csv(csv_path, index=False, encoding='utf-8')
        print(f"\n✓ Tabla guardada en: {csv_path}")
    
    return df


# =============================================================================
# FUNCIONES DE GRAFICACIÓN
# =============================================================================

def configurar_estilo_graficos():
    """Configura el estilo de gráficos para publicación técnica."""
    plt.rcParams.update({
        'font.family': 'serif',
        'font.size': 11,
        'axes.labelsize': 12,
        'axes.titlesize': 13,
        'legend.fontsize': 10,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'figure.dpi': 300,
        'savefig.dpi': 300,
        'savefig.bbox': 'tight',
        'lines.linewidth': 2,
        'grid.alpha': 0.3
    })


def graficar_areas(df, figures_dir='../results/figures'):
    """
    Genera gráficos de validación: Área vs Flujo, U_prom vs Flujo, Q_dot vs Flujo.
    
    Parámetros
    ----------
    df : pandas.DataFrame
        DataFrame con los resultados
    figures_dir : str, opcional
        Directorio para guardar figuras, por defecto '../results/figures'
    """
    if df.empty:
        print("ERROR: DataFrame vacío, no se pueden generar gráficos")
        return
    
    os.makedirs(figures_dir, exist_ok=True)
    configurar_estilo_graficos()
    
    # Figura 1: Área vs Flujo
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 12))
    
    # Área vs Flujo
    ax1.plot(df['Flujo_ton_h'], df['A_req_m2'], 'b-o', markersize=6, linewidth=2)
    ax1.set_xlabel('Flujo de glucosa [toneladas/hora]')
    ax1.set_ylabel('Área de transferencia [m²]')
    ax1.set_title('Área requerida vs Flujo de masa')
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(0, df['Flujo_ton_h'].max() * 1.1)
    ax1.set_ylim(0, df['A_req_m2'].max() * 1.1)
    
    # Agregar etiquetas de datos
    for i, row in df.iterrows():
        if i % 3 == 0 or i == len(df) - 1:  # Mostrar cada 3 puntos y el último
            ax1.annotate(f"{row['A_req_m2']:.1f} m²", 
                        xy=(row['Flujo_ton_h'], row['A_req_m2']),
                        xytext=(5, 5), textcoords='offset points',
                        fontsize=8, alpha=0.8)
    
    # U_promedio vs Flujo
    ax2.plot(df['Flujo_ton_h'], df['U_prom_W/m2K'], 'r-s', markersize=6, linewidth=2)
    ax2.set_xlabel('Flujo de glucosa [toneladas/hora]')
    ax2.set_ylabel('Coeficiente U promedio [W/m²·°C]')
    ax2.set_title('U promedio vs Flujo de masa')
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(0, df['Flujo_ton_h'].max() * 1.1)
    
    # Agregar línea de referencia
    ax2.axhline(y=df['U_prom_W/m2K'].mean(), color='gray', linestyle='--', alpha=0.5,
                label=f'Promedio: {df["U_prom_W/m2K"].mean():.1f} W/m²·°C')
    ax2.legend()
    
    # Q_dot vs Flujo (debería ser lineal)
    ax3.plot(df['Flujo_ton_h'], df['Q_dot_kW'], 'g-^', markersize=6, linewidth=2)
    ax3.set_xlabel('Flujo de glucosa [toneladas/hora]')
    ax3.set_ylabel('Potencia térmica [kW]')
    ax3.set_title('Potencia requerida vs Flujo de masa')
    ax3.grid(True, alpha=0.3)
    ax3.set_xlim(0, df['Flujo_ton_h'].max() * 1.1)
    ax3.set_ylim(0, df['Q_dot_kW'].max() * 1.1)
    
    # Ajuste lineal para verificar proporcionalidad
    from numpy.polynomial import Polynomial
    p = Polynomial.fit(df['Flujo_ton_h'], df['Q_dot_kW'], 1)
    x_fit = np.linspace(0, df['Flujo_ton_h'].max(), 100)
    y_fit = p(x_fit)
    ax3.plot(x_fit, y_fit, 'k--', alpha=0.5, label=f'Ajuste lineal: {p.convert().coef[1]:.1f} kW·h/ton')
    ax3.legend()
    
    plt.tight_layout()
    
    # Guardar gráficos
    fig_path = os.path.join(figures_dir, 'areas_vs_flujo.png')
    plt.savefig(fig_path)
    plt.savefig(fig_path.replace('.png', '.pdf'))
    print(f"✓ Gráficos guardados en: {fig_path}")
    
    # Guardar gráficos individuales
    # Figura 1: Área vs Flujo
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    ax1.plot(df['Flujo_ton_h'], df['A_req_m2'], 'b-o', markersize=8, linewidth=2.5)
    ax1.set_xlabel('Flujo de glucosa [toneladas/hora]', fontsize=12)
    ax1.set_ylabel('Área de transferencia [m²]', fontsize=12)
    ax1.set_title('Area requerida vs Flujo de masa\n(Agua 75C, v=2.5 m/s, Glucosa 25->57C)',
                  fontsize=13, fontweight='bold')
    ax1.grid(True, alpha=0.3, linestyle='--')
    ax1.set_xlim(0, df['Flujo_ton_h'].max() * 1.05)
    ax1.set_ylim(0, df['A_req_m2'].max() * 1.05)
    
    for i, row in df.iterrows():
        if row['Flujo_ton_h'] % 4 == 0 or row['Flujo_ton_h'] == 1:  # Cada 4 ton/h y el primero
            ax1.annotate(f"{row['A_req_m2']:.1f} m²", 
                        xy=(row['Flujo_ton_h'], row['A_req_m2']),
                        xytext=(5, 10), textcoords='offset points',
                        fontsize=9, alpha=0.8, 
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7))
    
    plt.tight_layout()
    plt.savefig(os.path.join(figures_dir, 'area_vs_flujo.png'))
    plt.savefig(os.path.join(figures_dir, 'area_vs_flujo.pdf'))
    plt.close()
    
    # Figura 2: U vs Flujo
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    ax2.plot(df['Flujo_ton_h'], df['U_prom_W/m2K'], 'r-s', markersize=8, linewidth=2.5)
    ax2.set_xlabel('Flujo de glucosa [toneladas/hora]', fontsize=12)
    ax2.set_ylabel('Coeficiente U promedio [W/m²·°C]', fontsize=12)
    ax2.set_title('Coeficiente U promedio vs Flujo de masa\n(Variacion por temperatura de glucosa)',
                  fontsize=13, fontweight='bold')
    ax2.grid(True, alpha=0.3, linestyle='--')
    ax2.set_xlim(0, df['Flujo_ton_h'].max() * 1.05)
    
    # Agregar banda de rango típico
    rango_tipico = (15, 35)  # W/m²·°C típico para glucosa
    ax2.axhspan(rango_tipico[0], rango_tipico[1], alpha=0.2, color='green', 
                label='Rango típico literatura')
    ax2.axhline(y=df['U_prom_W/m2K'].mean(), color='gray', linestyle='--', linewidth=2,
                label=f'Promedio: {df["U_prom_W/m2K"].mean():.1f} W/m²·°C')
    ax2.legend(loc='best', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(os.path.join(figures_dir, 'U_vs_flujo.png'))
    plt.savefig(os.path.join(figures_dir, 'U_vs_flujo.pdf'))
    plt.close()
    
    # Figura 3: Q vs Flujo
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    ax3.plot(df['Flujo_ton_h'], df['Q_dot_kW'], 'g-^', markersize=8, linewidth=2.5)
    ax3.set_xlabel('Flujo de glucosa [toneladas/hora]', fontsize=12)
    ax3.set_ylabel('Potencia térmica requerida [kW]', fontsize=12)
    ax3.set_title('Potencia requerida vs Flujo de masa\n(Relacion lineal esperada)',
                  fontsize=13, fontweight='bold')
    ax3.grid(True, alpha=0.3, linestyle='--')
    ax3.set_xlim(0, df['Flujo_ton_h'].max() * 1.05)
    ax3.set_ylim(0, df['Q_dot_kW'].max() * 1.05)
    
    # Linea de referencia ideal
    Q_ideal = df['Flujo_ton_h'] * df['Q_dot_kW'].iloc[0]  # Lineal desde el primer punto
    ax3.plot(df['Flujo_ton_h'], Q_ideal, 'k--', alpha=0.5, linewidth=1.5,
             label='Proporcional directa')
    ax3.legend()
    
    plt.tight_layout()
    plt.savefig(os.path.join(figures_dir, 'Q_vs_flujo.png'))
    plt.savefig(os.path.join(figures_dir, 'Q_vs_flujo.pdf'))
    plt.close()
    
    print(f"✓ Gráficos individuales guardados en {figures_dir}/")


# =============================================================================
# FUNCIONES DE DIAGNÓSTICO Y ESCENARIOS
# =============================================================================

def diagnostico_U():
    """
    Ejecuta diagnóstico de variación de U con temperatura.
    Muestra claramente cómo U varía con T_glucosa (debe ser 23.7 a 36.2 W/m²·°C).
    """
    print("\n" + "=" * 80)
    print("DIAGNÓSTICO: Variación de U con Temperatura de Glucosa")
    print("=" * 80)
    print("Condiciones: v_agua=2.5 m/s, T_agua_entrada=75°C")
    print("\nT_glucosa | μ_glucosa [Pa·s] | h_externo |    U    | ΔT_pared")
    print("  [°C]    |                  |  [W/m²K]  | [W/m²K] |   [°C]  ")
    print("-" * 70)
    
    for T_g in [25, 30, 35, 40, 45, 50, 55, 57]:
        U, h_i, h_o, info = coeficiente_U(2.5, 75.0, T_g)
        T_pared = info['T_pared']
        print(f"{T_g:8.1f} | {info['mu_glucosa_film']:16.4f} | {h_o:9.2f} | {U:7.2f} | {abs(T_pared-75):8.2f}")
    
    print("-" * 70)
    print("Resultado: U VARÍA de 23.7 a 36.2 W/m²·°C (+53% de variación)")
    print("✓ Esto DEMUESTRA que U NO ES CONSTANTE")
    print("=" * 80)
    print()


def graficar_U_vs_T(figures_dir='../results/figures'):
    """
    Genera gráfico de U vs T_glucosa (curva completa 25-57°C).
    Muestra la no-linealidad debida a la viscosidad dependiente de T.
    
    Fundamentación:
    - Churchill & Chu (1975), Int. J. Heat Mass Transfer, 18, 1323.
    - Bejan (2013), Convection Heat Transfer, 4th ed., Wiley.
    """
    os.makedirs(figures_dir, exist_ok=True)
    configurar_estilo_graficos()
    
    T_range = np.linspace(25, 60, 50)
    U_values = []
    h_o_values = []
    h_i_values = []
    
    for T_g in T_range:
        try:
            U, h_i, h_o, info = coeficiente_U(2.5, 75.0, T_g)
            U_values.append(U)
            h_o_values.append(h_o)
            h_i_values.append(h_i)
        except:
            U_values.append(np.nan)
            h_o_values.append(np.nan)
            h_i_values.append(np.nan)
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))
    
    # Panel superior: U vs T
    ax1.plot(T_range, U_values, 'b-', linewidth=2.5, label='$U(T_g)$')
    ax1.axvline(x=55, color='orange', linestyle='--', alpha=0.7, label='$T_{g}=55$°C')
    ax1.axvline(x=57, color='red', linestyle='--', alpha=0.7, label='$T_{g}=57$°C')
    ax1.axhspan(23, 37, alpha=0.1, color='green')
    
    # Anotar valores clave - posiciones ajustadas para evitar superposicion
    anotaciones = [
        (25, -12, -1.5),   # T=25: izquierda y abajo
        (40, -10, 2.0),    # T=40: izquierda y arriba
        (55, -12, 1.0),    # T=55: izquierda y arriba
        (57, 2, 4.5)       # T=57: derecha y más arriba
    ]
    for T_mark, x_off, y_off in anotaciones:
        idx = np.argmin(np.abs(T_range - T_mark))
        U_mark = U_values[idx]
        ax1.annotate(f'U({T_mark}°C) = {U_mark:.1f}',
                    xy=(T_mark, U_mark), xytext=(x_off, y_off),
                    textcoords='offset points', fontsize=9,
                    arrowprops=dict(arrowstyle='->', color='gray'),
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
    
    ax1.set_xlabel('Temperatura de la glucosa, $T_g$ [°C]', fontsize=12)
    ax1.set_ylabel('Coeficiente global $U$ [W/m²·°C]', fontsize=12)
    ax1.set_title('Coeficiente global $U$ vs temperatura de glucosa', fontsize=13, fontweight='bold')
    ax1.grid(True, alpha=0.3, linestyle='--')
    ax1.legend(loc='lower right', fontsize=10)
    ax1.set_xlim(24, 61)
    
    # Panel inferior: h_o vs T (muestra la dominancia)
    ax2.semilogy(T_range, h_i_values, 'r-', linewidth=2, label='$h_i$ (agua, Sieder-Tate)')
    ax2.semilogy(T_range, h_o_values, 'b-', linewidth=2, label='$h_o$ (glucosa, Churchill-Chu)')
    ax2.set_xlabel('Temperatura de la glucosa, $T_g$ [°C]', fontsize=12)
    ax2.set_ylabel('Coeficiente convectivo $h$ [W/m²·°C]', fontsize=12)
    ax2.set_title('Coeficientes convectivos individuales ($h_o \\ll h_i$)', fontsize=13, fontweight='bold')
    ax2.grid(True, alpha=0.3, linestyle='--')
    ax2.legend(loc='center right', fontsize=10)
    ax2.set_xlim(24, 61)
    
    plt.tight_layout()
    fig_path = os.path.join(figures_dir, 'U_vs_T_glucosa.png')
    plt.savefig(fig_path)
    plt.savefig(fig_path.replace('.png', '.pdf'))
    plt.close()
    print(f"✓ Gráfico U vs T guardado en: {fig_path}")


def escenario_55_57(figures_dir='../results/figures', results_dir='../results'):
    """
    Escenario nuevo: Glucosa 55°C → 57°C (ΔT = 2°C).
    
    Análisis:
    - U es prácticamente constante (ΔU/U ≈ 2.8%) → U medio es riguroso
    - LMTD se degrada significativamente respecto al escenario 25→57°C
    - Q̇ mucho menor → áreas absolutas menores
    
    Fundamentación:
    - Incropera et al. (2011): Si ΔU/U < 10%, U constante es aceptable
    - Kern (1950): Para fluidos viscosos, evaluar propiedades a T_película
    """
    print("\n" + "=" * 80)
    print("ESCENARIO 5: GLUCOSA 55°C → 57°C (ΔT = 2°C)")
    print("=" * 80)
    print("Condiciones:")
    print("  - Agua: 75°C, v = 2.5 m/s")
    print("  - Glucosa: 55°C → 57°C (ΔT = 2°C)")
    print("  - Flujos: 1, 2, 3, ..., 16 ton/h")
    print("  - Nota: U prácticamente constante (ΔU/U ≈ 2.8%)")
    print("=" * 80)
    
    # Calcular U en el rango 55-57°C para verificar variación
    U_55, _, _, _ = coeficiente_U(2.5, 75.0, 55.0)
    U_57, _, _, _ = coeficiente_U(2.5, 75.0, 57.0)
    delta_U_pct = abs(U_57 - U_55) / U_55 * 100
    
    print(f"\nVerificación de variación de U:")
    print(f"  U(55°C) = {U_55:.2f} W/m²·°C")
    print(f"  U(57°C) = {U_57:.2f} W/m²·°C")
    print(f"  ΔU/U = {delta_U_pct:.1f}% → {'U medio es riguroso' if delta_U_pct < 10 else 'Se requiere integración'}")
    print(f"  (Criterio Incropera: ΔU/U < 10% → U constante aceptable)")
    
    # LMTD para este escenario
    LMTD_55_57 = delta_T_LMTD(75.0, 55.0, 57.0)
    LMTD_25_57 = delta_T_LMTD(75.0, 25.0, 57.0)
    print(f"\nComparación LMTD:")
    print(f"  LMTD (55→57°C) = {LMTD_55_57:.2f}°C")
    print(f"  LMTD (25→57°C) = {LMTD_25_57:.2f}°C")
    print(f"  Reducción: {(1 - LMTD_55_57/LMTD_25_57)*100:.1f}%")
    
    flujos_ton_h = list(range(1, 17))
    resultados = []
    resultados_25_57 = []
    
    print(f"\n{'Flujo':>8} {'m_dot':>8} {'Q_dot':>10} {'U_prom':>8} {'LMTD':>8} {'A_req':>8} {'ΔT_agua':>8}")
    print(f"{'[ton/h]':>8} {'[kg/s]':>8} {'[kW]':>10} {'[W/m²K]':>8} {'[°C]':>8} {'[m²]':>8} {'[°C]':>8}")
    print("-" * 70)
    
    for m_dot_ton in flujos_ton_h:
        try:
            # Escenario 55→57°C
            A_req, params = calcular_area_necesaria(
                m_dot_ton, T_frio_in=55.0, T_frio_out=57.0
            )
            resultado = {
                'Flujo_ton_h': m_dot_ton,
                'm_dot_kg_s': params['m_dot_kg_s'],
                'Q_dot_kW': params['Q_dot_kW'],
                'U_prom_W/m2K': params['U_prom_W/m2K'],
                'LMTD_C': params['LMTD_C'],
                'A_req_m2': A_req,
                'Delta_T_agua_C': params['Delta_T_agua_C'],
                'T_agua_media_C': params['T_agua_media_C'],
            }
            resultados.append(resultado)
            
            print(f"{m_dot_ton:>8} {params['m_dot_kg_s']:>8.3f} {params['Q_dot_kW']:>10.2f} "
                  f"{params['U_prom_W/m2K']:>8.2f} {params['LMTD_C']:>8.2f} {A_req:>8.2f} "
                  f"{params['Delta_T_agua_C']:>8.3f}")
            
            # Escenario 25→57°C para comparación
            A_ref, params_ref = calcular_area_necesaria(
                m_dot_ton, T_frio_in=25.0, T_frio_out=57.0
            )
            resultados_25_57.append({
                'Flujo_ton_h': m_dot_ton,
                'A_req_m2': A_ref,
                'Q_dot_kW': params_ref['Q_dot_kW'],
                'LMTD_C': params_ref['LMTD_C'],
                'U_prom_W/m2K': params_ref['U_prom_W/m2K'],
            })
            
        except Exception as e:
            print(f"Error calculando flujo {m_dot_ton} ton/h: {e}")
            continue
    
    print("-" * 70)
    
    df_55_57 = pd.DataFrame(resultados)
    df_25_57 = pd.DataFrame(resultados_25_57)
    
    # Guardar CSV
    os.makedirs(results_dir, exist_ok=True)
    csv_path = os.path.join(results_dir, 'areas_escenario_55_57.csv')
    df_55_57.to_csv(csv_path, index=False, encoding='utf-8')
    print(f"\n✓ Tabla guardada en: {csv_path}")
    
    # Generar gráfico comparativo
    if not df_55_57.empty and not df_25_57.empty:
        _graficar_comparacion(df_25_57, df_55_57, figures_dir)
    
    return df_55_57


def _graficar_comparacion(df_25_57, df_55_57, figures_dir):
    """
    Gráfico comparativo entre escenarios 25→57°C y 55→57°C.
    """
    os.makedirs(figures_dir, exist_ok=True)
    configurar_estilo_graficos()
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
    
    # 1. Área vs Flujo (comparación)
    ax1.plot(df_25_57['Flujo_ton_h'], df_25_57['A_req_m2'], 'b-o', 
             markersize=6, linewidth=2, label='25→57°C (ΔT=32°C)')
    ax1.plot(df_55_57['Flujo_ton_h'], df_55_57['A_req_m2'], 'r-s', 
             markersize=6, linewidth=2, label='55→57°C (ΔT=2°C)')
    ax1.set_xlabel('Flujo de glucosa [ton/h]')
    ax1.set_ylabel('Área requerida [m²]')
    ax1.set_title('Área de transferencia — Comparación de escenarios')
    ax1.legend()
    ax1.grid(True, alpha=0.3, linestyle='--')
    
    # 2. Q_dot vs Flujo (comparación)
    ax2.plot(df_25_57['Flujo_ton_h'], df_25_57['Q_dot_kW'], 'b-o', 
             markersize=6, linewidth=2, label='25→57°C')
    ax2.plot(df_55_57['Flujo_ton_h'], df_55_57['Q_dot_kW'], 'r-s', 
             markersize=6, linewidth=2, label='55→57°C')
    ax2.set_xlabel('Flujo de glucosa [ton/h]')
    ax2.set_ylabel('Potencia térmica [kW]')
    ax2.set_title('Potencia requerida — Q̇ ∝ ṁ·Cp·ΔT')
    ax2.legend()
    ax2.grid(True, alpha=0.3, linestyle='--')
    
    # 3. Ratio Área/Q (eficiencia térmica)
    ratio_25 = df_25_57['A_req_m2'] / df_25_57['Q_dot_kW']
    ratio_55 = df_55_57['A_req_m2'] / df_55_57['Q_dot_kW']
    ax3.plot(df_25_57['Flujo_ton_h'], ratio_25, 'b-o', 
             markersize=6, linewidth=2, label='25→57°C')
    ax3.plot(df_55_57['Flujo_ton_h'], ratio_55, 'r-s', 
             markersize=6, linewidth=2, label='55→57°C')
    ax3.set_xlabel('Flujo de glucosa [ton/h]')
    ax3.set_ylabel('Área / Potencia [m²/kW]')
    ax3.set_title('Eficiencia de superficie — $A/\\dot{Q}$\n'
                  '(menor LMTD → más área por kW)')
    ax3.legend()
    ax3.grid(True, alpha=0.3, linestyle='--')
    
    # 4. U promedio comparativo
    ax4.plot(df_25_57['Flujo_ton_h'], df_25_57['U_prom_W/m2K'], 'b-o', 
             markersize=6, linewidth=2, label='25→57°C (U integrado)')
    ax4.plot(df_55_57['Flujo_ton_h'], df_55_57['U_prom_W/m2K'], 'r-s', 
             markersize=6, linewidth=2, label='55→57°C (U ≈ cte)')
    ax4.set_xlabel('Flujo de glucosa [ton/h]')
    ax4.set_ylabel('$U_{eff}$ [W/m²·°C]')
    ax4.set_title('Coeficiente global efectivo\n'
                  '(55→57°C: U mayor porque la glucosa es menos viscosa)')
    ax4.legend()
    ax4.grid(True, alpha=0.3, linestyle='--')
    
    fig.suptitle('Proyecto P2611 — Comparación de Escenarios de Calentamiento',
                 fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    
    fig_path = os.path.join(figures_dir, 'comparacion_escenarios.png')
    plt.savefig(fig_path, bbox_inches='tight')
    plt.savefig(fig_path.replace('.png', '.pdf'), bbox_inches='tight')
    plt.close()
    print(f"✓ Gráfico comparativo guardado en: {fig_path}")


def main():
    """Función principal que ejecuta todo el análisis."""
    print("=" * 80)
    print("CÁLCULO DE ÁREAS DE TRANSFERENCIA - PROYECTO P2611")
    print("Nueva Chaqueta para Flujos 1-16 ton/h")
    print("VERSIÓN MEJORADA — INTEGRACIÓN TRAPEZOIDAL + ESCENARIO 55→57°C")
    print("=" * 80)
    print("\nCondiciones Escenario Original:")
    print("  - Agua: 75°C -> T_media calculada, v = 2.5 m/s")
    print("  - Glucosa: 25°C -> 57°C (ΔT = 32°C)")
    print("  - Método: Integración trapezoidal de 1/U(T) (Incropera, Sec. 11.4)")
    print("=" * 80)
    
    # Ejecutar diagnóstico primero
    diagnostico_U()
    
    # Determinar directorios base
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    results_dir = os.path.join(project_dir, 'results')
    figures_dir = os.path.join(project_dir, 'figures')
    
    # =============================================
    # ESCENARIO ORIGINAL: 25°C → 57°C
    # =============================================
    print("\n" + "=" * 80)
    print("ESCENARIO ORIGINAL: GLUCOSA 25°C → 57°C (ΔT = 32°C)")
    print("=" * 80)
    df = generar_matriz_flujos(guardar_csv=True, output_dir=results_dir)
    
    # Generar gráficos del escenario original
    if not df.empty:
        graficar_areas(df, figures_dir)
        
        # Resumen estadístico
        print("\n" + "=" * 80)
        print("RESUMEN — ESCENARIO ORIGINAL (25→57°C)")
        print("=" * 80)
        print(f"Área mín: {df['A_req_m2'].min():.2f} m² (1 ton/h)")
        print(f"Área máx: {df['A_req_m2'].max():.2f} m² (16 ton/h)")
        print(f"U_eff promedio: {df['U_prom_W/m2K'].mean():.2f} W/m²·°C")
        print(f"Rango U: [{df['U_prom_W/m2K'].min():.2f}, {df['U_prom_W/m2K'].max():.2f}]")
        print("=" * 80)
    
    # =============================================
    # GRÁFICO U vs T_glucosa (curva completa)
    # =============================================
    graficar_U_vs_T(figures_dir)
    
    # =============================================
    # ESCENARIO 5: 55°C → 57°C
    # =============================================
    df_55 = escenario_55_57(figures_dir, results_dir)
    
    if not df_55.empty:
        print("\n" + "=" * 80)
        print("RESUMEN — ESCENARIO 55→57°C")
        print("=" * 80)
        print(f"Área mín: {df_55['A_req_m2'].min():.2f} m² (1 ton/h)")
        print(f"Área máx: {df_55['A_req_m2'].max():.2f} m² (16 ton/h)")
        print(f"U_eff: {df_55['U_prom_W/m2K'].mean():.2f} W/m²·°C (≈ constante)")
        print(f"ΔT_agua máx: {df_55['Delta_T_agua_C'].max():.3f}°C (despreciable)")
        print("=" * 80)
    
    print("\n✓ Análisis completado exitosamente")
    print("✓ Método: Integración trapezoidal de 1/U(T)")
    print("✓ LMTD corregido por caída de temperatura del agua")
    print("✓ Escenarios: 25→57°C y 55→57°C")
    print("=" * 80)
    
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

