import pandas as pd
import re
import os

ARCHIVO_CSV = "resultados_definitivos.csv"

# 1. DEFINIMOS LOS NOMBRES DE LAS COLUMNAS MANUALMENTE
# (Esto es necesario porque a veces al volcar en excel se pierde alguna fila)
COLUMNAS = ["Archivo", "Pedidos", "Camiones", "Config", "Estado", "Objetivo", "Gap", "Tiempo"]

def analizar_resultados():
    print(f"Leemos {ARCHIVO_CSV} asignando nombres de columnas manualmente...")
    
    # 2. CARGAMOS DATOS
    # header=None: Le decimos que NO busque títulos en el archivo
    # names=COLUMNAS: Le damos nosotros los nombres correctos
    try:
        df = pd.read_csv(ARCHIVO_CSV, sep=';', header=None, names=COLUMNAS, engine='python')
    except Exception as e:
        print(f"Error leyendo el archivo: {e}")
        return

    # Limpieza de números (coma -> punto)
    cols = ['Objetivo', 'Gap', 'Tiempo']
    for col in cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace(',', '.', regex=False)
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    # --- Agrupar por "Familia" de instancia ---
    def limpiar_nombre(nombre):
        # Evitamos error si el nombre no es texto
        if not isinstance(nombre, str): return str(nombre)
        
        nombre_sin_ruta = os.path.basename(nombre) 
        clean = re.sub(r'_iter\d+', '', nombre_sin_ruta).replace('.dat', '').replace('.txt', '')
        return clean

    df['Escenario'] = df['Archivo'].apply(limpiar_nombre)

    # --- CÁLCULO DE MEDIAS ---
    # Añadimos 'count' para ver cuántas iteraciones ha cogido (deberían ser ~30)
    resumen = df.groupby(['Escenario', 'Config'])[['Objetivo', 'Gap', 'Tiempo']].agg(['count', 'mean', 'std', 'min', 'max'])
    
    # Redondeamos
    resumen = resumen.round(2)

    print("\n--- TABLA DE MEDIAS ---")
    print(resumen)
    
    # Guardar en CSV con separador de punto y coma
    resumen.to_csv("resumen_medias_tfg.csv", sep=";")
    print("\n✅ Guardado en 'resumen_medias_tfg.csv'")

if __name__ == "__main__":
    analizar_resultados()