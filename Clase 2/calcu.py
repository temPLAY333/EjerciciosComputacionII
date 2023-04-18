import os, argparse, numpy as np

# Realizar un programa que implemente fork junto con el parseo de argumentos. 
# Deberá realizar relizar un fork si -f aparece entre las opciones al ejecutar el programa. 
# El proceso padre deberá calcular la raiz cuadrada positiva de un numero y el hijo la raiz negativa.


pasrse = argparse.ArgumentParser(prog= "DobleRaiz")
pasrse.add_argument("n", type= int)
pasrse.add_argument("-f", "--fork", action= "store_true")
args = pasrse.parse_args()

if args.fork:
    fork = os.fork()
    if fork == 0:
        print(round((-np.sqrt(args.n)), 4))
    else:
        print("",round(np.sqrt(args.n), 4))
else:
    print("",round(np.sqrt(args.n), 4))
