import os, time

# Escribir un programa que realice la multiplicación de dos matrices de 2x2. 
# Cada elemento deberá calcularse en un proceso distinto devolviendo el resultado en una fifo 
# indicando el indice del elemento. El padre deberá leer en la fifo y mostrar el resultado final.



A = [[1,0],[0,1]]
B = [[1,2],[3,4]]
rta = [[0,0],[0,0]]

def multi():
    os.mkfifo("pila")
    for i in range(2):
        for j in range(2):
            pip= os.fork()
            if pip == 0:
                for k in range(2):
                    pip += A[i][k]*B[k][j]
                with open("pila", "w") as p:
                    p.write(str(pip))
                exit()
            
            with open("pila") as p:
                rta[i][j] = int(p.read())

    os.unlink("pila")
    print(rta)

try:
    multi()
except FileExistsError as E:
    os.unlink("pila")
    print(E)





