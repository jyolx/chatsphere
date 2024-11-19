import socket
import threading
import logging
import json
import struct

class ChatServer:
    def __init__(self, host='127.0.0.1', port=8081, user_file='users.json'):
        self.host = host
        self.port = port
        self.user_file = user_file
        self.clients = {}
        self.setup_logging()
        self.load_users()

    def setup_logging(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', handlers=[logging.FileHandler('logs/server.log'), logging.StreamHandler()])

    def load_users(self):
        try:
            with open(self.user_file, 'r') as file:
                users = json.load(file)
            self.users = users
            logging.info(f"Loaded users from {self.user_file}")
        except FileNotFoundError:
            logging.error(f"User file not found: {self.user_file}")
            exit(1)
        except json.JSONDecodeError:
            logging.error(f"Invalid JSON in user file: {self.user_file}")
            exit(1)

    def authenticate(self, client_socket):
        try:
            # Receive the username length and data
            l = client_socket.recv(4)
            if len(l) < 4:
                logging.error("Received incomplete username length header")
                return False
    
            l = struct.unpack('I', l)[0]
            if l <= 0:
                logging.error("Received invalid username length")
                return False
    
            username = client_socket.recv(l).decode('utf-8')
            if not username:
                logging.error("Received empty username")
                return False
    
            # Receive the password length and data
            l = client_socket.recv(4)
            if len(l) < 4:
                logging.error("Received incomplete password length header")
                return False
    
            l = struct.unpack('I', l)[0]
            if l <= 0:
                logging.error("Received invalid password length")
                return False
    
            password = client_socket.recv(l).decode('utf-8')
            if not password:
                logging.error("Received empty password")
                return False
    
            # Validate credentials
            if username in self.users and self.users[username] == password:
                msg = "successful".encode('utf-8')
                client_socket.send(struct.pack('I', len(msg)))
                client_socket.send(msg)
                logging.info(f"User {username} authenticated successfully")
                self.clients[username] = client_socket
                self.update_user_list()
                return True
            else:
                msg = "failed".encode('utf-8')
                client_socket.send(struct.pack('I', len(msg)))
                client_socket.send(msg)
                logging.info(f"User {username} failed to authenticate")
                return False
        except Exception as e:
            logging.error(f"Error during authentication: {e}")
            return False


        
    def update_user_list(self):
        user_list = ','.join(self.clients.keys())
        for client in self.clients.values():
            msg = f"USERLIST:{user_list}".encode('utf-8')
            client.send(struct.pack('I', len(msg)))
            client.send(msg)
        logging.info(f"User list updated: {user_list} and sent to all clients")

    def forward(self, message):
        header = message.split(':')
        if(header[1] in self.clients):
            self.clients[header[1]].send(struct.pack('I', len(message.encode('utf-8'))))
            self.clients[header[1]].send(message.encode('utf-8'))
            logging.info(f"Forwarded message to {header[1]}")
        else:
            logging.info(f"User {header[1]} not found")

    def remove_client(self, client_socket):
        for username, client in self.clients.items():
            if client == client_socket:
                del self.clients[username]
                break
        self.update_user_list()

    def handle_client(self, client_socket, addr):
        while True:
            try:
                l = client_socket.recv(4)
                if len(l) < 4:
                    raise ValueError("Invalid length header")

                l = struct.unpack('I', l)[0]
                if l <= 0:
                    raise ValueError("Invalid message length")

                message = client_socket.recv(l).decode('utf-8')
                if message:
                    logging.info(f"Received message from {addr}: {message}")
                    self.forward(message)
                else:
                    raise ValueError("Empty message received")
            except Exception as e:
                logging.error(f"Error handling client {addr}: {e}")
                client_socket.close()
                self.remove_client(client_socket)
                break

        
    def start(self):

        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as e:
            logging.error(f"Error creating socket: {e}")
            exit(1)

        try:
            server.bind((self.host, self.port)) 
        except socket.error as e:
            logging.error(f"Error binding socket: {e}")
            exit(1)

        try:
            server.listen(5)
        except socket.error as e:
            logging.error(f"Error listening on socket: {e}")
            exit(1)

        logging.info(f"Server started {self.host}:{self.port}")

        while True:
            client_socket, addr = server.accept()
            logging.info(f"Connection from {addr}")

            if self.authenticate(client_socket):
                threading.Thread(target=self.handle_client, args=(client_socket, addr)).start()
            else:
                client_socket.close()
    
    
