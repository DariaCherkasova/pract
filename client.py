import socket
import pickle
from random import randint

def combinaton(message, key):
    #шифрование сообщения
    P2 = []
    for i in range(len(message)):
        P2 += chr(ord(message[i]) ^ key)
    return ''.join(P2)

def send_message(sock, message, key):
    #отправляет сообщение через сокет
    message = combinaton(message, key)
    #возвращает его сериализованное представление в виде байтовой строки
    #отправляет зашифрованное сообщение через сокет, используя модуль 'pickle для сериализации сообщения в байтовую строку
    sock.send(pickle.dumps(message))

def receive(sock, key):
    message = pickle.loads(sock.recv(1024)) #получение
    message = combinaton(message, key) #отправляет сообщение через сокет
    return message

HOST = '127.0.0.1'
PORT = 8080

sock = socket.socket()
sock.connect((HOST, PORT))

p = randint(0,10000)
g = randint(0,10000)
a = randint(0,10000)

A = g ** a % p
sock.send(pickle.dumps((p, g, A))) # для сериализации данных в байтовую строку

B = pickle.loads(sock.recv(1024)) #получает и десериализует значение B, отправленное сервером через сокет, используя модуль pickle

key = B ** a % p

message = input("Сообщение: ")
while message != 'exit':
    send_message(sock, message, key)
    print(receive(sock, key))
    message = input("Сообщение: ")

sock.close()
