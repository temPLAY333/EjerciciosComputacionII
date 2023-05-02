import os, time, argparse

#Escriba un programa que abra un archvo de texto pasado por argumento utilizando el modificador -f.
#* El programa deberá generar tantos procesos hijos como líneas tenga el archivo de texto.
#* El programa deberá enviarle, vía pipes (os.pipe()), cada línea del archivo a un hijo.
#* Cada hijo deberá invertir el orden de las letras de la línea recibida, y se lo enviará al proceso padre nuevamente, también usando os.pipe().
#* El proceso padre deberá esperar a que terminen todos los hijos, y mostrará por pantalla las líneas invertidas que recibió por pipe.
#* Debe manejar los errores.

def revez(texto):
    r2,w2 = os.pipe()
    r,w = os.pipe()
    try:
        with open(texto)as t:
            n=t.readlines()
    except FileNotFoundError:
        return FileNotFoundError

    for num in range(len(n)):
        pip = os.fork()
        if pip == 0:
            os.close(r)
            os.close(w2)
            time.sleep(num*0.005)
            linea=os.read(r2,2048)
            os.close(r2)
            
            os.write(w,linea[::-1])
            os.close(w)
            exit()

    os.close(w)
    os.close(r2)
    text = []
    for num in range(len(n)):
        os.write(w2,n[num].encode())
        
        text.append(os.read(r, 2048).decode())
        if text[num][0] == "\n":
            text[num]= text[num][1::]
    os.close(r)
    return(text)

if __name__ == '__main__':
    pasrse = argparse.ArgumentParser(prog= "Vezre")
    pasrse.add_argument("-f", "--file")
    args = pasrse.parse_args()
    if args.file:
        try:
            text = revez(args.file)
            for linea in text:
                print(linea)
        except FileNotFoundError:
            print("Error: Archivo no encontrado")

