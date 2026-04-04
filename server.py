import socket
import threading

HOST = "localhost"
PORT = 8080

clients = []

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(10)

print(f"Server is running on {HOST}:{PORT}")


def broadcast(data, sender=None):
    for client in clients:
        if client != sender:
            try:
                client.send(data)
            except:
                pass


def handle_client(client_socket):

    while True:

        try:
            data = client_socket.recv(1024)

            if not data:
                break

            broadcast(data, client_socket)

        except:
            break

    if client_socket in clients:
        clients.remove(client_socket)

    client_socket.close()


while True:

    client_socket, addr = server_socket.accept()

    print(f"Connected {addr}")

    clients.append(client_socket)

    threading.Thread(target=handle_client, args=(client_socket,), daemon=True).start()