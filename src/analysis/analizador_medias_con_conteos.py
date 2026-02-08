import pandas as pd
import re
import os

ARCHIVO_CSV = "resultados_definitivos.csv"

# 1. CABECERAS MANUALES (Por seguridad, ya que se te borraron)
COLUMNAS = ["Archivo", "Pedidos", "Camiones", "Config", "Estado", "Objetivo", "Gap", "Tiempo"]

def analizar_resultados():
    print(f"📊 Analizando éxitos y fallos en {ARCHIVO_CSV}...")
    
    # 2. CARGA BLINDADA
    try:
        df = pd.read_csv(ARCHIVO_CSV, sep=';', header=None, names=COLUMNAS, engine='python')
    except Exception as e:
        print(f"❌ Error leyendo: {e}")
        return

    # 3. LIMPIEZA DE NÚMEROS
    cols = ['Objetivo', 'Gap', 'Tiempo']
    for col in cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace(',', '.', regex=False)
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    # 4. LIMPIEZA DE NOMBRES
    def limpiar_nombre(nombre):
        if not isinstance(nombre, str): return str(nombre)
        nombre_sin_ruta = os.path.basename(nombre) 
        clean = re.sub(r'_iter\d+', '', nombre_sin_ruta).replace('.dat', '').replace('.txt', '')
        return clean

    df['Escenario'] = df['Archivo'].apply(limpiar_nombre)

    # ==========================================
    # NUEVA LÓGICA DE CONTEO
    # ==========================================
    
    # Definimos qué es "Óptimo": Gap menor o igual al 1% (0.01)
    # (Usamos 0.011 para evitar problemas de redondeo con el 0.01 exacto)
    df['Es_Optimo'] = df['Gap'] <= 0.011
    
    # Definimos qué es "Difícil/No Resuelto": Gap mayor o igual a 1.0
    df['Es_Dificil'] = df['Gap'] >= 0.999

    # Agrupamos calculando:
    # - count: Total de instancias
    # - sum: Suma de True (1) y False (0) para contar óptimos
    resumen = df.groupby(['Escenario', 'Config']).agg({
        'Objetivo': 'mean',          # Coste medio
        'Tiempo': 'mean',            # Tiempo medio
        'Gap': 'mean',               # Gap medio
        'Es_Optimo': 'sum',          # Cuántos óptimos
        'Es_Dificil': 'sum',         # Cuántos difíciles
        'Archivo': 'count'           # Total de intentos
    })

    # Renombramos columnas para que quede bonito en el Excel
    resumen = resumen.rename(columns={
        'Objetivo': 'Coste_Medio',
        'Tiempo': 'Tiempo_Medio',
        'Gap': 'Gap_Medio',
        'Es_Optimo': 'N_Optimos',
        'Es_Dificil': 'N_GapAlto',
        'Archivo': 'Total_Iteraciones'
    })
    
    # Calculamos % de Éxito
    resumen['%_Exito'] = (resumen['N_Optimos'] / resumen['Total_Iteraciones']) * 100
    
    resumen = resumen.round(2)

    print("\n--- TABLA DE RESULTADOS CON CONTEOS ---")
    print(resumen[['N_Optimos', 'N_GapAlto', 'Total_Iteraciones', '%_Exito']])
    
    output = "resumen_final_conteos.csv"
    resumen.to_csv(output, sep=";")
    print(f"\n✅ Guardado en '{output}'")

if __name__ == "__main__":
    analizar_resultados()