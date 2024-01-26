import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer, AsyncConsumer

class ConnectConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        print('?????')
        await self.accept()
    async def receive_json(self, content, **kwargs):
        message = content.get('message', '')
        print(f'Received message from client: {message}')
        await self.send_json({'message': 'Message received successfully!'})

class DisconnectConsumer(AsyncJsonWebsocketConsumer):
    async def disconnect(self, close_code):
        print('!!!!!!!!!!!')
        pass

class SendDataConsumer(AsyncJsonWebsocketConsumer):
    async def send_data_to_client(self):
        data = 'hi'
        await self.send_json({"data": data})


import json
from channels.generic.websocket import AsyncWebsocketConsumer

class MyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # 받은 메시지를 처리하거나 다른 동작을 수행
        print(f"Received message: {message}")

        # 클라이언트에게 응답을 보낼 수도 있음
        await self.send(text_data=json.dumps({
            'message': 'Message received successfully.'
        }))
