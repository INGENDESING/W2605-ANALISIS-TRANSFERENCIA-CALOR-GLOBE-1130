import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

def generar_grafica_ciclo_vida(figures_dir='../results/figures'):
    plt.rcParams.update({
        'font.family': 'serif',
        'font.size': 11,
        'axes.labelsize': 12,
        'legend.fontsize': 10,
        'figure.dpi': 300,
        'savefig.dpi': 300,
        'savefig.bbox': 'tight',
    })

    # Datos base
    tasa_historica = 0.0625  # mm/ano (reporte P2543)
    tasa_fatiga = 0.1200     # mm/ano (nuevo criterio 75C + ciclicidad)
    
    # Virola 1 (Cilindro) - Instalado hace 20 anos
    t_cil_actual = 6.0  # mm
    t_cil_min_req = 4.98 # mm (calculado API 650)
    
    # Fondo Toriesferico - Nuevo (0 anos)
    t_fondo_actual = 9.0 # mm
    # Criterio del 10% de margen de diseño (0.9 mm de sacrificio)
    t_fondo_limite_retiro = t_fondo_actual * 0.90 # 8.1 mm

    # Rango de anos (relativo al presente = 0)
    anos_pasados = -20
    anos_futuros = 25
    
    tiempo_cil = np.linspace(anos_pasados, anos_futuros, 100)
    # El cilindro mantiene tasa historica segun su regimen menos agresivo
    espesor_cilindro = t_cil_actual - tasa_historica * tiempo_cil
    
    # Espesor del fondo nuevo (solo desde t=0) bajo dos escenarios
    tiempo_fondo = np.linspace(0, anos_futuros, 100)
    espesor_fondo_fatiga    = t_fondo_actual - tasa_fatiga    * tiempo_fondo
    espesor_fondo_historico = t_fondo_actual - tasa_historica * tiempo_fondo

    fig, ax = plt.subplots(figsize=(10, 6))

    # Límites mínimos
    ax.axhline(y=t_cil_min_req, color='blue', linestyle='--', alpha=0.6, label=f'Espesor mín. req. cilindro ({t_cil_min_req:.2f} mm)')
    ax.axhline(y=t_fondo_limite_retiro, color='red', linestyle='--', alpha=0.6, label=f'Límite de retiro fondo 10% ({t_fondo_limite_retiro:.1f} mm)')

    # Curvas de corrosión
    ax.plot(tiempo_cil, espesor_cilindro, 'b-', linewidth=2.5, label=f'Cuerpo cilíndrico ({tasa_historica} mm/año)')
    ax.plot(tiempo_fondo, espesor_fondo_historico, 'g-', linewidth=2.5, label=f'Fondo - tasa histórica ({tasa_historica} mm/año)')
    ax.plot(tiempo_fondo, espesor_fondo_fatiga,    'r-', linewidth=2.5, label=f'Fondo - corrosión-fatiga ({tasa_fatiga} mm/año)')

    # Marcar año 0 (Actualidad)
    ax.axvline(x=0, color='gray', linestyle='-', alpha=0.3)
    ax.annotate('Actualidad (t=0)', xy=(0, 8.5), xytext=(1, 8.6), color='gray', weight='bold')

    # Marcar puntos de corte
    corte_cilindro = (t_cil_actual - t_cil_min_req) / tasa_historica  # 16.3 años
    ax.plot(corte_cilindro, t_cil_min_req, 'bo', markersize=8)
    ax.annotate(f'+{corte_cilindro:.1f} años\nRemanente', xy=(corte_cilindro, t_cil_min_req),
                xytext=(corte_cilindro+1, t_cil_min_req+0.2), arrowprops=dict(arrowstyle="->", color='blue'))

    corte_fondo_historico = (t_fondo_actual - t_fondo_limite_retiro) / tasa_historica  # 14.4 años
    ax.plot(corte_fondo_historico, t_fondo_limite_retiro, 'go', markersize=8)
    ax.annotate(f'+{corte_fondo_historico:.1f} años\nLímite 10%\n(histórica)', xy=(corte_fondo_historico, t_fondo_limite_retiro),
                xytext=(corte_fondo_historico+0.8, t_fondo_limite_retiro+0.3), arrowprops=dict(arrowstyle="->", color='green'))

    corte_fondo_fatiga = (t_fondo_actual - t_fondo_limite_retiro) / tasa_fatiga  # 7.5 años
    ax.plot(corte_fondo_fatiga, t_fondo_limite_retiro, 'ro', markersize=8)
    ax.annotate(f'+{corte_fondo_fatiga:.1f} años\nLímite 10%\n(fatiga)', xy=(corte_fondo_fatiga, t_fondo_limite_retiro),
                xytext=(corte_fondo_fatiga+1, t_fondo_limite_retiro+0.3), arrowprops=dict(arrowstyle="->", color='red'), weight='bold')

    ax.set_xlabel('Tiempo [años] (0 = Actualidad)')
    ax.set_ylabel('Espesor [mm]')
    ax.set_title('Proyección de Ciclo de Vida: Corrosión-Fatiga (Nuevo Fondo)')
    ax.grid(True, alpha=0.3)
    ax.legend(loc='lower left', framealpha=0.9)
    ax.set_xlim([anos_pasados-1, anos_futuros])
    ax.set_ylim([4.5, 9.5])
    
    plt.tight_layout()
    os.makedirs(figures_dir, exist_ok=True)
    plt.savefig(os.path.join(figures_dir, 'ciclo_vida_corrosion.pdf'))
    plt.savefig(os.path.join(figures_dir, 'ciclo_vida_corrosion.png'))
    plt.close()
    print(f"Grafica actualizada con tasa de {tasa_fatiga} mm/ano generada exitosamente.")

if __name__ == '__main__':
    generar_grafica_ciclo_vida()
