"""Genera un catalogo de 1200 productos de prueba y lo guarda en productos.txt.

Ejecutar:  python generar_catalogo.py
           python generar_catalogo.py --forzar   (reemplaza el archivo existente)

La semilla es fija para que el catalogo salga siempre igual y las mediciones
de tiempo sean comparables entre ejecuciones.
"""

import os
import random
import sys
from decimal import Decimal

from catalogo import ARCHIVO, guardar, validar

CANTIDAD = 1200
SEMILLA = 7

NOMBRES = [
    "Arroz extra", "Azucar rubia", "Aceite vegetal", "Leche entera",
    "Pan blanco", "Fideo talludin", "Aceite de oliva", "Atun en aceite",
    "Cafe molido", "Te negro", "Mantequilla", "Queso fresco",
    "Yogurt fresa", "Leche evaporada", "Papa amarilla", "Cebolla roja",
    "Tomate", "Zanahoria", "Manzana", "Platano", "Naranja",
    "Pollo entero", "Carne molida", "Huevos", "Sardinas", "Atun en lata",
    "Harina", "Azucar glass", "Bicarbonato", "Maicena", "Milo verde",
]
PRESENTACIONES = ["1 kg", "500 g", "250 g", "1 L", "900 ml", "12 unidades"]


def generar(cantidad, semilla=SEMILLA):
    """Arma la lista de productos con valores aleatorios pero reproducibles."""
    azar = random.Random(semilla)
    productos = []
    for i in range(1, cantidad + 1):
        descripcion = f"{azar.choice(NOMBRES)} {azar.choice(PRESENTACIONES)}"
        # Cantidad entre 0 y 200 unidades; el 0 es valido segun las reglas.
        cantidad_unidades = azar.randint(0, 200)
        # Precio entre 1.00 y 500.00, con 2 decimales.
        precio = Decimal(azar.randint(100, 50000)) / Decimal(100)
        productos.append(validar(f"{i:06d}", descripcion,
                                 cantidad_unidades, precio))
    return productos


def main():
    if os.path.exists(ARCHIVO) and "--forzar" not in sys.argv:
        print(f"{os.path.basename(ARCHIVO)} ya existe y no se va a tocar.")
        print("Use --forzar si quiere reemplazarlo por el de 1200 productos.")
        return

    productos = generar(CANTIDAD)
    guardar(productos)

    total = sum(p[2] for p in productos)
    print(f"{CANTIDAD} productos guardados en {os.path.basename(ARCHIVO)}.")
    print(f"Unidades totales: {total}")


if __name__ == "__main__":
    main()
