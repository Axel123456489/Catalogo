"""Mide el tiempo de respuesta de cada operacion del catalogo.

Ejecutar:  python generar_catalogo.py
           python medir_tiempo.py

No modifica productos.txt: la parte que escribe usa un archivo temporal.
"""

import os
import tempfile
import time

from catalogo import actualizar, buscar, cargar, guardar, registrar

REPETICIONES = 100


def medir(operacion, repeticiones=REPETICIONES):
    """Devuelve el tiempo promedio de una operacion, en milisegundos."""
    inicio = time.perf_counter()
    for _ in range(repeticiones):
        operacion()
    return (time.perf_counter() - inicio) * 1000 / repeticiones


def main():
    productos = cargar()
    if not productos:
        print("El catalogo esta vacio. Ejecute generar_catalogo.py primero.")
        return

    total = len(productos)
    print(f"\nCatalogo con {total} productos, "
          f"{REPETICIONES} repeticiones por operacion\n")
    print(f"{'Operacion':<42}{'ms':>12}")
    print("-" * 54)

    def fila(nombre, operacion, repeticiones=REPETICIONES):
        print(f"{nombre:<42}{medir(operacion, repeticiones):>12.4f}")

    # --- cargar: lee el archivo completo desde el disco
    fila("Cargar el archivo completo", cargar, 1)

    # --- buscar: recorrido lineal. El codigo inexistente es el peor caso
    #     porque obliga a revisar los 1200 registros sin salir nunca.
    fila("Buscar el primer codigo (mejor caso)",
         lambda: buscar(productos, productos[0][0]))
    fila("Buscar el ultimo codigo",
         lambda: buscar(productos, productos[-1][0]))
    fila("Buscar un codigo inexistente (peor caso)",
         lambda: buscar(productos, "999999"))

    # --- el mismo conjunto de datos, pero con un indice. Sirve para
    #     apoyar la seccion 5.1 del informe.
    indice = {producto[0]: i for i, producto in enumerate(productos)}
    fila("Buscar el ultimo codigo con indice (diccionario)",
         lambda: indice.get(productos[-1][0], -1))

    # --- registrar y actualizar: en memoria, sin tocar el disco
    def registrar_y_quitar():
        registrar(productos, "999999", "Producto de prueba", 10, "1.00")
        productos.pop()  # se retira para que la repeticion no sea duplicado

    fila("Registrar un producto nuevo", registrar_y_quitar)
    fila("Actualizar el ultimo producto",
         lambda: actualizar(productos, productos[-1][0], 10, "1.00"))

    # --- guardar y recargar: escribe un archivo temporal y lo relee
    def guardar_y_recargar():
        guardar(productos, ruta)
        return cargar(ruta)

    with tempfile.TemporaryDirectory() as carpeta:
        ruta = os.path.join(carpeta, "productos.txt")
        fila("Guardar y recargar los 1200", guardar_y_recargar, 10)

    print("-" * 54)
    print("Menos es mejor. La busqueda lineal crece con el catalogo; "
          "el indice no.\n")


if __name__ == "__main__":
    main()
