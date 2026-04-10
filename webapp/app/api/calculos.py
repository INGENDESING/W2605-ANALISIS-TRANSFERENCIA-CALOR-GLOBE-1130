"""
API Endpoints para cálculos de transferencia de calor y balance
"""
from flask import Blueprint, request, jsonify

from ..core.balance_energia import (
    calcular_transferencia_calor,
    simular_calentamiento_transitorio,
    simular_calentamiento_y_ciclo,
    simular_ciclo_automatico,
    calcular_tiempo_calentamiento
)
from ..core.balance_masa import (
    calcular_masa_glucosa,
    calcular_volumen_a_nivel,
    calcular_nivel_porcentaje,
    calcular_capacidad_tanque
)
from ..core.props_calculadas import (
    calcular_propiedades_completas,
    generar_tabla_propiedades
)

api_calculos_bp = Blueprint('api_calculos', __name__)


@api_calculos_bp.route('/calcular/transferencia-calor', methods=['POST'])
def api_calcular_transferencia_calor():
    """
    Calcular transferencia de calor
    
    Request JSON:
    {
        "flujo_agua_m3h": 30.9,
        "temp_agua_entrada": 65,
        "temp_glucosa_inicial": 20,
        "temp_glucosa_objetivo": 60,
        "volumen_glucosa_m3": 24,
        "area_contacto_m2": 13.0
    }
    """
    data = request.get_json()
    
    try:
        # Parámetros requeridos
        flujo_agua = float(data.get('flujo_agua_m3h', 30.9))
        temp_agua = float(data.get('temp_agua_entrada', 65))
        temp_glucosa = float(data.get('temp_glucosa_inicial', 20))
        
        # Parámetros opcionales
        temp_objetivo = data.get('temp_glucosa_objetivo')
        if temp_objetivo is not None:
            temp_objetivo = float(temp_objetivo)
        
        volumen = float(data.get('volumen_glucosa_m3', 24))
        area = data.get('area_contacto_m2')
        if area is not None:
            area = float(area)
        
        # Validaciones
        if flujo_agua <= 0:
            return jsonify({'error': 'Flujo de agua debe ser positivo'}), 400
        if temp_agua <= temp_glucosa:
            return jsonify({'error': 'Temperatura del agua debe ser mayor que la glucosa'}), 400
        
        # Calcular
        resultado = calcular_transferencia_calor(
            flujo_agua, temp_agua, temp_glucosa,
            temp_objetivo, volumen, area
        )
        
        return jsonify({
            'success': True,
            'data': resultado
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_calculos_bp.route('/calcular/simular-calentamiento', methods=['POST'])
def api_simular_calentamiento():
    """
    Simular calentamiento transitorio completo
    
    Request JSON:
    {
        "temp_inicial": 20,
        "temp_agua": 65,
        "flujo_agua_m3h": 30.9,
        "volumen_glucosa_m3": 24,
        "tiempo_final_h": 24,
        "dt_min": 10
    }
    """
    data = request.get_json()
    
    try:
        temp_inicial = float(data.get('temp_inicial', 20))
        temp_agua = float(data.get('temp_agua', 65))
        flujo_agua = float(data.get('flujo_agua_m3h', 30.9))
        volumen = float(data.get('volumen_glucosa_m3', 24))
        t_final = float(data.get('tiempo_final_h', 24))
        dt = float(data.get('dt_min', 10))
        
        # Velocidad en media caña — geometría real
        A_sec_mc = 0.0455 * 0.141  # m²
        v_agua = (flujo_agua / 3600.0) / A_sec_mc  # m/s
        
        resultado = simular_calentamiento_transitorio(
            temp_inicial, temp_agua, v_agua, volumen, t_final, dt
        )
        
        return jsonify({
            'success': True,
            'data': resultado
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_calculos_bp.route('/calcular/masa-glucosa', methods=['POST'])
def api_calcular_masa():
    """Calcular masa de glucosa"""
    data = request.get_json()
    
    try:
        volumen = float(data.get('volumen_m3', 24))
        temperatura = float(data.get('temperatura_c', 40))
        
        resultado = calcular_masa_glucosa(volumen, temperatura)
        
        return jsonify({
            'success': True,
            'data': resultado
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_calculos_bp.route('/calcular/nivel-a-volumen', methods=['POST'])
def api_nivel_a_volumen():
    """Convertir nivel a volumen"""
    data = request.get_json()
    
    try:
        nivel = float(data.get('nivel_m', 5))
        resultado = calcular_volumen_a_nivel(nivel)
        
        return jsonify({
            'success': True,
            'data': resultado
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_calculos_bp.route('/calcular/porcentaje-a-nivel', methods=['POST'])
def api_porcentaje_a_nivel():
    """Convertir porcentaje a nivel"""
    data = request.get_json()
    
    try:
        porcentaje = float(data.get('porcentaje', 80))
        resultado = calcular_nivel_porcentaje(porcentaje)
        
        return jsonify({
            'success': True,
            'data': resultado
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_calculos_bp.route('/calcular/capacidad-tanque', methods=['GET'])
def api_capacidad_tanque():
    """Obtener capacidad del tanque"""
    try:
        resultado = calcular_capacidad_tanque()
        
        return jsonify({
            'success': True,
            'data': resultado
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_calculos_bp.route('/calcular/propiedades', methods=['POST'])
def api_calcular_propiedades():
    """Calcular propiedades termofísicas a una temperatura"""
    data = request.get_json()
    
    try:
        temperatura = float(data.get('temperatura_c', 40))
        resultado = calcular_propiedades_completas(temperatura)
        
        return jsonify({
            'success': True,
            'data': resultado
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_calculos_bp.route('/calcular/tabla-propiedades', methods=['GET'])
def api_tabla_propiedades():
    """Generar tabla de propiedades"""
    try:
        temp_min = float(request.args.get('temp_min', 20))
        temp_max = float(request.args.get('temp_max', 80))
        paso = float(request.args.get('paso', 5))
        resultado = generar_tabla_propiedades(temp_min, temp_max, paso)
        return jsonify({'success': True, 'data': resultado})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ── A.3: Cálculo instantáneo (solo álgebra, sin ODE) ─────────────────────────
import sys as _sys
from pathlib import Path as _Path
import math as _math
_sys.path.insert(0, str(_Path(__file__).parent.parent.parent.parent / 'src'))
from coeficiente_U import coeficiente_U as _coef_U
from propiedades_glucosa import (rho_glucosa as _rho_g, Cp_glucosa as _Cp_g,
                                  mu_glucosa as _mu_g, k_glucosa as _k_g,
                                  Pr_glucosa as _Pr_g,
                                  rho_agua as _rho_w, Cp_agua as _Cp_w)
from geometria_tanque import A_CONTACTO as _A_CONTACTO


@api_calculos_bp.route('/calcular/instantaneo', methods=['POST'])
def api_calcular_instantaneo():
    """Cálculo instantáneo sin ODE — respuesta < 200 ms."""
    data = request.get_json() or {}
    try:
        T_agua = float(data.get('temp_agua', 65))
        T_glucosa = float(data.get('temp_glucosa', 40))
        area = float(data.get('area_m2', _A_CONTACTO))
        fouling_agua = float(data.get('fouling_agua', 1.76e-4))
        fouling_glucosa = float(data.get('fouling_glucosa', 3.5e-4))
        _Amc = 0.0455 * 0.141
        if 'velocidad_m_s' in data:
            v_agua = float(data['velocidad_m_s'])
        elif 'flujo_agua_m3h' in data:
            v_agua = float(data['flujo_agua_m3h']) / 3600.0 / _Amc
        else:
            v_agua = 2.5
        if T_agua <= T_glucosa:
            return jsonify({'error': 'T_agua debe ser mayor que T_glucosa'}), 400

        U, h_i, h_o, info = _coef_U(v_agua, T_agua, T_glucosa)
        R_total_f = 1/h_i + info['R_w'] + 1/h_o + fouling_agua + fouling_glucosa
        U_f = 1.0 / R_total_f
        DeltaT = T_agua - T_glucosa
        Q_kW = U_f * area * DeltaT / 1000.0

        Q_m3s = v_agua * _Amc
        m_dot_w = Q_m3s * _rho_w(T_agua)
        dTw = (U_f * area * DeltaT) / (m_dot_w * _Cp_w(T_agua))
        T_ws = T_agua - dTw
        dT1, dT2 = DeltaT, T_ws - T_glucosa
        LMTD = ((dT1 - dT2) / _math.log(dT1 / max(dT2, 0.01))
                if abs(dT1 - dT2) > 0.01 else dT1)
        Re = info['Re_agua']
        regimen = ('turbulento' if Re > 10000
                   else ('transicion' if Re > 2300 else 'laminar'))
        return jsonify({'success': True, 'data': {
            'U': round(U_f, 3), 'U_sin_fouling': round(U, 3),
            'h_i': round(h_i, 2), 'h_o': round(h_o, 2),
            'R_i': round(1/h_i, 6), 'R_w': round(info['R_w'], 6),
            'R_o': round(1/h_o, 6), 'R_f_agua': fouling_agua, 'R_f_glucosa': fouling_glucosa,
            'pct_R_i': round(info['pct_R_i'], 1),
            'pct_R_w': round(info['pct_R_w'], 1),
            'pct_R_o': round(info['pct_R_o'], 1),
            'Q_kW': round(Q_kW, 3), 'Q_kW_m2': round(Q_kW / area, 4),
            'LMTD': round(LMTD, 3), 'T_agua_salida': round(T_ws, 2),
            'DeltaT_agua': round(dTw, 3), 'Re': round(Re, 0),
            'Nu': round(info['Nu_agua'], 2), 'regimen': regimen,
            'v_agua': round(v_agua, 4),
            'propiedades_glucosa': {
                'rho': round(_rho_g(T_glucosa), 2),
                'mu_Pa_s': round(_mu_g(T_glucosa), 6),
                'mu_cP': round(_mu_g(T_glucosa) * 1000, 3),
                'Cp': round(_Cp_g(T_glucosa), 2),
                'k': round(_k_g(T_glucosa), 5),
                'Pr': round(_Pr_g(T_glucosa), 1),
            },
        }})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ── A.4: Transitorio completo (calentamiento + ciclo) ────────────────────────
@api_calculos_bp.route('/calcular/transitorio-completo', methods=['POST'])
def api_transitorio_completo():
    """Calentamiento inicial + ciclo de descargas en una sola llamada."""
    data = request.get_json() or {}
    try:
        T_inicial = float(data.get('T_inicial', 20))
        T_objetivo = float(data.get('T_objetivo_inicio_descarga', 57))
        T_agua = float(data.get('T_agua', 65))
        area = float(data.get('area_m2', _A_CONTACTO))
        nivel_pct = float(data.get('nivel_inicial_pct', 80))
        num_descargas = int(data.get('num_descargas', 8))
        masa_ton = float(data.get('masa_por_descarga_ton', 24))
        t_desc_h = float(data.get('tiempo_descarga_h', 1.5))
        periodo_h = float(data.get('periodo_ciclo_h', 3.0))
        temp_min_ac = float(data.get('temp_minima_aceptable', 55))
        _Amc = 0.0455 * 0.141
        if 'velocidad_m_s' in data:
            v_agua = float(data['velocidad_m_s'])
        elif 'flujo_agua_m3h' in data:
            v_agua = float(data['flujo_agua_m3h']) / 3600.0 / _Amc
        else:
            v_agua = 2.5
        from geometria_tanque import volumen_total
        vol_ini = volumen_total() * (nivel_pct / 100.0)
        resultado = simular_calentamiento_y_ciclo(
            T_inicial=T_inicial, T_objetivo_inicio_descarga=T_objetivo,
            T_agua=T_agua, v_agua=v_agua, area=area,
            volumen_inicial_m3=vol_ini, num_descargas=num_descargas,
            masa_por_descarga_kg=masa_ton * 1000,
            tiempo_descarga_h=t_desc_h, periodo_ciclo_h=periodo_h,
            temp_minima_aceptable=temp_min_ac,
        )
        return jsonify({'success': True, 'data': resultado})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ── A.4b: Ciclo automático (num_descargas es resultado) ──────────────────────
@api_calculos_bp.route('/calcular/ciclo-automatico', methods=['POST'])
def api_ciclo_automatico():
    """Ciclo automático: descargas calculadas por el motor ODE."""
    data = request.get_json() or {}
    try:
        T_inicial = float(data.get('T_inicial', 20))
        T_objetivo = float(data.get('T_objetivo_inicio_descarga', 57))
        T_agua = float(data.get('T_agua', 65))
        area = float(data.get('area_m2', _A_CONTACTO))
        nivel_pct = float(data.get('nivel_inicial_pct', 80))
        masa_ton = float(data.get('masa_por_descarga_ton', 24))
        t_desc_h = float(data.get('tiempo_descarga_h', 1.5))
        periodo_h = float(data.get('periodo_ciclo_h', 3.0))
        temp_min_ac = float(data.get('temp_minima_aceptable', 55))
        tiempo_max_h = float(data.get('tiempo_maximo_h', 24.0))
        _Amc = 0.0455 * 0.141
        if 'velocidad_m_s' in data:
            v_agua = float(data['velocidad_m_s'])
        elif 'flujo_agua_m3h' in data:
            v_agua = float(data['flujo_agua_m3h']) / 3600.0 / _Amc
        else:
            v_agua = 2.5
        from geometria_tanque import volumen_total
        vol_ini = volumen_total() * (nivel_pct / 100.0)
        resultado = simular_ciclo_automatico(
            T_inicial=T_inicial, T_objetivo_inicio_descarga=T_objetivo,
            T_agua=T_agua, v_agua=v_agua, area=area,
            volumen_inicial_m3=vol_ini,
            masa_por_descarga_kg=masa_ton * 1000,
            tiempo_descarga_h=t_desc_h, periodo_ciclo_h=periodo_h,
            temp_minima_aceptable=temp_min_ac,
            tiempo_maximo_h=tiempo_max_h,
        )
        return jsonify({'success': True, 'data': resultado})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ── A.5: Análisis de sensibilidad univariable ─────────────────────────────────
@api_calculos_bp.route('/sensibilidad', methods=['POST'])
def api_sensibilidad():
    """Varía un parámetro y devuelve KPIs para cada valor."""
    data = request.get_json() or {}
    try:
        variable = data.get('variable_nombre', 'T_agua')
        valores = data.get('valores_lista', [])
        p = data.get('params_fijos', {})
        T_agua_f = float(p.get('T_agua', 65))
        v_f = float(p.get('velocidad_m_s', 2.5))
        T_ini_f = float(p.get('T_glucosa_inicial', 20))
        T_obj_f = float(p.get('T_objetivo', 57))
        nivel_f = float(p.get('nivel_pct', 80))
        area_f = float(p.get('area_m2', _A_CONTACTO))
        nd_f = int(p.get('num_descargas', 8))
        masa_f = float(p.get('masa_por_descarga_ton', 24))
        td_f = float(p.get('tiempo_descarga_h', 1.5))
        per_f = float(p.get('periodo_ciclo_h', 3.0))
        from geometria_tanque import volumen_total
        V_tot = volumen_total()
        resultados = []
        for val in valores:
            val = float(val)
            T_a, v, T_i, niv, ar, nd = T_agua_f, v_f, T_ini_f, nivel_f, area_f, nd_f
            if variable == 'T_agua': T_a = val
            elif variable == 'velocidad_m_s': v = val
            elif variable == 'T_glucosa_inicial': T_i = val
            elif variable == 'nivel_pct': niv = val
            elif variable == 'area_m2': ar = val
            elif variable == 'num_descargas': nd = int(val)
            vol_i = V_tot * (niv / 100.0)
            U_val, _, _, _ = _coef_U(v, T_a, T_i)
            t_c = calcular_tiempo_calentamiento(T_i, T_obj_f, T_a, v, vol_i)
            cap, T_fin = None, None
            try:
                s = simular_calentamiento_y_ciclo(T_i, T_obj_f, T_a, v, ar, vol_i,
                                                   nd, masa_f * 1000, td_f, per_f)
                cap = round(s['metricas']['masa_total_descargada_ton'], 2)
                T_fin = s['metricas']['T_final']
            except Exception:
                pass
            resultados.append({'valor': val, 'U': round(U_val, 3),
                                'tiempo_calentamiento_h': round(t_c, 3) if t_c else None,
                                'capacidad_ton': cap, 'T_final': T_fin})
        return jsonify({'success': True, 'data': resultados})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ── A.6: Propiedades termofísicas glucosa ─────────────────────────────────────
@api_calculos_bp.route('/propiedades-glucosa', methods=['GET'])
def api_propiedades_glucosa():
    """GET /api/propiedades-glucosa?temp_min=20&temp_max=70&paso=1"""
    try:
        temp_min = float(request.args.get('temp_min', 20))
        temp_max = float(request.args.get('temp_max', 70))
        paso = float(request.args.get('paso', 1))
        tabla = generar_tabla_propiedades(temp_min, temp_max, paso)
        return jsonify({'success': True, 'data': tabla})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ── A.7: Estado del tanque (para SVG animado) ─────────────────────────────────
@api_calculos_bp.route('/estado-tanque', methods=['GET'])
def api_estado_tanque():
    """GET /api/estado-tanque?nivel_pct=80&temp=45"""
    try:
        nivel_pct = float(request.args.get('nivel_pct', 80))
        temp = float(request.args.get('temp', 45))
        from geometria_tanque import volumen_total, nivel_a_porcentaje
        V_tot = volumen_total()
        volumen = V_tot * (nivel_pct / 100.0)
        h_nivel = nivel_a_porcentaje(nivel_pct)
        masa_ton = volumen * _rho_g(temp) / 1000.0
        t_norm = max(0.0, min(1.0, (temp - 15) / 55.0))
        hue = round(210 - t_norm * 180)
        return jsonify({'success': True, 'data': {
            'nivel_pct': round(nivel_pct, 1),
            'nivel_mm': round(h_nivel * 1000, 1),
            'volumen_m3': round(volumen, 3),
            'masa_ton': round(masa_ton, 2),
            'color': f'hsl({hue},80%,55%)',
            'hue': hue,
        }})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
