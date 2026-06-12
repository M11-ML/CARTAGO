"""
Modelo MILP para el CVRP de Florida Bebidas (Cartago).

Variables:
  x_ij  (entero >= 0)  -> número de veces que un camión recorre el arco i->j
  y_ij  (continuo >=0) -> pallets transportados sobre el arco i->j

Restricciones:
  1) Conservación de camiones (balance de grado):
         sum_j x_kj - sum_i x_ik = 0      para todo nodo k
     "Camión entra - Camión sale = 0"

  2) Conservación de pallets (satisfacción de demanda):
         sum_i y_ik - sum_j y_kj = d_k    para todo nodo k
     "Entradas - Salidas = Demanda del cantón"

  3) Acoplamiento capacidad / Gran M:
         y_ij <= 24 * x_ij                para todo i != j
     Si no pasa ningún camión por el arco (x_ij = 0), no puede llevar carga,
     y cada camión que sí pasa lleva como máximo 24 pallets.

Objetivo:
  minimizar  sum_ij  dist_ij * x_ij   (km totales recorridos por la flota)
"""

import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds


def solve_cvrp(dist, demand, capacity=24, k_max=None):
    """
    dist   : matriz de distancias (n x n), nodo 0 = depósito
    demand : lista de demandas (largo n), demand[0] = 0
    capacity: capacidad por camión (pallets)
    k_max  : cota superior (Gran M) sobre cuántas veces se puede usar un arco
    """
    n = len(dist)
    arcs = [(i, j) for i in range(n) for j in range(n) if i != j]
    m = len(arcs)

    total_demand = sum(demand)
    if k_max is None:
        k_max = int(np.ceil(total_demand / capacity)) + 2

    # vector de variables: [x_0..x_{m-1}, y_0..y_{m-1}]
    c = np.zeros(2 * m)
    for idx, (i, j) in enumerate(arcs):
        c[idx] = dist[i][j]

    A_rows, lb_rows, ub_rows = [], [], []

    # (1) balance de camiones por nodo
    for k in range(n):
        row = np.zeros(2 * m)
        for idx, (i, j) in enumerate(arcs):
            if i == k:
                row[idx] += 1
            if j == k:
                row[idx] -= 1
        A_rows.append(row)
        lb_rows.append(0)
        ub_rows.append(0)

    # (2) balance de pallets = demanda
    # En cada cantón: entradas - salidas = demanda (la carga baja al entregar).
    # En el depósito (nodo 0) no aplica conservación normal: el CD es la
    # FUENTE de todo el flujo, por lo que ahí: salidas - entradas = demanda total.
    total_demand = sum(demand)
    for k in range(n):
        row = np.zeros(2 * m)
        for idx, (i, j) in enumerate(arcs):
            if j == k:
                row[m + idx] += 1
            if i == k:
                row[m + idx] -= 1
        A_rows.append(row)
        target = -total_demand if k == 0 else demand[k]
        lb_rows.append(target)
        ub_rows.append(target)

    # (3) y_ij - capacidad * x_ij <= 0   (Gran M / capacidad)
    for idx in range(m):
        row = np.zeros(2 * m)
        row[m + idx] = 1
        row[idx] = -capacity
        A_rows.append(row)
        lb_rows.append(-np.inf)
        ub_rows.append(0)

    A = np.array(A_rows)
    constraints = LinearConstraint(A, lb_rows, ub_rows)

    integrality = np.array([1] * m + [0] * m)
    lb = np.zeros(2 * m)
    ub = np.concatenate([np.full(m, k_max), np.full(m, capacity * k_max)])
    bounds = Bounds(lb, ub)

    res = milp(
        c=c,
        constraints=constraints,
        integrality=integrality,
        bounds=bounds,
        options={"time_limit": 30, "presolve": True},
    )

    if not res.success:
        raise RuntimeError("El modelo no encontró solución: " + res.message)

    x = res.x[:m]
    x_dict = {arcs[idx]: int(round(x[idx])) for idx in range(m) if x[idx] > 0.5}
    return x_dict, res.fun


def extract_routes(x_dict, n):
    """Descompone la solución (multigrafo balanceado) en viajes CD -> ... -> CD."""
    adj = {}
    for (i, j), cnt in x_dict.items():
        adj.setdefault(i, []).extend([j] * cnt)

    routes = []
    while adj.get(0):
        route = [0]
        current = 0
        while True:
            nxt = adj[current].pop()
            if not adj[current]:
                del adj[current]
            route.append(nxt)
            current = nxt
            if current == 0:
                break
        routes.append(route)
    return routes
