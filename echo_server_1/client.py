import socket

sock = socket.socket()
#объект сокета.по умолчанию применяется протокол управления передачей (TCP)
while True:
    try:
        address = input("Введите адрес сервера: ")
        if address == '':
            address = 'localhost'
        while True:
            port = int(input("Введите порт (диапозон 1024-65535): "))
            if 1024 <= port <= 65535:
                break
        sock.connect((address, port)) #для подключения сокета к удаленному адресу.
    except (socket.error, ValueError):
        print("Повторите ввод!")
    else:
        break

# массив для имитации сообщений от пользователя
msg = ["Привет", "Как дела?", "exit"]

# Цикл для имитации ввода сообщений пользователем
for i in range(len(msg)):
    sock.send(msg[i].encode()) # последовательность байтов в строку
    data = sock.recv(1024) # считывает по 1кбайт
    print(data.decode())

sock.close()
