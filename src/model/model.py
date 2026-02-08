# ====================================================
#   MODELO DE ASIGNACIÓN DE PEDIDOS A CAMIONES
#   Pyomo + SolverStudio
# ====================================================

from pyomo.environ import *

# ----------------------------------------------------
# 1) DECLARAR MODELO ABSTRACTO
# ----------------------------------------------------
model = AbstractModel()

# ----------------------------------------------------
# 2) CONJUNTOS
# ----------------------------------------------------
model.I = Set()      # pedidos
model.J = Set()      # camiones
model.C = Set()      # clientes

# ----------------------------------------------------
# 3) PARÁMETROS
# ----------------------------------------------------

# --- parámetros de pedidos
model.vol   = Param(model.I)
model.pes   = Param(model.I)
model.fecha = Param(model.I, within=Reals)   # fecha del pedido (número o formato convertible)
model.adr   = Param(model.I)
model.t     = Param(model.I)   # coste mensajería

model.cli   = Param(model.I, within=model.C)   # cliente al que pertenece cada pedido

# --- parámetros de clientes
model.dist_c = Param(model.C, within=Reals)  # distancia del cliente

# --- parámetros de camiones
model.V     = Param(model.J)   # volumen
model.W     = Param(model.J)   # peso
model.ADRmax = Param(model.J)  # límite ADR
model.Pmax   = Param(model.J)  # paradas máximas
model.F      = Param(model.J, within=Reals)  # coste fijo

# --- parámetros globales
model.alpha = Param(within=Reals)          # factor €/km
model.s     = Param(within=Reals)          # coeficiente de incentivo temporal
model.fecha_hoy = Param(within=Reals)      # fecha actual


# ----------------------------------------------------
# 4) PARÁMETROS DERIVADOS
# ----------------------------------------------------

# Distancia por pedido i (hereda del cliente)
def dist_i_rule(m, i):
    return m.dist_c[m.cli[i]]
model.dist = Param(model.I, initialize=dist_i_rule)

# Coste variable: u_i = alpha * dist
def u_rule(m, i):
    return m.alpha * m.dist[i]
model.u = Param(model.I, initialize=u_rule)

# Días adelantados: d_i = fecha_i - fecha_hoy
def d_rule(m, i):
    return m.fecha[i] - m.fecha_hoy
model.d = Param(model.I, initialize=d_rule)

# Fecha del envío más lejano
def fmax_rule(m):
    return max(m.fecha[i] for i in m.I)
    
model.Fmax = Param(initialize=fmax_rule)

# C) Delta (Beneficio por Anticipación)
def delta_rule(m, i):
    if m.Fmax > 0:
        return (m.Fmax - m.d[i])/m.Fmax
    else:
        # Si todos los pedidos son de hoy, el beneficio es max (1)
        return 1.0
model.delta = Param(model.I, initialize=delta_rule)

# ----------------------------------------------------
# 5) VARIABLES
# ----------------------------------------------------
model.x = Var(model.I, model.J, domain=Binary)   # pedido i va en camión j
model.y = Var(model.I, domain=Binary)            # pedido i va por mensajería
model.z = Var(model.J, domain=Binary)            # camión usado

# ----------------------------------------------------
# 6) FUNCIÓN OBJETIVO
# ----------------------------------------------------
def obj_rule(m):
    return (
        sum(m.u[i] * m.x[i, j] for i in m.I for j in m.J)        # coste variable camión
        + sum(m.t[i] * m.y[i] for i in m.I)                      # mensajería
        + sum(m.F[j] * m.z[j] for j in m.J)                      # coste fijo camión
        - sum(m.s * m.delta[i] * (sum(m.x[i, j] for j in m.J) + m.y[i]) 
              for i in m.I)                                      # adelanto
    )
model.OBJ = Objective(rule=obj_rule, sense=minimize)

# ----------------------------------------------------
# 7) RESTRICCIONES
# ----------------------------------------------------

# A) Todos los pedidos del día se envían
def hoy_rule(m, i):
    if m.fecha[i] == m.fecha_hoy:
        return sum(m.x[i, j] for j in m.J) + m.y[i] == 1
    return Constraint.Skip
model.envio_hoy = Constraint(model.I, rule=hoy_rule)

# B) Pedidos futuros: envío opcional
def futuro_rule(m, i):
    if m.fecha[i] > m.fecha_hoy:
        return sum(m.x[i, j] for j in m.J)<= 1
    return Constraint.Skip
model.envio_fut = Constraint(model.I, rule=futuro_rule)

# Los envíos futuros NO se envían por mensajería
def futuro_mens_rule(m, i):
    if m.fecha[i] > m.fecha_hoy:
        return m.y[i] == 0
    return Constraint.Skip
model.futuro_mens = Constraint(model.I, rule=futuro_mens_rule)

# C) Solo cargar camión si se usa
def linking_rule(m, i, j):
    return m.x[i, j] <= m.z[j]
model.link = Constraint(model.I, model.J, rule=linking_rule)

# D) Capacidad volumen
def volumen_rule(m, j):
    return sum(m.vol[i] * m.x[i, j] for i in m.I) <= m.V[j]
model.volumen = Constraint(model.J, rule=volumen_rule)

# E) Capacidad peso
def peso_rule(m, j):
    return sum(m.pes[i] * m.x[i, j] for i in m.I) <= m.W[j]
model.peso = Constraint(model.J, rule=peso_rule)

# F) ADR máximo
def adr_rule(m, j):
    return sum(m.adr[i] * m.vol[i] * m.x[i, j] for i in m.I) <= m.ADRmax[j]
model.adr_limit = Constraint(model.J, rule=adr_rule)

# G) Paradas máximas
def paradas_rule(m, j):
    return sum(m.x[i, j] for i in m.I) <= m.Pmax[j]
model.paradas = Constraint(model.J, rule=paradas_rule)




