import socket
import pickle
from random import randint

def combinaton(message, key):
    # шифрование сообщения
    P2 = []
    for i in range(len(message)):
        P2 += chr(ord(message[i]) ^ key)
    return ''.join(P2)

def send_message(sock, message, key):
    # отправляет сообщение через сокет
    message = combinaton(message, key)

    # возвращает его сериализованное представление в виде байтовой строки
    # отправляет зашифрованное сообщение через сокет, используя модуль 'pickle для сериализации сообщения в байтовую строку
    sock.send(pickle.dumps(message))

def receive(sock, key):
    message = pickle.loads(sock.recv(1024))#получение
    message = combinaton(message,key) #отправляет сообщение через сокет
    return message

HOST = '127.0.0.1'
PORT = 8080

sock = socket.socket()
sock.bind((HOST, PORT))
sock.listen(1)

#блокирует выполнение программы, пока не будет установлено новое соединение с клиентом, и возвращает новый сокет
conn, addr = sock.accept()

message = conn.recv(1024) #подключение

p, g, A = pickle.loads(message) #получает и десериализует значение B, отправленное сервером через сокет, используя модуль pickle
b = randint(0, 10000)
B = g ** b % p

conn.send(pickle.dumps(B))# для сериализации данных в байтовую строку

key = A ** b % p


while True:
    try:
        message = receive(conn, key)
        print(message)
        send_message(conn, 'Сообщение успешно получено и расшифровано', key)
    except EOFError: 
        break

conn.close()
