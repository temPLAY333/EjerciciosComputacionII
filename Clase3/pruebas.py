import os, time

# Verificar si es posible que dos procesos hijos (o nieto) lean el PIPE del padre. ==> SI
# Verificar si el PIPE sigue existiendo cuendo el padre muere (termina el proceso), ==> SI
# cuando el hijo muere [o cuendo mueren ambos] ==> SI

r, w = os.pipe()
pip= os.fork()
if pip==0:
    os.close(w)
    pip2=os.fork()
    if pip2==0:
        time.sleep(2)
        print(os.read(r,2048))

    exit()

os.close(r)
os.write(w, "Chau".encode())
print("Hola")
exit()
