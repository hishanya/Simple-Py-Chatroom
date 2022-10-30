# importing all the required modules
import threading
import socket
import os


class Server(threading.Thread):
    # Create socket
    def __init__(self, host, port):
        super().__init__()
        self.connections = []
        self.host = '127.0.0.1'
        self.port = 60443
    
    def run(self):
        #TCP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.host, self.port))
        sock.listen(1)
        print('Listening at', sock.getsockname())

        while True:

            # Accept new connection
            sc, sockname = sock.accept()
            print('New connection from {} to {}'.format(sc.getpeername(), sc.getsockname()))

            # A new thread
            server_socket = ServerSocket(sc, sockname, self)
            server_socket.start()

            # Add thread to active connections
            self.connections.append(server_socket)
            print('Ready to receive messages from', sc.getpeername())

    def broadcast(self, message, source):
        for connection in self.connections:

            # Send to all in chat (not including self)
            if connection.sockname != source:
                connection.send(message)
    
    def remove_connection(self, connection):
        # Remove connection
        self.connections.remove(connection)


class ServerSocket(threading.Thread):
    def __init__(self, sc, sockname, server):
        super().__init__()
        self.sc = sc
        self.sockname = sockname
        self.server = server
    
    def run(self):
        while True:
            message = self.sc.recv(1024).decode('ascii')
            # Show messages
            if message:
                print('{} says {!r}'.format(self.sockname, message))
                self.server.broadcast(message, self.sockname)
            #Show when a client leaves
            else:
                print('{} has closed the connection'.format(self.sockname))
                self.sc.close()
                server.remove_connection(self)
                return
    # Send all
    def send(self, message):
        self.sc.sendall(message.encode('ascii'))


def exit(server):
    while True:
        ex_input = input('')
        # Enter 'shutdown' to shutdown the server
        if ex_input == 'shutdown':
            print('Closing all connections...')
            for connection in server.connections:
                connection.sc.close()
            print('Shutting down...')
            os._exit(0)

# Start/Exit server
if __name__ == '__main__':
    server = Server('127.0.0.1', 60443)
    server.start()
    exit = threading.Thread(target = exit, args = (server,))
    exit.start()