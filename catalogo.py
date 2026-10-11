import csv
import os
import tempfile
from decimal import Decimal

ARCHIVO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "productos.txt")
CABECERA = ["codigo", "descripcion", "cantidad", "precio"]

MENU = """
  1. Registrar    
  2. Buscar    
  3. Listar    
  4. Actualizar    
  0. Salir
"""


# ------------------------------------------------------------------ funciones

def validar(codigo, descripcion, cantidad, precio):
    codigo, descripcion = codigo.strip(), descripcion.strip()
    if not codigo or not descripcion:
        raise ValueError("codigo y descripcion son obligatorios.")

    try:
        cantidad, precio = int(str(cantidad).strip()), Decimal(str(precio).strip())
    except (ValueError, ArithmeticError):
        raise ValueError("cantidad o precio no son validos.")

    if cantidad < 0:
        raise ValueError(f"cantidad invalida: {cantidad}")
    if not precio.is_finite() or precio <= 0:
        raise ValueError(f"precio invalido: {precio}")
    if precio.as_tuple().exponent < -2:
        raise ValueError(f"el precio admite maximo 2 decimales: {precio}")

    return [codigo, descripcion, cantidad, precio]


def buscar(productos, codigo):
    codigo = codigo.strip()
    for i, producto in enumerate(productos):
        if producto[0] == codigo:
            return i
    return -1


def registrar(productos, codigo, descripcion, cantidad, precio):
    producto = validar(codigo, descripcion, cantidad, precio)
    if buscar(productos, producto[0]) != -1:
        raise ValueError(f"el codigo {producto[0]} ya esta registrado.")
    productos.append(producto)
    return producto


def actualizar(productos, codigo, cantidad, precio):
    indice = buscar(productos, codigo)
    if indice == -1:
        raise ValueError(f"no existe el codigo {codigo.strip()}")
    productos[indice] = validar(productos[indice][0], productos[indice][1],
                                cantidad, precio)
    return productos[indice]


def confirmar_cambio(productos, operacion, *datos):
    copia = list(productos)
    operacion(copia, *datos)
    guardar(copia)
    return copia


def cargar(ruta=ARCHIVO):
    if not os.path.exists(ruta):
        return []

    with open(ruta, encoding="utf-8-sig", newline="") as archivo:
        filas = list(csv.reader(archivo, delimiter=";"))

    if not filas or filas[0] != CABECERA:
        raise ValueError(f"cabecera invalida, se esperaba: {';'.join(CABECERA)}")

    productos = []
    for numero, fila in enumerate(filas[1:], start=2):
        if not any(campo.strip() for campo in fila):
            continue  # fila en blanco
        if len(fila) != len(CABECERA):
            raise ValueError(f"fila {numero} incompleta")

        try:
            producto = validar(*fila)
        except ValueError as error:
            raise ValueError(f"fila {numero}: {error}")

        if buscar(productos, producto[0]) != -1:
            raise ValueError(f"fila {numero}: codigo duplicado {producto[0]}")

        productos.append(producto)

    return productos


def guardar(productos, ruta=ARCHIVO):
    directorio = os.path.dirname(os.path.abspath(ruta))
    temporal = None
    try:
        with tempfile.NamedTemporaryFile(
            "w", encoding="utf-8", newline="", dir=directorio,
            prefix=".catalogo-", suffix=".tmp", delete=False,
        ) as archivo:
            temporal = archivo.name
            escritor = csv.writer(archivo, delimiter=";")
            escritor.writerow(CABECERA)
            for producto in productos:
                escritor.writerow([str(campo) for campo in producto])

        os.replace(temporal, ruta)
    except OSError as error:
        if temporal and os.path.exists(temporal):
            os.remove(temporal)
        raise ValueError(f"no se pudo guardar {ruta}: {error}")


def mostrar(productos):
    if not productos:
        print("El catalogo esta vacio.")
    for codigo, descripcion, cantidad, precio in productos:
        print(f"{codigo:<8} {descripcion:<28} {cantidad:>5} {precio:>8}")
    print(f"{len(productos)} producto(s).")



def main():
    try:
        productos = cargar()
    except ValueError as error:
        print(f"El catalogo no se pudo cargar: {error}")
        return

    print(f"Productos cargados: {len(productos)}")

    while True:
        print(MENU)
        opcion = input("Opcion: ").strip()

        if opcion == "0":
            break

        try:
            if opcion == "1":
                productos = confirmar_cambio(
                    productos, registrar, input("Codigo: "), input("Descripcion: "),
                    input("Cantidad: "), input("Precio: "))
                print("Registrado.")

            elif opcion == "2":
                indice = buscar(productos, input("Codigo: "))
                print(productos[indice] if indice != -1 else "No encontrado.")

            elif opcion == "3":
                mostrar(productos)

            elif opcion == "4":
                productos = confirmar_cambio(
                    productos, actualizar, input("Codigo: "),
                    input("Cantidad: "), input("Precio: "))
                print("Actualizado.")

            else:
                print("Opcion no valida.")

        except ValueError as error:
            print(f"Error: {error}")

    print("Hasta luego.")


if __name__ == "__main__":
    main()
