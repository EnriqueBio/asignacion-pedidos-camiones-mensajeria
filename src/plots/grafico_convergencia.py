import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# ==========================================
# 1. DATOS REALES (Media y Desviación Típica)
# ==========================================
# Tiempos de evaluación
tiempos = [20, 60, 300]

# --- Escenario 400p / 25 Camiones ---
# Muestra mejora rápida al principio y luego se estanca
mean_25c = [49554.64, 35377.35, 29785.18]
std_25c  = [8209.79,  7406.68,  3231.21]

# --- Escenario 400p / 30 Camiones ---
# Le cuesta arrancar pero encuentra una solución mucho mejor al final
mean_30c = [53340.52, 48249.13, 21477.65]
std_30c  = [6219.46,  11483.92, 3843.01]

# ==========================================
# 2. CONFIGURACIÓN DEL GRÁFICO
# ==========================================
sns.set_theme(style="whitegrid")
plt.figure(figsize=(10, 6))

# --- PLOT 400p / 25c (Naranja) ---
plt.plot(tiempos, mean_25c, color='#e67e22', marker='o', linewidth=3, markersize=8, label='400p / 25 Camiones (Media)')
# Área de sombra (Media +/- Desviación)
plt.fill_between(tiempos, 
                 np.array(mean_25c) - np.array(std_25c), 
                 np.array(mean_25c) + np.array(std_25c), 
                 color='#e67e22', alpha=0.2, label='Dispersión (±1 std)')

# --- PLOT 400p / 30c (Morado) ---
plt.plot(tiempos, mean_30c, color='#8e44ad', marker='s', linewidth=3, markersize=8, linestyle='--', label='400p / 30 Camiones (Media)')
plt.fill_between(tiempos, 
                 np.array(mean_30c) - np.array(std_30c), 
                 np.array(mean_30c) + np.array(std_30c), 
                 color='#8e44ad', alpha=0.15) # Sin label para no ensuciar la leyenda

# ==========================================
# 3. DETALLES Y ANOTACIONES
# ==========================================
plt.title('Convergencia del Coste Operativo: Evolución Temporal (n=30)', fontsize=14, fontweight='bold', pad=20)
plt.xlabel('Tiempo de Resolución (segundos)', fontsize=12, fontweight='bold')
plt.ylabel('Coste Operativo (€)', fontsize=12, fontweight='bold')

# Ejes y Límites
plt.xticks([20, 60, 300])
plt.xlim(10, 320)

# Anotación "Rendimientos Decrecientes" (Para el caso 25c)
plt.annotate('Rendimientos\ndecrecientes', 
             xy=(60, 35377), xytext=(80, 50000),
             arrowprops=dict(facecolor='#e67e22', shrink=0.05),
             fontsize=10, color='#d35400', fontweight='bold')

# Anotación "Mejora Tardía" (Para el caso 30c)
plt.annotate('Salto de Calidad\n(>60s)', 
             xy=(250, 24000), xytext=(200, 40000),
             arrowprops=dict(facecolor='#8e44ad', shrink=0.05),
             fontsize=10, color='#8e44ad', fontweight='bold')

plt.legend(loc='upper right', frameon=True, framealpha=0.9)
plt.tight_layout()

plt.savefig('grafico_3_convergencia_final.png', dpi=300)
print("✅ Gráfico generado: grafico_3_convergencia_final.png")
plt.show()