from django.shortcuts import render
from django.http import HttpResponse
import socket
import select
from .models import location
import json


client_socket = None

# 소켓 연결
def initialize_socket(request):
    global client_socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('0.0.0.0', 20000)
    print('Start up on {} port {}'.format(*server_address))
    server_socket.bind(server_address)
    server_socket.listen()
    print('waiting.......')
    # 새로운 클라이언트 연결을 수락
    client_socket, client_address = server_socket.accept()
    print(client_socket, client_address)
    # client_socket.setblocking(0)

    try:
        while True:
            data = client_socket.recv(4096)
            if not data:
                break
            decoded_data = data.decode()
            json_data = json.loads(decoded_data)
            if json_data.get("num_of_frames") == 1:
                print('1단계 성공######')
                location_instance = location(loca_file=json_data)
                print('2단계성공############')
                location_instance.save()
                print('완전성공##############')                
            #print(f"Received data from client: {data.decode()}")

    except Exception as e:
        print('연결끊김')

    finally:
        print('Closing connection')
        client_socket.close()
    
    return HttpResponse('통신중!')
    
    
# 소켓 수신
def socket_client(request):
    global client_socket
    if client_socket is None:
        initialize_socket(request)

    try:
        while True:
            print('loading')
            ready = select.select([client_socket], [], [], 5)
            if ready[0]:
                data1 = client_socket.recv(4096)

                if not data1:
                    break

                data = data1.decode()
                print(f"Received data from client: {data}")

                # 프론트에서 '전송' 버튼을 누르면 라즈베리 파이로 메시지 전송
                if data == "aaa":
                    message = data
                    send_message_to_raspberry(message)
                    print("Message sent to Raspberry Pi")

                    # 여기서 필요에 따라 클라이언트에 응답을 보낼 수 있음
                    client_socket.sendall("서버에서 클라이언트로 전송하는 메시지".encode())

    except Exception as err:
        print(f"Error: {err}")

    # finally:
    #     print('Closing connection')
    #     client_socket.close()
    #     client_socket = None  # 연결 종료 후 클라이언트 소켓 초기화

    return HttpResponse("Socket communication complete.")


def send_message_to_raspberry(request, message):
    global client_socket
    if client_socket:
        client_socket.sendall(message.encode())
        print(client_socket)
    return HttpResponse('발송완료')


# Create your views here.
# def socket_client(request):
#     server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server_address = ('0.0.0.0', 20000)
#     print('Start up on {} port {}'.format(*server_address))
#     server_socket.bind(server_address)
#     server_socket.listen()
#     print('accept wait')
#     # 새로운 클라이언트 연결을 수락
#     client_socket, client_address = server_socket.accept()
#     client_socket.setblocking(0)
#     print(f"Accepted connection from {client_address}")

#     try:
#         while True:
#             print('loading')
#             ready = select.select([client_socket], [], [], 5)
#             if ready[0]:
#                 data1 = client_socket.recv(4096)
#             # data1 = client_socket.recv(1024)

#             if not data1:
#                 break 
#             data = data1.decode()
#             print(f"Received data from client: {data}")


#             response_data = "Server received: " + data
#             client_socket.sendall(response_data.encode())

#     except Exception as err:
#         print(f"Error: {err}")

#     finally:
#         print('Closing connection')
#         client_socket.close()

#     return HttpResponse("Socket communication complete.")


def close(request):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.close()
    return HttpResponse("Socket communication complete.")
