import argparse, http.server, socketserver, socket, cgi, sys, os
from multiprocessing import Process, Queue
from PIL import Image, ImageOps
from http import HTTPStatus

image_queue = Queue()


def image_processing_worker(queue):
    while True:
        image_path, output_path, image_name, scale_factor = queue.get()
        
        # Procesar la imagen (escala de grises)
        process_image(image_path, output_path)
        print("Imagen Procesada")

        # Si es necesario redimensionar
        if scale_factor is not None:
            # Enviar tarea al servidor de redimensionamiento
            resized_image_data = send_to_resize_server(output_path, scale_factor)
            
            output_path = os.path.join("output", "resized_" + image_name)

            # Guardar la imagen redimensionada
            with open(output_path, "wb") as resized_image_file:
                resized_image_file.write(resized_image_data)


def process_image(image_path, output_path):
    # Cargar la imagen
    print("Procesando imagen...")
    original_image = Image.open(image_path)

    # Convertir a escala de grises
    grayscale_image = ImageOps.grayscale(original_image)

    # Guardar la imagen en escala de grises
    grayscale_image.save(output_path)


def send_to_resize_server(image_path, scale_factor):

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as resize_client:
            resize_client.connect(("127.0.0.1", 5000))  # Cambiar si es necesario

            # Convertir el factor de escala a cadena de bytes
            scale_factor_bytes = str(scale_factor).encode("utf-8")

            # Enviar la longitud del factor de escala y luego el factor de escala
            resize_client.sendall(len(scale_factor_bytes).to_bytes(4, byteorder='big'))
            resize_client.sendall(scale_factor_bytes)

            # Enviar los datos de la imagen
            with open(image_path, "rb") as image_file:
                image_data = image_file.read()
            resize_client.sendall(image_data)

            # Enviar un indicador de finalización
            resize_client.shutdown(socket.SHUT_WR)

            # Recibir los datos de la imagen redimensionada
            resized_image_data = b""
            while True:
                data = resize_client.recv(1024)
                if not data:
                    break
                resized_image_data += data

        return resized_image_data
    
    except ConnectionRefusedError:
        print("Error: La conexión con el servidor de redimensionamiento fue rechazada.")

    except OSError as e:
        print(f"Error de sistema al conectar con el servidor de redimensionamiento: {e}")


class ImageProcessingHandler(http.server.CGIHTTPRequestHandler):
    def do_POST(self):
        try: 
            form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD':'POST'})
            
            # Obtener la imagen y otros datos directamente del formulario
            image_file = form['file']
            image_name =image_file.filename
            resize_option = form.getvalue('resize', '')
            scale_factor = form.getvalue('scale_factor', '')

            # Guardar la imagen en el servidor
            uploaded_filename = os.path.join("uploads", image_name)
            with open(uploaded_filename, 'wb') as f:
                f.write(image_file.file.read())

            if os.path.exists(uploaded_filename):
                print(f"El archivo {image_name} existe en el directorio.")
            else:
                print(f"El archivo {image_name} no existe en el directorio.")

            # Agregar tarea a la cola de procesamiento
            output_filename = os.path.join("output", "gray_" + image_name)
            image_queue.put((uploaded_filename, output_filename, image_name, scale_factor if resize_option == 'on' else None))

            # Responder al cliente con la imagen procesada
            self.send_response(200)
            self.send_header('Content-type', 'application/octet-stream')
            self.send_header('Content-Disposition', f'attachment; filename="{os.path.basename(output_filename)}"')
            self.end_headers()

        except IOError as e:
            print(f"Error de E/S en el manejo del POST: {e}")
            # Enviar una respuesta HTTP con un código de error (por ejemplo, 500 Internal Server Error)
            self.send_error(HTTPStatus.INTERNAL_SERVER_ERROR)

        except OSError as e:
            print(f"Error de sistema en el manejo del POST: {e}")
            # Enviar una respuesta HTTP con un código de error (por ejemplo, 500 Internal Server Error)
            self.send_error(HTTPStatus.INTERNAL_SERVER_ERROR)

        except http.server.CGIHTTPRequestHandler.CGIError as e:
            print(f"Error CGI en el manejo del POST: {e}")
            # Enviar una respuesta HTTP con un código de error (por ejemplo, 500 Internal Server Error)
            self.send_error(HTTPStatus.INTERNAL_SERVER_ERROR)

def main(ip, port):
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("output", exist_ok=True)

    # Iniciar el worker para procesamiento de imágenes
    image_worker = Process(target=image_processing_worker, args=(image_queue,))
    image_worker.start()

    try:
        # Iniciar el servidor HTTP personalizado
        handler = ImageProcessingHandler
        with socketserver.TCPServer((ip, port), handler) as httpd:
            print(f"Serving on {ip}:{port}")
            httpd.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            httpd.serve_forever()
    
    except KeyboardInterrupt:
        print("Interrupción del teclado.")
        
        image_worker.terminate()
        image_worker.join()

        print("Servidor hijo cerrado. Saliendo...")
        # Finalizar el programa después de cerrar el servidor hijo
        sys.exit(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TP2 - procesa imágenes")
    parser.add_argument("-i", "--ip", default="127.0.0.1", type=str, help="Dirección de escucha", required=True)
    parser.add_argument("-p", "--port", default="7500", type=int, help="Puerto de escucha", required=True)
    args = parser.parse_args()

    main(args.ip, args.port)
