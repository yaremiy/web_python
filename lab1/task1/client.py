import socket
import threading

def recieve():
    while True:
        try:
            message = input("Введіть повідомлення: ")
            client.send(message.encode(format))
            message = client.recv(1024).decode(format)
            print(message)
        except: 
            print("Вас відключено")
            client.close()
            break


host = "127.0.0.1"
port = 11111
format = 'utf-8'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

receive_thread = threading.Thread(target=recieve)
receive_thread.start()

print('Щоб завершити напишіть "Вийти"')
