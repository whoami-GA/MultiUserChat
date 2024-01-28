#!/usr/bin/env python3

import threading
import socket
from tkinter import *
from tkinter.scrolledtext import ScrolledText
import time
import ssl


def send_message(client_socket, username, text_widget, entry_widget):
    #print(f"\nThe enter Key has pressed\n")
    message = entry_widget.get()
    #print(f"\n[!]The user {username} has send a message: \n{message}")
    client_socket.sendall(f"{username} > {message}".encode())
    
    entry_widget.delete(0, END)
    text_widget.configure(state='normal') # se pone en normal para que cuando le des al anter se abra para poder entrar la data de message al darle enter
    text_widget.insert(END, f"{username} > {message}\n")
    text_widget.configure(state='disabled')

def recive_message(client_socket, text_widget):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            
            if not message:
                break

            text_widget.configure(state='normal') # se pone en normal para que cuando le des al anter se abra para poder entrar la data de message al darle enter
            text_widget.insert(END, message)
            text_widget.configure(state='disabled')

        except:
            break


def exit_request(client_socket, username, window):

    client_socket.sendall(f"[!] User {username} has left the chat\n".encode())
    client_socket.close()

    window.quit()
    window.destroy()


def list_users(client_socket):
    client_socket.sendall("!user".encode())
    print(f"\n[!] Request Send")


def client_program():
    host = 'localhost'
    port = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket = ssl.wrap_socket(client_socket)
    client_socket.connect((host, port))
    
    username = input(f"[@] Enter your username: ")
    client_socket.sendall(username.encode())

    window = Tk()
    window.configure(bg='#553739')
    window.title("Chat")

    text_widget = ScrolledText(window, state='disable', bg='#232020') # si no pones nada python lo pone automaticamente, state se hace para bloquear la introduccion de texto
    text_widget.configure(bg='#748e54', font=("Consolas",11))
    text_widget.pack(padx=5,pady=5)

    frame_widget = Frame(window, bg='')
    frame_widget.pack(padx=5,pady=5, fill=BOTH, expand=1)

    entry_widget = Entry(frame_widget)
    entry_widget.bind("<Return>", lambda _: send_message(client_socket, username, text_widget, entry_widget)) # return = Enter(Boton)
    entry_widget.configure(bg='#955e42')
    entry_widget.pack(side=LEFT, fill=X, expand=1)

    #Send Botton
    button_widget = Button(frame_widget,text="Send", command=lambda: send_message(client_socket, username, text_widget, entry_widget))
    button_widget.pack(side=RIGHT, padx=5)


    #Users Botton
    users_widget = Button(window,text="Users Lists", command=lambda: list_users(client_socket))
    users_widget.pack(padx=5, pady=5)

    exit_widget = Button(window,text="Exit", command=lambda: exit_request(client_socket, username, window))
    exit_widget.pack(padx=5, pady=5)


    thread = threading.Thread(target=recive_message, args=(client_socket, text_widget))
    thread.daemon= True
    thread.start()


    window.mainloop()
    client_socket.close()

if __name__ == '__main__':
    client_program()
