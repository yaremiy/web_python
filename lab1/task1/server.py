import threading
from datetime import datetime
import time
import socket
from sys import getsizeof

def handle(client):
    while True:
        try:
            message = client.recv(1024).decode(format)
            if message == "Вийти":
                client.close()
                break
            print(f'{datetime.now().strftime("%H:%M:%S")} {message}')
            time.sleep(5)
            size = client.send(message.encode(format))
            if size != len(message.encode(format)):
                print("Проблема при надсиланні даних")
        except:
            print("Розірвано з'єднання з користувачем")
            break

def receive():
    while True:
        client, adress = server.accept()
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


host = "127.0.0.1"
port = 11111
format = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

print("Сервер запущено")
receive()