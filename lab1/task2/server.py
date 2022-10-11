import socket
import threading
from collections import deque

def send_all(message, current_client=None):
    with open('messages.txt', 'a+') as file:
        file.write(message + '\n')
    for client in clients:
        if client != current_client:
            client.send(message.encode(format))

def client_handler(client, login):
    while True:
        try:
            message = client.recv(1024).decode(format)
            send_all(message, client) 
        except:
            if client in clients:
                clients.remove(client)
                send_all(f"[{login}] Покинув чат!")
                print(f"{login} покинув чат")
            break

def log_in(client):
    while True:
        try:
            if client not in clients:
                client.send('start'.encode(format))
                login = client.recv(1024).decode(format)
                if login not in users:
                    client.send('registration'.encode(format))
                    password = client.recv(1024).decode(format)
                    users[login] = password
                    with open('users.txt', 'a') as file:
                        file.write(f"{login} {password}\n")
                else:
                    client.send('log in'.encode(format))
                    password = client.recv(1024).decode(format)
                    if users[login] != password:
                        client.send('Невірний пароль'.encode(format))
                        continue
                start_chat(client, login)
        except:
            continue

def start_chat(client, login):
    with open("messages.txt") as file:
        last_messages =  ''.join(deque(file, maxlen = 5))
    client.send(last_messages.encode(format))
    client.send('Ви в чаті'.encode(format))
    clients.append(client)
    print(f"Користувач {login} при'єднався")
    send_all(f"[{login}] при'єднується до чату!", client)
    client_thread = threading.Thread(target=client_handler, args=(client, login,))
    client_thread.start()

def read_users():
    open('users.txt', 'a+')
    open('messages.txt', 'a+')
    with open('users.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            user = line.split()
            users[user[0]] = user[1]

host = '127.0.0.1'
port = 11111
format = 'utf-8'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen()
print("Сервер запущено")
clients = []
users = {}
read_users()
while True:
    client, address = s.accept()
    print(f"З'єднано з {address}")
    receive_handler = threading.Thread(target=log_in, args=(client,))
    receive_handler.start()



