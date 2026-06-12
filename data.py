"""
Datos base del problema — Florida Bebidas, Provincia de Cartago
Fuente: hoja de datos del Caso (8 cantones + CD Cartago)
"""

# Nombres de los nodos (0 = Centro de Distribución)
NAMES = {
    0: "CD Cartago",
    1: "Cartago",
    2: "Paraíso",
    3: "La Unión",
    4: "Jiménez",
    5: "Turrialba",
    6: "Alvarado",
    7: "Oreamuno",
    8: "El Guarco",
}

# Matriz de distancias por carretera (km) — nodo 0..8
DIST = [
    [0,  0,  9, 10, 34, 34, 20, 6,  6],
    [0,  0,  9, 10, 34, 34, 20, 6,  6],
    [9,  9,  0, 19, 26, 28, 13, 7, 12],
    [10, 10, 19, 0, 45, 43, 29, 14, 11],
    [34, 34, 26, 45, 0, 20, 21, 31, 37],
    [34, 34, 28, 43, 20, 0, 15, 29, 40],
    [20, 20, 13, 29, 21, 15, 0, 14, 25],
    [6,  6,  7, 14, 31, 29, 14, 0, 12],
    [6,  6, 12, 11, 37, 40, 25, 12, 0],
]

# Demanda semanal total (pallets) por cantón — valores por defecto
DEFAULT_DEMAND = {
    1: 124,  # Cartago
    2: 48,   # Paraíso
    3: 75,   # La Unión
    4: 15,   # Jiménez
    5: 61,   # Turrialba
    6: 12,   # Alvarado
    7: 36,   # Oreamuno
    8: 35,   # El Guarco
}

# Split de productos (Imperial / Pilsen / Tropical)
PRODUCT_SPLIT = {"Imperial": 0.50, "Pilsen": 0.25, "Tropical": 0.25}

# Coordenadas aproximadas (lat, lon) de cada cabecera de cantón / CD
COORDS = {
    0: (9.8600, -83.9230),   # CD Cartago (depósito)
    1: (9.8644, -83.9194),   # Cartago
    2: (9.8377, -83.8669),   # Paraíso
    3: (9.9281, -84.0167),   # La Unión
    4: (9.8814, -83.7847),   # Jiménez
    5: (9.9028, -83.6747),   # Turrialba
    6: (9.9389, -83.7956),   # Alvarado
    7: (9.9067, -83.8833),   # Oreamuno
    8: (9.8208, -83.9461),   # El Guarco
}

CAPACITY = 24  # pallets por camión
