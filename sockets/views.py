from django.shortcuts import render
from django.http import HttpResponse
import socket
import select
from .models import location
import json
from websocket.settings import message_queue

client_socket = None
a = 1

# 소켓 연결
def send_message(message):
    server_host = '70.12.246.136'  # 서버 IP 주소
    server_port = 55555  # 서버 포트

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_host, server_port))

    # 메시지 전송
    client_socket.sendall(message.encode('utf-8'))

    # 연결 종료
    client_socket.close()


from django.http import JsonResponse

def aaa(request):
    message_queue.put('과연')
    # print(message_queue)
    print(111)
    return HttpResponse('hi')


    # 이하 생략...
