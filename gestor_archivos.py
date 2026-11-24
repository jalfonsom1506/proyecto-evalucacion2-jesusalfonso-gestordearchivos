"""
PROYECTO 2: GESTOR DE ARCHIVOS EN CONSOLA
Módulo: MPO
Alumno: Jesús Alfonso Muñoz
"""

import os
from datetime import datetime

def mostrar_menu():
    """Muestra el encabezado, la ruta del directorio actual y las opciones del menú"""

    print("""
****************************************
*********  GESTOR DE ARCHIVOS  *********
****************************************
""")
    print("RUTA: ", os.getcwd())
    print("""
1. Listar contenido del directorio actual
2. Crear un nuevo directorio
3. Crear un archivo de texto
4. Escribir texto en un archivo existente
5. Eliminar un archivo o directorio
6. Mostrar información de un archivo
7. Salir
""")

def listar_contenido(elemento):
    """Lista los elementos del sistema de archivos indicando si es una CARPETA o un ARCHIVO"""

    if os.path.isdir(elemento):
        return True

    elif os.path.isfile(elemento):
        return False

def crear_directorio(nombre):
    """Crea una carpeta gestionando si ya existe anteriormente"""
    try:
        os.mkdir(nombre)
        return True

    except FileExistsError:
        return False

def crear_archivo(nombre, contenido):
    """Crea un archivo con contenido adicional opcional sin sobreescribir existentes"""

    try:
        with open (nombre, "x", encoding = "utf-8") as archivo:

            if contenido:
                archivo.write(contenido + "\n")
        return True

    except FileExistsError:
        return False

def escribir_en_archivo(nombre, frase):
    """Añade una línea de texto al final de un archivo existente"""

    try:
        with open (nombre, "a", encoding="utf-8") as archivo:
            archivo.write(frase + "\n")
        return True

    except FileNotFoundError:
        return False

def eliminar_elemento(tipo, nombre):
    """Elimina una carpeta vacía o archivo del equipo. Se gestionan excepciones"""

    try:
        if tipo == "1":

            os.rmdir(nombre)
            return "carpeta"

        elif tipo == "2":

            os.remove(nombre)
            return "archivo"

        else:
            return "numero"

    except FileNotFoundError:
        return "noExiste"

    except PermissionError:
        return "sinPermiso"

    except OSError:
        return "noVacía"

def mostrar_informacion(nombre):
    """Obtiene el tipo, tamaño en bytes y fecha formateada de la última modificación"""

    if not os.path.exists(nombre):
        return None

    try:
        tipo = "CARPETA" if os.path.isdir(nombre) else "ARCHIVO"
        tamanio = os.path.getsize(nombre)
        segundos = os.path.getmtime(nombre)
        legible = datetime.fromtimestamp(segundos)
        fecha = legible.strftime("%d/%m/%Y %H:%M:%S")

        return tipo, tamanio, fecha

    except Exception:
        return None

def main():
    """Bucle principal de ejecución del Gestor de Archivos"""

    while True:
        mostrar_menu()
        opcion = input("\nPor favor, elije una opción: ")

        match opcion:

            case "1":
                print("\n--- CONTENIDO DEL DIRECTORIO ACTUAL ---")
                elementos = os.listdir()
                if not elementos:
                    print("El directorio actual está vacío")

                else:
                    for elemento in elementos:
                        if listar_contenido(elemento):
                            print(elemento, " es una CARPETA")
                        else:
                            print(elemento, " es un ARCHIVO")

            case "2":
                nombre = input("\nPor favor, introduce el nombre de la carpeta: ")
                if crear_directorio(nombre):
                    print("\nCarpeta creada con éxito")
                else:
                    print("\nYa existe una carpeta con ese nombre.")

            case "3":
                nombre = input("Indica el nombre del archivo: ")
                texto = input("¿Quieres añadir contenido al archivo (S/N): ").upper()
                contenido= ""

                if texto == "S":
                    contenido = input("Escribe el contenido que quieres añadir: ")

                if crear_archivo(nombre, contenido):

                    if contenido:
                        print("Se ha creado el archivo con el contenido indicado")
                    else:
                        print("Se ha creado el archivo sin contenido")

                else:
                    print("Ya existe un archivo con el nombre indicado")

            case "4":
                nombre = input("\nIndica el nombre del archivo en el que vas a añadir contenido: ")
                if os.path.isfile(nombre):
                    frase = input("\nEscribe el contenido que quieres añadir. Al terminar, pulsa ENTER: ")
                    escribir_en_archivo(nombre, frase)
                    print("\nTu contenido se ha añadido correctamente al archivo")
                else:
                    print("\nEl nombre de archivo que has indicado no existe")

            case "5":
                tipo = input("\nPulse '1' si quiere eliminar una carpeta, y '2' si se trata de un fichero: ")
                nombre = input ("\nAhora indique el nombre del elemento que desea eliminar: ")
                resultado = eliminar_elemento(tipo, nombre)
                if resultado == "carpeta":
                    print("La carpeta ", nombre, " ha sido eliminada")
                elif resultado == "archivo":
                    print("El archivo ", nombre, " ha sido eliminado")
                elif resultado == "numero":
                    print("\nSelección incorrecta")
                elif resultado == "noExiste":
                    print("\nNo existe ningún elemento con el nombre indicado")
                elif resultado == "sinPermiso":
                    print("No tienes los permisos necesarios para ejecutar la acción")
                else:
                    print("La carpeta no está vacía. Operación no permitida")

            case "6":
                nombre = input("\nEscribe el nombre del elemento que quieres consultar: ")
                info = mostrar_informacion(nombre)

                if info is not None:
                    print("Información de [", nombre, "]")
                    print("Tipo de elemento: ", info[0])
                    print("Tamaño: ", info[1], " bytes")
                    print("Última modificación: ", info[2])

                else:
                    print("No existe ningún elemento con el nombre especificado")

            case "7": print("\nSaliendo...... ¡Hasta pronto!"); break

            case _: print("Opción no válida. Por favor, elige un número del 1 al 7")

if __name__ == "__main__":
    main()