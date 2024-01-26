from django.shortcuts import render
from django.http import HttpResponse
import socket
import select

# Create your views here.
def socket_client(request):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('0.0.0.0', 20000)
    print('Start up on {} port {}'.format(*server_address))
    server_socket.bind(server_address)
    server_socket.listen()
    print('accept wait')
    # 새로운 클라이언트 연결을 수락
    client_socket, client_address = server_socket.accept()
    client_socket.setblocking(0)
    print(f"Accepted connection from {client_address}")

    try:
        while True:
            print('loading')
            ready = select.select([client_socket], [], [], 5)
            if ready[0]:
                data1 = client_socket.recv(4096)
            # data1 = client_socket.recv(1024)

            if not data1:
                break 
            data = data1.decode()
            print(f"Received data from client: {data}")


            response_data = "Server received: " + data
            client_socket.sendall(response_data.encode())

    except Exception as err:
        print(f"Error: {err}")

    finally:
        print('Closing connection')
        client_socket.close()

    return HttpResponse("Socket communication complete.")
    # server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # server_address = ('0.0.0.0', 20000)
    # print('Start up on {} port {}'.format(*server_address))
    # server_socket.bind(server_address)
    # server_socket.listen()
    # print('accept wait')
    # client_socket, client_address = server_socket.accept()
    # # print(client_socket)
    # # print(client_address)
    # while True:
    #     print('loading')
    #     # client_socket, client_address = server_socket.accept()
    #     try:

    #         data1 = client_socket.recv(8)

    #         if not data1:
    #             client_socket.close()
    #             break
    #         data = data1.decode()
    #         print(f"Received data from client: {data}")


    #     except Exception as err:
    #         print('error')
    #         client_socket.close()
    #         break


    # return HttpResponse("Socket communication complete.")



def close(request):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.close()
    return HttpResponse("Socket communication complete.")
