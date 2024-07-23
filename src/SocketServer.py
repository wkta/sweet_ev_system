from GameModel import GameModel
import socket
import threading

gl_state = GameModel()
clients = []


def handle_client(conn, addr):
    global gl_state
    with conn:
        print(f'Connected by {addr}')
        while True:
            data = conn.recv(1024)
            if not data:
                break
            gl_state = GameModel.deserialize(data.decode())
            print(f'Shared variable updated to {gl_state.serialize()}')
            broadcast_variable()


def broadcast_variable():
    global gl_state
    for client in clients:
        try:
            client.sendall(gl_state.serialize().encode())
        except:
            clients.remove(client)


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(2)
    print('Server listening on port 12345...')

    while len(clients) < 2:
        conn, addr = server_socket.accept()
        clients.append(conn)
        threading.Thread(target=handle_client, args=(conn, addr)).start()


if __name__ == '__main__':
    start_server()
