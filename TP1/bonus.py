from multiprocessing import Process
import time, argparse

#Escriba un programa que abra un archvo de texto pasado por argumento utilizando el modificador -f.
#* El programa deberá generar tantos procesos hijos como líneas tenga el archivo de texto.
#* El programa deberá enviarle, vía pipes (os.pipe()), cada línea del archivo a un hijo.
#* Cada hijo deberá invertir el orden de las letras de la línea recibida, y se lo enviará al proceso padre nuevamente, también usando os.pipe().
#* El proceso padre deberá esperar a que terminen todos los hijos, y mostrará por pantalla las líneas invertidas que recibió por pipe.
#* Debe manejar los errores.

def revez(linea):
    return linea[::-1]

if __name__ == "__main__":
    pasrse = argparse.ArgumentParser(prog= "Revez")
    pasrse.add_argument("-f", "--file")
    if pasrse.parse_args().file:
        with open(pasrse.parse_args().file) as t:
            txt = t.readlines()
        for linea in txt:
            p = Process(target=revez, args=linea)
        p.start
        for linea in txt:
            print(linea)