import os, time

# Escribir un programa en Python que comunique dos procesos. 
# El proceso padre deberá leer un archivo de texto y enviar cada línea del archivo al proceso hijo a través de un pipe. 
# El proceso hijo deberá recibir las líneas del archivo y, por cada una de ellas, 
# contar la cantidad de palabras que contiene y mostrar ese número.

r, w = os.pipe()
pid = os.fork()

if pid == 0:
    os.close(w)
    while 1:
        linea = os.read(r, 4048).split()
        print(len(linea))
        if len(linea) == 0:
            break
    os.close(r)
    exit()

os.close(r)
with open('texto.txt') as t:   
    for row in t:
        time.sleep(0.1)
        os.write(w, row.encode())

os.close(w)