import socket
from PIL import Image
from io import BytesIO

def resize_image(image_data, scale_factor):
    print("Trabajando")

    image = Image.open(BytesIO(image_data))
    width, height = image.size
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)
    resized_image = image.resize((new_width, new_height))
    output_buffer = BytesIO()
    resized_image.save(output_buffer, format="JPEG")
    return output_buffer.getvalue()

def start_resize_server(ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((ip, port))
        server_socket.listen()

        print(f"Listening for resize requests on {ip}:{port}")

        while True:
            conn, addr = server_socket.accept()
            with conn:
                print(f"Accepted connection from {addr}")

                scale_factor_length_data = conn.recv(4)
                scale_factor_length = int.from_bytes(scale_factor_length_data, byteorder='big')

                scale_factor_data = conn.recv(scale_factor_length)
                scale_factor = float(scale_factor_data.decode("utf-8"))

                image_data = b""
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    image_data += data

                resized_image_data = resize_image(image_data, scale_factor)
                print("Listo")

                conn.sendall(resized_image_data)

if __name__ == "__main__":
    start_resize_server("127.0.0.1", 5000)  # Cambiar si es necesario

