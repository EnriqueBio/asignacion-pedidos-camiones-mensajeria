import random
import os

# ==========================================
# CONFIGURACIÓN GENERAL
# ==========================================
CARPETA_SALIDA = "." # Donde se guardarán los .dat

# Datos fijos de base (Clientes y sus distancias aproximadas)
NUM_CLIENTES = 15
CLIENTES = [f"C{i+1}" for i in range(NUM_CLIENTES)]
DISTANCIAS_BASE = {c: random.randint(5, 100) for c in CLIENTES}

# ==========================================
# MOTOR DE GENERACIÓN
# ==========================================
def generar_archivo_dat(nombre_archivo, num_pedidos, num_camiones, perfil="normal"):
    print(f"Generando {nombre_archivo} ({perfil})...")
    
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write(f"# Escenario generado automaticamente: {perfil}\n\n")
        
        # 1. PARÁMETROS GLOBALES
        alpha = 0.5 if perfil != "caro" else 1.5  # Si el escenario es "caro", sube el coste km
        f.write(f"param alpha := {alpha};\n")
        f.write("param fecha_hoy := 45984;\n")
        f.write("param s := 100;\n\n")
        
        # 2. SETS (Conjuntos)
        # Pedidos
        lista_pedidos = [f"P{i+1}" for i in range(num_pedidos)]
        f.write(f"set I := {' '.join(lista_pedidos)};\n")
        
        # Clientes
        f.write(f"set C := {' '.join(CLIENTES)};\n")
        
        # Camiones
        lista_camiones = [f"T{j+1}" for j in range(num_camiones)]
        f.write(f"set J := {' '.join(lista_camiones)};\n\n")
        
        # 3. PARÁMETROS DE CLIENTES
        f.write("param dist_c :=\n")
        for c in CLIENTES:
            # Pequeña variación aleatoria en la distancia
            dist = max(1, DISTANCIAS_BASE[c] + random.randint(-5, 5))
            f.write(f"  '{c}' {dist}\n")
        f.write(";\n\n")
        
        # 4. PARÁMETROS DE CAMIONES (Simulamos flota heterogénea)
        # Tipos: [PesoMax, VolMax, CosteFijo, ADR]
        tipos_camion = [
            (3500, 25, 700, 1), # Grande
            (2500, 18, 550, 0), # Mediano
            (1000, 10, 350, 0)  # Pequeño
        ]
        
        datos_camiones = {}
        for t in lista_camiones:
            tipo = random.choice(tipos_camion)
            datos_camiones[t] = tipo

        # Escribir param F (Coste Fijo)
        f.write("param F :=\n")
        for t, data in datos_camiones.items():
            f.write(f"  '{t}' {data[2]}\n")
        f.write(";\n")

        # Escribir param ADRmax (Capacidad ADR)
        f.write("param ADRmax :=\n")
        for t, data in datos_camiones.items():
            limit = 5 if data[3] == 1 else 0 # Si es ADR, permite 5 puntos, si no 0
            f.write(f"  '{t}' {limit}\n")
        f.write(";\n")

        # Escribir W (Peso) y V (Volumen) y Pmax
        f.write("param W :=\n")
        for t, data in datos_camiones.items(): f.write(f"  '{t}' {data[0]}\n")
        f.write(";\n")
        
        f.write("param V :=\n")
        for t, data in datos_camiones.items(): f.write(f"  '{t}' {data[1]}\n")
        f.write(";\n")

        f.write("param Pmax :=\n") # Paradas máximas aleatorias entre 4 y 10
        for t in lista_camiones: f.write(f"  '{t}' {random.randint(4, 10)}\n")
        f.write(";\n\n")

        # 5. PARÁMETROS DE PEDIDOS (Aquí aplicamos el "perfil")
        datos_pedidos = {}
        for p in lista_pedidos:
            # Lógica según el perfil
            es_adr = 0
            peso = random.randint(100, 300)
            vol = random.randint(1, 3)
            
            if perfil == "adr_extremo":
                if random.random() < 0.6: es_adr = 1 # 60% probabilidad de ser ADR
            elif perfil == "adr_medio":
                if random.random() < 0.5: es_adr = 1 # 50% probabilidad de ser ADR
            elif perfil == "adr_bajo":
                if random.random() < 0.25: es_adr = 1 # 25% probabilidad de ser ADR
            elif perfil == "pesado":
                peso = random.randint(500, 1200) # Pedidos muy pesados
                vol = random.randint(3, 6)
            else: # Normal
                if random.random() < 0.1: es_adr = 1 # 10% probabilidad ADR

            cliente = random.choice(CLIENTES)
            datos_pedidos[p] = {
                "pes": peso, "vol": vol, "adr": es_adr, "cli": cliente,
                "t": 350, # Coste mensajería fijo
                "fecha": 45984 + (0 if random.random() < 0.7 else 1) # 70% para hoy, 30% mañana
            }

        # Escribir params de pedidos
        for param in ["pes", "vol", "adr", "t", "fecha", "cli"]:
            f.write(f"param {param} :=\n")
            for p, d in datos_pedidos.items():
                val = d[param]
                if param == "cli": val = f"'{val}'"
                f.write(f"  '{p}' {val}\n")
            f.write(";\n")

# ==========================================
# EJECUCIÓN: CREAR LOS ESCENARIOS
# ==========================================
if __name__ == "__main__":
    NUM_ITERACIONES = 30
    
    # Crea una carpeta para no inundar el directorio principal
    if not os.path.exists("bateria_pruebas"):
        os.makedirs("bateria_pruebas")

    print(f"--- Generando {NUM_ITERACIONES} instancias por escenario ---")

    # Bucle para generar las 30 copias con semillas aleatorias distintas
    for i in range(1, NUM_ITERACIONES + 1):
        # Formato de nombre: "escenario_iteracion.dat"
        # Usamos f"{i:02d}" para que salga 01, 02... y se ordenen bien.
        '''
        generar_archivo_dat(f"bateria_pruebas/run_40p_05c_iter{i:02d}.dat", 40, 5, "normal")
        generar_archivo_dat(f"bateria_pruebas/run_60p_05c_iter{i:02d}.dat", 60, 5, "normal")
        generar_archivo_dat(f"bateria_pruebas/run_80p_05c_iter{i:02d}.dat", 80, 5, "normal")
        generar_archivo_dat(f"bateria_pruebas/run_100p_05c_iter{i:02d}.dat", 100, 5, "normal")
        generar_archivo_dat(f"bateria_pruebas/run_100p_10c_iter{i:02d}.dat", 100, 10, "normal")
        
        generar_archivo_dat(f"bateria_pruebas/run_200p_10c_iter{i:02d}.dat", 200, 10, "normal")
        generar_archivo_dat(f"bateria_pruebas/run_400p_10c_iter{i:02d}.dat", 400, 10, "normal")
        generar_archivo_dat(f"bateria_pruebas/run_400p_20c_iter{i:02d}.dat", 400, 20, "normal")
        generar_archivo_dat(f"bateria_pruebas/run_400p_25c_iter{i:02d}.dat", 400, 25, "normal")
        generar_archivo_dat(f"bateria_pruebas/run_400p_30c_iter{i:02d}.dat", 400, 30, "normal")
        generar_archivo_dat(f"bateria_pruebas/run_400p_40c_iter{i:02d}.dat", 400, 40, "normal")
        
        generar_archivo_dat(f"bateria_pruebas/run_200p_ADRE_iter{i:02d}.dat", 200, 15, "adr_extremo")
        generar_archivo_dat(f"bateria_pruebas/run_200p_ADRM_iter{i:02d}.dat", 200, 15, "adr_medio")
        generar_archivo_dat(f"bateria_pruebas/run_200p_ADRB_iter{i:02d}.dat", 200, 15, "adr_bajo")
        '''

        generar_archivo_dat(f"bateria_pruebas/run_200p_normal_iter{i:02d}.dat", 200, 15, "normal")
        generar_archivo_dat(f"bateria_pruebas/run_200p_ADR_iter{i:02d}.dat", 200, 15, "adr_extremo")
        generar_archivo_dat(f"bateria_pruebas/run_200p_pesado_iter{i:02d}.dat", 200, 15, "pesado")
        
        if i % 5 == 0: print(f"Generate {i}...")

    print("\n✅ ¡Listo! Los archivos generados se encuentran en 'bateria_pruebas'.")