import matplotlib.pyplot as plt
import numpy as np

# ==========================================
# 1. DATOS REALES (Extraídos manualmente de las tablas de análisis - Limite 300s)
# ==========================================
stats_data = [
    # --- ESCENARIO NORMAL ---
    {
        'label': 'Escenario Base\n(Normal)',
        'mean': 8829.40, 
        'std': 2283.27, 
        'min': 5466.5, 
        'max': 14715.0
    },
    # --- ESCENARIO ADR ---
    {
        'label': 'ADR Extremo\n(Peligroso)',
        'mean': 15204.15, 
        'std': 2151.88, 
        'min': 10572.52, 
        'max': 19039.52
    },
    # --- ESCENARIO PESADO ---
    {
        'label': 'Carga Pesada\n(Saturación)',
        'mean': 26359.77, 
        'std': 2452.44, 
        'min': 20729.0, 
        'max': 33239.5
    }
]

# ==========================================
# 2. CÁLCULO DE LA CAJA
# ==========================================
box_data = []

for s in stats_data:
    # Estimación de cuartiles (Q1 y Q3) usando distribución normal
    # Q1 = Media - 0.67 * Std
    # Q3 = Media + 0.67 * Std
    q1 = s['mean'] - 0.6745 * s['std']
    q3 = s['mean'] + 0.6745 * s['std']
    
    # Aseguramos que la caja no exceda los máximos/mínimos reales
    q1 = max(q1, s['min'])
    q3 = min(q3, s['max'])
    
    item = {
        'label': s['label'],
        'mean': s['mean'],   # Línea punteada (Media)
        'med': s['mean'],    # Usamos la media como centro visual
        'q1': q1,
        'q3': q3,
        'whislo': s['min'],  # Bigote Izquierdo: Mínimo Real
        'whishi': s['max'],  # Bigote Derecho: Máximo Real
        'fliers': []         # Sin puntos extraños
    }
    box_data.append(item)

# ==========================================
# 3. GENERACIÓN DEL GRÁFICO
# ==========================================
plt.style.use('seaborn-v0_8-whitegrid')
fig, ax = plt.subplots(figsize=(10, 5))

# Colores: Verde (Normal), Naranja (ADR), Gris/Azul (Pesado)
colores = ['#2ecc71', '#e67e22', '#34495e']

# Dibujar cajas HORIZONTALES (vert=False)
bp = ax.bxp(box_data, vert=False, showmeans=True, meanline=True, patch_artist=True,
            boxprops=dict(linewidth=1.5),
            medianprops=dict(color='black', linewidth=1.5),
            meanprops=dict(color='white', linestyle='--', linewidth=1.5),
            whiskerprops=dict(linewidth=1.5, color='black'),
            capprops=dict(linewidth=1.5, color='black'))

# Aplicar colores
for patch, color in zip(bp['boxes'], colores):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)

# Estética
ax.set_title('Distribución del Coste Operativo según Tipología de Carga (n=30)', 
             fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Coste Operativo (€)', fontsize=12, fontweight='bold')

# Etiquetas de valor (Media) al lado de las cajas
for i, s in enumerate(stats_data):
    ax.text(s['max'] + 500, i + 1, f"Media:\n{int(s['mean'])}€", 
            va='center', fontsize=10, fontweight='bold', color='#444')

# Ajustar márgenes
plt.tight_layout()

nombre_archivo = 'grafico_tipologia_boxplot_final.png'
plt.savefig(nombre_archivo, dpi=300)
print(f"✅ Gráfico generado: {nombre_archivo}")
plt.show()