# 🚚 Florida Bebidas — CVRP Cartago

App de Streamlit que resuelve el problema de ruteo de vehículos con capacidad
(CVRP) para la distribución semanal de Florida Bebidas (Imperial, Pilsen,
Tropical) a los 8 cantones de la provincia de **Cartago**, desde el Centro de
Distribución (CD Cartago).

## ¿Qué hace?

- Permite editar la **demanda semanal** (pallets) de cada cantón.
- Calcula automáticamente la tabla de demanda por producto (split 50/25/25:
  Imperial / Pilsen / Tropical).
- Resuelve un modelo **MILP** (con `scipy.optimize.milp` / HiGHS) que minimiza
  los kilómetros totales recorridos por la flota, sujeto a:
  1. **Conservación de camiones**: camiones que entran a un cantón = camiones
     que salen.
  2. **Conservación de pallets**: entradas − salidas = demanda del cantón.
  3. **Gran M / capacidad**: un camión solo lleva carga si transita el arco, y
     como máximo **24 pallets** por viaje.
- Muestra el **detalle de cada viaje** (ruta y distancia) y un **mapa
  interactivo** de Cartago con las rutas óptimas marcadas en rojo.

## Estructura del proyecto

```
cartago-cvrp/
├── app.py            # App de Streamlit (UI, tabla, mapa)
├── solver.py         # Modelo MILP del CVRP + extracción de rutas
├── data.py           # Distancias, demandas por defecto, coordenadas
├── requirements.txt
└── README.md
```

## Cómo correrlo localmente

```bash
git clone <tu-repo>
cd cartago-cvrp
pip install -r requirements.txt
streamlit run app.py
```

## Desplegar en Streamlit Community Cloud

1. Sube esta carpeta a un repositorio de GitHub.
2. Ve a [share.streamlit.io](https://share.streamlit.io), conecta tu repo.
3. Indica `app.py` como archivo principal.
4. ¡Listo! La app quedará pública con una URL de `*.streamlit.app`.

## Datos base

- **Capacidad por camión**: 24 pallets.
- **Demanda total Cartago**: 406 pallets/semana (8 cantones).
- **Matriz de distancias** por carretera (km), provista en el caso del curso
  *II-1122 Modelos de Optimización Industrial — UCR*.

## Notas del modelo

El modelo agrega todos los viajes en una única variable $x_{ij}$ (número de
veces que se recorre el arco $i \to j$) y una variable de flujo $y_{ij}$
(pallets transportados). Al resolver, se obtiene la combinación óptima de
arcos; luego `extract_routes` descompone esa solución en viajes individuales
CD → … → CD (cada viaje es un camión que sale, entrega y regresa).
