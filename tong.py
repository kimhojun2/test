import socket
import threading
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
    

    # client_sockets = []  # 클라이언트 소켓을 저장할 리스트

    try:
        # 사용자 입력 처리를 하는 쓰레드
        input_thread = threading.Thread(target=handle_user_input, args=(client_sockets, ))
        input_thread.start()
        while True:
            client_sock, client_addr = server_sock.accept()
            print(f'Accepted connection from {client_addr}')

            client_sockets.append(client_sock)  # 새로 연결된 클라이언트 소켓을 리스트에 추가


            client_thread = threading.Thread(target=handle_client, args=(client_sock, client_addr, client_sockets))
            client_thread.start()



    except KeyboardInterrupt:
        print('Server is shutting down...')
        server_sock.close()

def handle_user_input(client_sockets):
    print(client_sockets)
    while True:
        print(client_sockets)
        message = input(f'Server >>> ')
        if message.lower() == 'exit':
            break
        target_client_index = int(message[0])
        if 0 <= target_client_index < len(client_sockets):
            target_client_socket = client_sockets[target_client_index]
            target_client_socket.sendall(message[1:].encode('utf-8'))
        else:
            print(f'Invalid client index: {target_client_index}')


start_server()