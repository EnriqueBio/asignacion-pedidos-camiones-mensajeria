import os
import glob
import time
import csv
import sys
import shutil
import json

# Importación segura del modelo
try:
    from pyomo.environ import SolverFactory, value
    from model import model 
    print("✅ Modelo importado correctamente.")
except ImportError as e:
    print("❌ ERROR: No se pudo importar 'model.py'.")
    sys.exit(1)

# ==========================================
# CONFIGURACIÓN
# ==========================================
SALIDA_CSV = "resultados_definitivos.csv"

# Búsqueda de CBC
if os.path.exists("cbc.exe"):
    RUTA_CBC = os.path.abspath("cbc.exe")
else:
    RUTA_CBC = r"C:\Solvers\cbc-2.10.12\bin\cbc.exe"

# Configuraciones
CONFIGURACIONES = [
    {"sec": 20,  "ratio": 0.01, "tag": "Limite_20s"},
    {"sec": 60,  "ratio": 0.01, "tag": "Limite_60s"},
    {"sec": 300, "ratio": 0.01, "tag": "Limite_300s"}
]

# ==========================================
# FUNCIONES
# ==========================================
def analizar_instancia(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            txt = f.read()
            return txt.count("'P"), txt.count("'T")
    except:
        return 0, 0

def obtener_datos_resultado(results, instance):
    """Extrae Objetivo y Gap usando el objeto en memoria."""
    
    # 1. ESTADO
    status = str(results.solver.status)
    term_cond = str(results.solver.termination_condition)
    estado_final = f"{status}/{term_cond}"
    
    # 2. OBJETIVO (Z)
    try:
        # Intentamos leer el objetivo de la instancia cargada
        obj_val = value(instance.OBJ())
    except:
        # Si falla, intentamos leer del objeto results
        try:
            obj_val = results.problem[0].upper_bound
        except:
            obj_val = "Error"

    # 3. GAP (Cálculo)
    gap_str = "N/A"
    
    # CASO A: Si dice "optimal", el Gap es 0 por definición.
    if "optimal" in term_cond.lower():
        gap_str = "0,0"
    
    # CASO B: Si se cortó por tiempo (maxTimeLimit), calculamos manual
    else:
        try:
            # Límites teóricos
            # Upper Bound (UB) = Mejor solución encontrada
            # Lower Bound (LB) = Mejor límite teórico
            ub = results.problem[0].upper_bound
            lb = results.problem[0].lower_bound
            
            if ub is None or lb is None:
                 # A veces están en 'solution' en lugar de 'problem'
                 gap_str = "N/A (No bounds)"
            elif ub == float('inf') or lb == -float('inf'):
                 gap_str = "inf"
            else:
                # Calcular Gap
                # Para minimización: (UB - LB) / UB
                # Evitar división por cero
                denom = abs(ub) if abs(ub) > 1e-9 else 1.0
                gap_val = abs(ub - lb) / denom
                gap_str = str(round(gap_val, 6)).replace('.', ',')
                
        except Exception as e:
            gap_str = "N/A (Error)"

    return estado_final, obj_val, gap_str

CARPETA_DATOS = "bateria_pruebas"
def ejecutar_batch():
    print(f"\n--- INICIANDO EJECUCIÓN (Buscando en '{CARPETA_DATOS}') ---")
    
    # El CSV se guardará fuera, junto al script, para que sea fácil de ver
    with open(SALIDA_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["Archivo", "Pedidos", "Camiones", "Config", "Estado", "Objetivo", "Gap", "Tiempo"])

    # CAMBIO 2: Usar os.path.join para buscar DENTRO de la carpeta
    # Esto busca "bateria_pruebas/*.dat" y "bateria_pruebas/*.txt"
    patron_dat = os.path.join(CARPETA_DATOS, "*.dat")
    patron_txt = os.path.join(CARPETA_DATOS, "*.txt")
    
    archivos = glob.glob(patron_dat) + glob.glob(patron_txt)
    
    # Filtramos para asegurarnos de no coger basura
    archivos = [f for f in archivos if "model.py" not in f and "batch" not in f]
    
    if not archivos:
        print(f"❌ ERROR: No encontré archivos .dat en la carpeta '{CARPETA_DATOS}'.")
        return

    # Ordenamos para que se ejecuten en orden (iter01, iter02...)
    archivos.sort()
    
    for archivo in archivos:
        pedidos, camiones = analizar_instancia(archivo)
        print(f"\n📂 {archivo} (P~{pedidos}, C~{camiones})")
        
        # Fix temporal para .txt
        archivo_uso = archivo
        es_temp = False
        
        # Si hubiera que convertir txt, hay que tener cuidado con la ruta
        if archivo.endswith(".txt"):
            nombre_temp = os.path.join(CARPETA_DATOS, "temp.dat") # Temp dentro de la misma carpeta
            shutil.copy(archivo, nombre_temp)
            archivo_uso = nombre_temp
            es_temp = True

        for config in CONFIGURACIONES:
            etiqueta = config["tag"]
            print(f"   > {etiqueta}...", end=" ", flush=True)
            
            try:
                instance = model.create_instance(archivo_uso)
                opt = SolverFactory("cbc", executable=RUTA_CBC)
                opt.options['sec'] = config["sec"]
                opt.options['ratio'] = config["ratio"]
                
                inicio = time.time()
                results = opt.solve(instance, tee=False) # Silencioso
                duracion = round(time.time() - inicio, 2)
                
                # --- EXTRACCIÓN MEJORADA ---
                estado, obj, gap = obtener_datos_resultado(results, instance)
                # ---------------------------

                print(f"✅ Z={obj} | Gap={gap}")
                
                with open(SALIDA_CSV, "a", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f, delimiter=";")
                    writer.writerow([
                        archivo, pedidos, camiones, 
                        etiqueta, estado, 
                        str(obj).replace(".", ","), 
                        gap, 
                        str(duracion).replace(".", ",")
                    ])
                    
            except Exception as e:
                print(f"❌ FALLO: {e}")
        
        if es_temp: os.remove("temp.dat")

    print(f"\n--- FIN. Abre '{SALIDA_CSV}' en Excel ---")

if __name__ == "__main__":
    ejecutar_batch()