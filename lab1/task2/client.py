import socket
import threading

def receive():
    while True:
        try:
            recived = client.recv(1024).decode(format)
            if recived == 'start':
                login = input('Логін: ').strip()
                client.send(login.encode(format))
            recived = client.recv(1024).decode(format)
            if recived == 'log in':
                password = input('Пароль: ').strip()
                client.send(password.encode(format))
            elif recived == 'registration':
                password = registration()
                client.send(password.encode(format))
                chat_thread = threading.Thread(target=chat, args=(login,))
                chat_thread.start()
            else:
                print(recived)
        except: 
            print("An error occured!")
            client.close()
            break

def chat(login):
    while True:
        message = input()
        if message != "":
            client.send(f'{login}: "{message}"'.encode(format))

def registration():
    print("Вам потрібно зареєструватися")
    while True:
        password = input('Пароль: ')
        password_confirmed = input('Підтвердіть пароль: ')
        if password_confirmed == password:
            break
        print("Невірне введення паролю, спробуйте ще раз")
    return password

host = '127.0.0.1'
port = 11111
format = 'utf-8'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))
receive_handler = threading.Thread(target=receive)
receive_handler.start()
