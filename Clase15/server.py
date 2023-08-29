# 1- Cuándo y por qué se produce el error BrokenPipeError: [Errno 32] Broken pipe ?
# 2- Realizar dos versiones de un servidor de mayúsculas que atienda múltiples clientes de forma 
# concurrente utilizando multiprocessing y threading utilizando sockets TCP.
# El hilo/proceso hijo debe responder con mayúsculas hasta que el cliente envíe la palabra exit.
# En caso de exit el cliente debe administrar correctamente el cierre de la conexión y del proceso/hilo.

import socket, multiprocessing, signal, os

def childWork(msg: socket, pid: int):
    while True:
        msg.send(b"Texto: ")

        data = msg.recv(4096).decode().replace("\n","").replace("\r","")
        if data == "Exit":
            msg.close()
            break
        elif data == "CloseServer":
            msg.close()
            os.kill(pid, signal.SIGUSR1)
            break
        msg.send(bytes(str(data.upper()+"\n"), "utf-8"))

def start():
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)
    signal.signal(signal.SIGUSR1, closeServer)
    
    sock.listen(5)
    pid = os.getgid()
    while True:
        msg, adrres = sock.accept()
        msg.send(b"Ingrese un texto a mayusculear (Exit para terminar la conexion)"+"\n")
        child = multiprocessing.Process(target=childWork, args=(msg, pid))
        list.append(child)
        child.start()

def closeServer(signum=None, frame=None):
    for child in list:
        child.terminate()
        child.join()
    sock.close()
    exit()

if __name__ == "__main__":
    list= []
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("localhost", 5678))
    start()
