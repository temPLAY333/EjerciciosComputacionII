import os, time

# Escribir un programa que realice la multiplicación de dos matrices de 2x2. 
# Cada elemento deberá calcularse en un proceso distinto devolviendo el resultado en una fifo 
# indicando el indice del elemento. El padre deberá leer en la fifo y mostrar el resultado final.

pdf = os.mkfifo("pila")

A = [[1,0],[0,1]]
B = [[1,2],[3,4]]
rta = 0

for n in range(1,5):
    pip = os.fork()
    if pip == 0:
        for k in range(2):
            if n == 1:
                rta += A[0][k]*B[k][0]
            elif n == 2:
                rta += A[0][k]*B[k][1]
            elif n == 3:
                rta += A[1][k]*B[k][0]
            elif n == 4:
                rta += A[1][k]*B[k][1]
        time.sleep(0.002*n)
        with open("pila", "w") as p:
            p.write(str(rta))
        exit()

for i in range(2):
    for j in range(2):
        with open("pila", "r") as p: 
            A[i][j] = int(p.read())
print(A)
os.unlink("pila")

