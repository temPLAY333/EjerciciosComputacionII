# 1- Cuándo y por qué se produce el error BrokenPipeError: [Errno 32] Broken pipe ?
# 2- Realizar dos versiones de un servidor de mayúsculas que atienda múltiples clientes de forma 
# concurrente utilizando multiprocessing y threading utilizando sockets TCP.
# El hilo/proceso hijo debe responder con mayúsculas hasta que el cliente envíe la palabra exit.
# En caso de exit el cliente debe administrar correctamente el cierre de la conexión y del proceso/hilo.

import socket, multiprocessing, signal, os

def childWork(msg, pid):
    while True:
        msg.send(b"Texto: ")
        try:
            data = msg.recv(4096).decode().replace("\n","").replace("\r","")
            if data == "Exit":
                msg.close
                break
            if data == "CloseServer":
                msg.close
                os.kill(pid, signal.SIGUSR1)
            msg.send(bytes(str(data.upper()+"\n"), "utf-8"))
        except Exception as error:
            msg.send(b"Ocurrio un error")
            msg.send(bytes(error, "utf-8"))

def start():
    list=[]
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)
    signal.signal(signal.SIGUSR1, closeServer(list))
    
    sock.listen(5)
    pid = os.getgid()
    while True:
        msg = sock.accept()
        msg.send(b"Ingrese un texto a mayusculear (Exit para terminar la conexion y CloseServer para cerrar el servidor")
        child = multiprocessing.Process(target=childWork, args=(msg, pid))
        list.append(child)
        child.start()

def closeServer(hijos: list, signum=None, frame=None):
    for child in hijos:
        child.terminate()
        child.join()
    sock.close()
    exit()

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("localhost", 5678))
    start()
