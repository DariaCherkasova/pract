import socket
from threading import Thread 

def accept_incoming_connections():
	""" Set up new clients """
	while True:
		client, client_address = server.accept()
		print("{} клиент подключился".format(client_address))
		client.send("Добро пожаловать. Представтесь".encode())
		#addresses[client] = client_address
		Thread(target = handle_client, args=(client,)).start()

def handle_client(client):
	name = client.recv(1024).decode()
	welcome = "Привет %s! Если ты хочешь выйти, напиши {quit}" %name
	client.send(welcome.encode())
	msg = "%s теперь в чате" %name
	broadcast(msg.encode()) #посылает всем клиентам
	clients[client] = name

	while True:
		msg = client.recv(1024)
		if msg!=bytes("{quit}", "utf8"):
			broadcast(msg, name+": ")
		else:
			client.send(bytes("{quit}", "utf8"))
			client.close()
			del clients[client]
			broadcast("{} Покинул чат чат чат".format(name))
			break

def broadcast(msg, prefix=""):
	"""For all users"""
	for sock in clients:
		sock.send(bytes(prefix, "utf8")+msg)

clients={}
#addresses={}

host="127.0.0.1"
port=7072

server=socket.socket()
server.bind((host, port)) #привязывет сокет к адресу

if __name__ == "__main__":
	server.listen(2)
	print("Ожидание подключения...")
	accept_thread=Thread(target=accept_incoming_connections)
	accept_thread.start()
	accept_thread.join()
	server.close()
