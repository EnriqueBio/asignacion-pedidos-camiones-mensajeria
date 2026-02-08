import matplotlib.pyplot as plt
import numpy as np

# ==========================================
# 1. DATOS EXACTOS
# ==========================================
# Escenario: 400 Pedidos, Límite 300s
flotas = [10, 20, 25, 30, 40]

# Datos copiados manualmente de las tablas de análisis
stats_data = [
    # 10 Camiones
    {'label': '10', 'mean': 51521.52, 'std': 3765.55, 'min': 45273.5, 'max': 59996.0, 'tiempo': 76.09},
    # 20 Camiones
    {'label': '20', 'mean': 36990.95, 'std': 3709.02, 'min': 31858.0, 'max': 46319.0, 'tiempo': 204.66},
    # 25 Camiones
    {'label': '25', 'mean': 29785.18, 'std': 3231.21, 'min': 24703.0, 'max': 36820.5, 'tiempo': 287.94},
    # 30 Camiones
    {'label': '30', 'mean': 21477.65, 'std': 3843.01, 'min': 13321.5, 'max': 33541.0, 'tiempo': 299.41},
    # 40 Camiones
    {'label': '40', 'mean': 6921.54, 'std': 3968.02, 'min': 1072.01, 'max': 19343.0, 'tiempo': 298.23}
]

# Preparamos la estructura para que Matplotlib dibuje la caja sin inventar datos
box_data = []
tiempos = []

for s in stats_data:
    tiempos.append(s['tiempo'])
    
    # CÁLCULO ESTADÍSTICO DE LA CAJA (Q1 y Q3)
    # Usamos la aproximación normal: el 50% central está a +/- 0.67 desviaciones de la media
    q1 = s['mean'] - 0.6745 * s['std']
    q3 = s['mean'] + 0.6745 * s['std']
    
    # Corrección de seguridad: La caja no puede salirse de los bigotes reales
    q1 = max(q1, s['min'])
    q3 = min(q3, s['max'])
    
    item = {
        'label': s['label'],
        'mean': s['mean'],   # La línea punteada verde será la media
        'med': s['mean'],    # Usamos la media como centro visual
        'q1': q1,            # Borde inferior de la caja (calculado con std)
        'q3': q3,            # Borde superior de la caja (calculado con std)
        'whislo': s['min'],  # Bigote inferior: MÍNIMO REAL
        'whishi': s['max'],  # Bigote superior: MÁXIMO REAL
        'fliers': []         # Sin puntos extraños
    }
    box_data.append(item)

# ==========================================
# 2. GENERACIÓN DEL GRÁFICO
# ==========================================
plt.style.use('seaborn-v0_8-whitegrid')
fig, ax1 = plt.subplots(figsize=(10, 6))

# --- EJE IZQ: COSTE (Cajas) ---
ax1.bxp(box_data, showmeans=False, patch_artist=True,
        boxprops=dict(facecolor='lightblue', alpha=0.7, edgecolor='#2980b9'),
        medianprops=dict(color='#2980b9', linewidth=2),
        whiskerprops=dict(color='black', linewidth=1.5),
        capprops=dict(color='black', linewidth=1.5))

ax1.set_xlabel('Tamaño de Flota (Nº Camiones)', fontsize=12, fontweight='bold')
ax1.set_ylabel('Coste Operativo (€)', color='#2980b9', fontsize=12, fontweight='bold')
ax1.tick_params(axis='y', labelcolor='#2980b9')

# --- EJE DER: TIEMPO (Línea Roja) ---
ax2 = ax1.twinx()
ax2.plot(range(1, len(flotas) + 1), tiempos, color='#c0392b', marker='o', linewidth=3, markersize=8, label='Tiempo Medio')

# Línea de límite 300s
ax2.axhline(300, color='red', linestyle='--', alpha=0.5)
ax2.text(3.8, 305, 'Límite (300s)', color='red', fontsize=10, ha='center')

ax2.set_ylabel('Tiempo de Resolución (s)', color='#c0392b', fontsize=12, fontweight='bold')
ax2.tick_params(axis='y', labelcolor='#c0392b')
ax2.set_ylim(0, 330)

plt.title('Coste (Cajas) vs Tiempo (Línea) [400 Pedidos]', fontsize=14, fontweight='bold', pad=15)
plt.tight_layout()

plt.savefig('grafico_2_escalabilidad_final.png', dpi=300)
print("✅ Gráfico generado correctamente.")
plt.show()