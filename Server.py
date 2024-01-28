#!/usr/bin/env python3

import socket 
import threading
import time
import ssl

def client_thread(client_socket, clients, usernames):
    
    username = client_socket.recv(1024).decode()
    usernames[client_socket] = username
    
    print(f"The user {username} has connected")

    for client in clients: # enviar la data a todos los clientes
        if client is not client_socket: #si no soy yo envia el mensaje de que me he conectado al chat
            client.sendall(f"\n[+] The user {username} is logged connected to the chat\n\n".encode())
   
    while True:
        try:
            message = client_socket.recv(1024).decode()
            
            if not message:
                break
           
           # Check the users requests
            if message == "!user":
                client_socket.sendall(f"\n[!] The users are: {' ,'.join(usernames.values())}\n\n".encode())
                continue # para que no se envie de cliente en cliente, en este punto no continuara hasta que entre otro mensaje

            for client in clients:
                if client is not client_socket:
                    client.sendall(f"{message}\n".encode())

        except:
            break
    #print(f"[+] We are in client thread\n")
    client_socket.close()
    clients.remove(client_socket)
    del usernames[client_socket]

def server_program():
    
    host = 'localhost'
    port = 12345 

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET = Ipv4 Stram = TCP
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # TIME_WAIT, para que el servidor no se ponga en escucha
    server_socket.bind((host, port)) # Para ponerse en escucaha () esta es la forma
    server_socket = ssl.wrap_socket(server_socket, keyfile="server-key.key", certfile="server-cert.pem", server_side=True)
    server_socket.listen()

    print(f"\n[!] Server is listening for incoming conections...")

    clients = []
    usernames = {}

    while True:

        client_socket, address = server_socket.accept() # aqui haceptamos los clientes que se conectan y los almacenamos en clients 
        clients.append(client_socket)
        print(f"[+] A new client has connected: {address}")

        thread = threading.Thread(target=client_thread, args=(client_socket, clients, usernames)) # que utilize los threads en client socket clients y usernames
        thread.daemon = True # Si no se pone, cuando se ejecute el script, tanto como el servidor como el cliente si se cierra el programa, se cierran los hilos tambien, porque si no los hilos por detras se quedan arrancando pero en segundo plano. # Garantiza que los hilos hijos mueran.
        thread.start()
    
    server_socket.close()


if __name__ == '__main__':

    server_program()
