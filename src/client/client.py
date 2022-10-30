# Sha'nya Conaway
# importing all the required modules
import socket
import threading
import os
import sys
from tkinter import *
import tkinter as tk

class Send(threading.Thread):
    def __init__(self, sock, name):
        super().__init__()
        self.sock = sock
        self.name = name

    def run(self):
        while True:
            print('{}: '.format(self.name), end='')
            sys.stdout.flush()
            message = sys.stdin.readline()[:-1]

            # Entering '.exit' to leave the chatroom
            if message == '.exit':
                self.sock.sendall('{} has left the chat.'.format(self.name).encode('ascii'))
                break
            
            # Message to server 
            else:
                self.sock.sendall('{}: {}'.format(self.name, message).encode('ascii'))
        
        print('\nLeaving...')
        self.sock.close()
        os._exit(0)

class Receive(threading.Thread):
    def __init__(self, sock, name):
        super().__init__()
        self.sock = sock
        self.name = name
        self.messages = None
    
    # Receive messages
    def run(self):
        while True:
            message = self.sock.recv(1024).decode('ascii')

            if message:

                if self.messages:
                    self.messages.insert(tk.END, message)
                    print('hi')
                    print('\r{}\n{}: '.format(message, self.name), end = '')
                
                else:
                    print('\r{}\n{}: '.format(message, self.name), end = '')
            
            else:
                # Server connect lost, exit
                print('\n\n**Connection to server lost**')
                print('\nClosing...')
                self.sock.close()
                os._exit(0)

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.name = None
        self.messages = None
    
    # Connect to server
    def start(self):
        print('Trying to connect to {}:{}...'.format(self.host, self.port))
        self.sock.connect((self.host, self.port))
        print('Successfully connected to {}:{}'.format(self.host, self.port))
        
        print()
        self.name = input('Your name: ')

        print()
        print('Welcome, {}!'.format(self.name))

        # Create send and receive threads
        send = Send(self.sock, self.name)
        receive = Receive(self.sock, self.name)

        # Start send and receive threads
        send.start()
        receive.start()
        
        # Client joined
        self.sock.sendall('{} has joined the chat.'.format(self.name).encode('ascii'))
        print("\rTo leave the chat, enter '.exit'\n")
        print('{}: '.format(self.name), end = '')

        return receive

    def send(self, t_input):
        # Sending message
        message = t_input.get()
        t_input.delete(0, tk.END)
        self.messages.insert(tk.END, '{}: {}'.format(self.name, message))

        # Type 'QUIT' to leave the chatroom
        if message == '.exit':
            self.sock.sendall('{} has left the chat.'.format(self.name).encode('ascii'))
            
            print('\nLeaving...')
            self.sock.close()
            os._exit(0)
        
        # Send all
        else:
            self.sock.sendall('{}: {}'.format(self.name, message).encode('ascii'))

def main(host, port):

    # Simple GUI for chatroom
    client = Client(host, port)
    receive = client.start()
    chatgui = tk.Tk()
    chatgui.title('Simple Chat App')

    # Display messages
    f_messages = tk.Frame(master=chatgui)
    scrollbar = tk.Scrollbar(master=f_messages)
    messages = tk.Listbox(
        master=f_messages, 
        yscrollcommand=scrollbar.set
    )
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y, expand=False)
    messages.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    client.messages = messages
    receive.messages = messages

    # Defining GUI style
    f_messages.grid(row=0, column=0, columnspan=2, sticky="nsew")

    f_entry = tk.Frame(master=chatgui)
    t_input = tk.Entry(master=f_entry)
    t_input.pack(fill=tk.BOTH, expand=True)
    t_input.bind("<Return>", lambda x: client.send(t_input))
    t_input.insert(0, "Send your first message!")

    btn_send = tk.Button(
        master=chatgui,
        text='Send',
        command=lambda: client.send(t_input)
    )

    # Defining GUI style
    f_entry.grid(row=1, column=0, padx=10, sticky="ew")
    btn_send.grid(row=1, column=1, pady=10, sticky="ew")

    chatgui.rowconfigure(0, minsize=500, weight=1)
    chatgui.rowconfigure(1, minsize=50, weight=0)
    chatgui.columnconfigure(0, minsize=500, weight=1)
    chatgui.columnconfigure(1, minsize=200, weight=0)

    chatgui.mainloop()

if __name__ == '__main__':
    main('127.0.0.1', 60443)