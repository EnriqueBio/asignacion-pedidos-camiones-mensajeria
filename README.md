# Asignación Diaria de Pedidos a Camiones y Mensajería

Este repositorio contiene el código, los datos de prueba y los resultados asociados al Trabajo Fin de Grado titulado **“Optimización de la asignación diaria de pedidos a flota propia y mensajería externa”**.  
El objetivo del proyecto es modelar y resolver el problema de planificación diaria del transporte en una empresa logística, decidiendo de forma óptima qué pedidos se asignan a flota propia y cuáles se externalizan mediante mensajería, bajo restricciones reales de capacidad, costes y normativa ADR.

El problema se aborda mediante un modelo de **Programación Lineal Entera Mixta (MILP)** implementado en **Pyomo**, integrado en **Microsoft Excel** a través del complemento **SolverStudio**.

---

## Estructura del repositorio

```text
├── docs/
│   └── memoria_TFG.pdf
│
├── src/
│   ├── model/
│   │   ├── model.py
│   │   └── batch_plem_final_gap.py
│   ├── generator/
│   │   └── generador_masivo.py
│   ├── analysis/
│   │   ├── analizador_medias.py
│   │   └── analizador_medias_con_conteos.py
│   └── plots/
│       ├── grafico_convergencia.py
│       ├── grafico_escalabilidad.py
│       └── grafico_tipologia.py
│
├── data/
│   ├── inputs/
│   │   ├── 40P5C.xlsx
│   │   ├── 100P10C.xlsx
│   │   └── 400P30C-time.xlsx
│   ├── instances/
│   │   ├── bateria_pruebas_40-100/
│   │   ├── bateria_pruebas_200-400/
│   │   ├── bateria_pruebas_ADR/
│   │   └── bateria_pruebas_Normal_ADR_Pesado/
│   └── results/
│       ├── results_40-100/
│       ├── results_200-400/
│       ├── results_200_ADR/
│       └── results_200_Normal_ADR_Pesado/
│
├── requirements.txt
└── README.md
```



---

## Descripción general

- **Modelo**: Programación Lineal Entera Mixta (MILP)
- **Lenguaje**: Python
- **Librería de modelado**: Pyomo
- **Entorno de ejecución**: SolverStudio (Excel)
- **Solver por defecto**: CBC

El modelo permite:
- Decidir la asignación diaria de pedidos a camiones propios o mensajería externa
- Gestionar restricciones de volumen, peso, número de paradas y mercancías peligrosas (ADR)
- Analizar el dilema **Make-or-Buy**
- Incorporar un incentivo para la anticipación de pedidos futuros
- Evaluar escalabilidad, tiempos de cómputo y soluciones cuasi-óptimas

---

## Datos y experimentos

- Los **experimentos computacionales** se han realizado sobre **30 instancias independientes por escenario**, generadas de forma estocástica.
- En el repositorio se incluyen **únicamente instancias representativas** de cada escenario a modo de ejemplo.
- Los **resultados agregados** (costes medios, tiempos, gaps, etc.) se encuentran en la carpeta `data/results/` y corresponden a los valores analizados en la memoria.

---

## Ejecución del modelo

El modelo se ha utilizado en dos modos de ejecución distintos, en función del objetivo perseguido.

### Ejecución interactiva en Excel (SolverStudio)

Para el uso interactivo y la validación funcional del modelo, se emplea el complemento **SolverStudio** integrado en **Microsoft Excel**.  
Los ficheros Excel incluidos en este repositorio ya contienen:

- El modelo Pyomo cargado en SolverStudio
- La configuración del solver

Esto permite a un usuario ejecutar el modelo directamente desde Excel sin necesidad de modificar el código Python, facilitando su adopción en entornos empresariales no técnicos.

### Ejecución automática por lotes (Pyomo + SolverFactory)

Para la realización de experimentos computacionales a gran escala, el modelo se ejecuta de forma independiente a Excel mediante scripts en Python.  
En este caso:

- Las instancias del problema se generan como ficheros `.dat`
- El modelo Pyomo se carga directamente desde Python
- El solver CBC se invoca mediante `SolverFactory`
- Se establecen límites de tiempo y tolerancias
- Los resultados se agregan automáticamente en ficheros CSV

Este enfoque permite evaluar escalabilidad, tiempos de cómputo y calidad de las soluciones de forma sistemática y reproducible.

> **Nota sobre la ejecución automática**

La organización del repositorio responde a criterios de **claridad, trazabilidad y reproducibilidad académica**, no a una ejecución directa. Para la ejecución, se deben tener en cuenta las rutas locales, ajustando las rutas relativas según la organización local del proyecto.

Los scripts incluidos en el repositorio se ejecutan desde línea de comandos utilizando un intérprete de Python correctamente configurado.

Ejemplo de ejecución del generador de instancias:

python generador_masivo.py

De forma análoga, el resto de scripts de generación, análisis y visualización
pueden ejecutarse mediante:

python nombre_del_script.py

En algunos entornos puede ser necesario utilizar `python3` en lugar de `python`,
dependiendo de la configuración del sistema.


---

## Dependencias

Las principales dependencias utilizadas son:

- Python 3.x
- Pyomo
- SolverStudio
- CBC (solver de optimización)

Las dependencias Python específicas del proyecto se detallan en `requirements.txt`. Pueden instalarse mediante:

pip install -r requirements.txt


---

## Reproducibilidad

El repositorio ha sido estructurado con el objetivo de garantizar la **reproducibilidad académica** de los resultados presentados en la memoria, manteniendo al mismo tiempo claridad y trazabilidad en los distintos componentes del proyecto.

La reproducción completa de los experimentos se basa en los siguientes elementos:

- **Modelo de optimización**
  El modelo matemático está implementado en Pyomo y disponible en `src/model/model.py`. La formulación es independiente de los datos, lo que permite reutilizar el código para distintos escenarios sin modificaciones.

- **Generación de instancias**
  Las instancias del problema se generan de forma estocástica mediante el script `src/generator/generador_masivo.py`.
  Para cada escenario experimental se generan 30 instancias independientes que comparten la misma estructura, pero difieren en la distribución concreta de pedidos, clientes y capacidades, tal y como se describe en la memoria.

- **Instancias incluidas en el repositorio**
  Por motivos de claridad y tamaño, en el repositorio se incluyen únicamente **instancias representativas** de cada escenario en la carpeta `data/instances/`.
  Estas instancias permiten verificar la correcta ejecución del modelo y comprender el formato de los datos utilizados, mientras que los resultados agregados corresponden a la resolución completa de todas las instancias generadas durante el estudio.

- **Resolución del modelo**  
  El modelo puede resolverse de dos formas:
  - De manera interactiva mediante SolverStudio y los ficheros Excel incluidos en `data/inputs/`, que ya contienen la configuración necesaria.
  - De forma automática por lotes mediante scripts en Python que cargan directamente los ficheros `.dat` y ejecutan el solver CBC a través de `SolverFactory`.

- **Análisis de resultados**
  Los resultados individuales se agregan y analizan mediante los scripts disponibles en `src/analysis/`.  
  Los ficheros CSV generados, que contienen medias, conteos y métricas globales, se encuentran en `data/results/` y son los utilizados para la elaboración de tablas y gráficos en la memoria.

Este enfoque garantiza que los resultados puedan ser reproducidos siguiendo el mismo procedimiento experimental, al tiempo que se evita la dependencia de configuraciones locales específicas o de rutas rígidas en el sistema de archivos.

> **Nota sobre los scripts de visualización**

Los scripts de generación de gráficos utilizan valores agregados (medias,
desviaciones, mínimos y máximos) extraídos previamente de las tablas de resultados.
Estos valores se incorporan manualmente en los scripts con el objetivo de reproducir
exactamente las figuras presentadas en la memoria.

---

## Licencia y uso académico

Este repositorio se proporciona con fines **académicos y educativos**.  
Puede utilizarse como referencia o base para trabajos posteriores en planificación del transporte, optimización logística o investigación operativa.

---

