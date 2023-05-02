import argparse

# Escribir un programa en Python que acepte un número de argumento entero positivo n y
# genere una lista de los n primeros números impares. 
# El programa debe imprimir la lista resultante en la salida estandar.

def evens(number):
    print( [even for even in range(1,number*2,2)] )

# Escribir un programa en Python que acepte dos argumentos de línea de comando: una cadena de texto, un número entero.
# El programa debe imprimir una repetición de la cadena de texto tantas veces como el número entero.

def repet(text, number):
    print((text+"\n")*number)

#3- Escribir un programa en Python que acepte argumentos de línea de comando para leer un archivo de texto. 
# El programa debe contar el número de palabras y líneas del archivo e imprimirlas en la salida estándar. 
# Además el programa debe aceptar una opción para imprimir la longitud promedio de las palabras del archivo. 
# Esta última opción no debe ser obligatoria. Si hubiese errores deben guardarse el un archivo cuyo nombre 
# será "errors.log" usando la redirección de la salida de error.

def reader(file, media=0):
    suma=0
    try:
        with open(file, "r" ) as file:
            f= file.read()
            print("Palabras:", len(f.split())) 
            print("  Lineas:", len(f.splitlines()))
        if media == 1:
            for word in f.split():
                suma += len(word)
            print("Promedio:", (suma / len(f.split()) ))
    except Exception as e:
        with open("errors.log", "a") as f:
            f.write(f"Error: {type(e).__name__} \n")
            f.write(f"{str(e)} \n")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog= "Ejercicios Computacion")
    parser.add_argument("-c", "--cadena")
    parser.add_argument("-r", "--repetir", type=int)
    parser.add_argument("-t", "--texto")
    parser.add_argument("-p","--promedio", action="store_true")

    arg = parser.parse_args()
    if arg.cadena and arg.repetir:
        repet(arg.cadena, arg.repetir)
    if arg.texto:
        if arg.promedio:
            reader(arg.texto, arg.promedio)
        else:
            reader(arg.texto)

