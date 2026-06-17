"""
API Endpoints para exportación de datos (PDF, Excel, CSV)
"""
import io
import csv
from flask import Blueprint, request, jsonify, send_file

api_exportar_bp = Blueprint('api_exportar', __name__)


@api_exportar_bp.route('/exportar/csv', methods=['POST'])
def exportar_csv():
    """Exportar datos a CSV"""
    data = request.get_json()
    
    try:
        serie = data.get('serie_temporal', [])
        filename = data.get('filename', 'datos_w2605.csv')
        
        if not serie:
            return jsonify({'error': 'No hay datos para exportar'}), 400
        
        # Crear CSV en memoria
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=serie[0].keys())
        writer.writeheader()
        writer.writerows(serie)
        
        # Convertir a bytes
        output.seek(0)
        bytes_output = io.BytesIO(output.getvalue().encode('utf-8'))
        
        return send_file(
            bytes_output,
            mimetype='text/csv',
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_exportar_bp.route('/exportar/excel', methods=['POST'])
def exportar_excel():
    """Exportar datos a Excel"""
    data = request.get_json()
    
    try:
        import xlsxwriter
        
        serie = data.get('serie_temporal', [])
        descargas = data.get('descargas', [])
        filename = data.get('filename', 'datos_w2605.xlsx')
        
        if not serie:
            return jsonify({'error': 'No hay datos para exportar'}), 400
        
        # Crear Excel en memoria
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        
        # Hoja 1: Serie temporal
        ws1 = workbook.add_worksheet('Serie Temporal')
        headers = list(serie[0].keys())
        
        # Formato de encabezado
        header_format = workbook.add_format({
            'bold': True,
            'bg_color': '#4472C4',
            'font_color': 'white'
        })
        
        # Escribir encabezados
        for col, header in enumerate(headers):
            ws1.write(0, col, header, header_format)
        
        # Escribir datos
        for row, record in enumerate(serie, start=1):
            for col, header in enumerate(headers):
                ws1.write(row, col, record.get(header, ''))
        
        # Hoja 2: Descargas (si hay)
        if descargas:
            ws2 = workbook.add_worksheet('Descargas')
            headers2 = list(descargas[0].keys())
            
            for col, header in enumerate(headers2):
                ws2.write(0, col, header, header_format)
            
            for row, record in enumerate(descargas, start=1):
                for col, header in enumerate(headers2):
                    ws2.write(row, col, record.get(header, ''))
        
        workbook.close()
        output.seek(0)
        
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=filename
        )
        
    except ImportError:
        return jsonify({'error': 'Módulo xlsxwriter no instalado'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_exportar_bp.route('/exportar/reporte-json', methods=['POST'])
def exportar_reporte_json():
    """Exportar reporte completo como JSON descargable"""
    data = request.get_json()
    
    try:
        # Construir reporte completo
        reporte = {
            'proyecto': 'W2605 - Balance de Materia y Energía',
            'cliente': 'INGREDION S.A.',
            'empresa': 'DMV S.A.S.',
            'version': '1.0.0',
            'datos': data
        }
        
        output = io.BytesIO()
        output.write(json.dumps(reporte, indent=2).encode('utf-8'))
        output.seek(0)
        
        return send_file(
            output,
            mimetype='application/json',
            as_attachment=True,
            download_name='reporte_w2605.json'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


import json
