import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

def graficar_resistencias(figures_dir='../figures'):
    plt.rcParams.update({
        'font.family': 'serif',
        'font.size': 12,
        'figure.dpi': 300,
        'savefig.dpi': 300,
        'savefig.bbox': 'tight',
    })

    labels = ['Agua en media ca\u00f1a (1.4%)', 'Pared de acero SS316L (8.3%)', 'Glucosa - Convecci\u00f3n Natural (90.3%)']
    sizes = [1.4, 8.3, 90.3]
    colors = ['#3498db', '#95a5a6', '#e74c3c']
    explode = (0, 0, 0.1)  # Destacar la glucosa

    fig, ax = plt.subplots(figsize=(8, 6))
    wedges, texts = ax.pie(sizes, explode=explode, colors=colors, startangle=140, 
                           wedgeprops=dict(width=0.4, edgecolor='w'))
    
    # Leyenda en lugar de texto sobre el grafico para aspecto mas profesional (Elsevier)
    ax.legend(wedges, labels,
              title="Componentes de Resistencia T\u00e9rmica",
              loc="center left",
              bbox_to_anchor=(1, 0, 0.5, 1))

    ax.set_title("Distribuci\u00f3n de la Resistencia T\u00e9rmica Global (U)")
    
    os.makedirs(figures_dir, exist_ok=True)
    plt.savefig(os.path.join(figures_dir, 'resistencias_termicas.pdf'))
    plt.savefig(os.path.join(figures_dir, 'resistencias_termicas.png'))
    plt.close()
    print("Gr\u00e1fico de resistencias generado.")

if __name__ == '__main__':
    graficar_resistencias()
