import socket
import threading
from queue import Queue
from websocket.settings import message_queue

client_sockets = []  


def handle_client(client_sock, client_addr, client_sockets):
    try:
        while True:
            data = client_sock.recv(1024)
            if data == 'exit':
                break
            print(f'Received from {client_addr}: {data.decode("utf-8")}')

    except Exception as e:
        print(f'Error handling client {client_addr}: {e}')

    finally:
        client_sockets.remove(client_sock)
        client_sock.close()
        print(f'Connection with {client_addr} closed.')


def start_server():
    server_host = 'localhost'
    server_port = 55555

    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((server_host, server_port))
    server_sock.listen(5)
    
    print(f'Server is listening on {server_host}:{server_port}')

    try:
        # 클라이언트 접속 대기를 위한 스레드 실행
        message_thread = threading.Thread(target=send_messages, args=(client_sockets, message_queue))
        message_thread.start()
        client_thread = threading.Thread(target=wait_for_clients, args=(server_sock, client_sockets))
        client_thread.start()

    except KeyboardInterrupt:
        print('Server is shutting down...')
        server_sock.close()


def send_messages(client_sockets, message_queue):
    while True:
        # 큐에 메시지가 있으면 가져와서 클라이언트에게 전송
        message = message_queue.get()
        print(message)
        print(message_queue)
        print(client_sockets)
        for client_socket in client_sockets:
            client_socket.sendall(message.encode('utf-8'))


def wait_for_clients(server_sock, client_sockets):
    # message_thread = threading.Thread(target=send_messages, args=(client_sockets, message_queue))
    # message_thread.start()
    while True:
        client_sock, client_addr = server_sock.accept()
        print(f'Accepted connection from {client_addr}')
        client_sockets.append(client_sock)
        print(client_sockets)
        new_client_thread = threading.Thread(target=handle_client, args=(client_sock, client_addr, client_sockets))
        new_client_thread.start()

# 서버 시작
if __name__ == "__main__":
    start_server()
