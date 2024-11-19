import socket
import threading
import struct
from .gui import ClientGui
from tkinter import messagebox

class ChatClient:
    def __init__(self, host='127.0.0.1', port=8081):
        self.host = host
        self.port = port
        self.connected_users = []
        self.username = None
        self.gui = None
        self.chats = {}

    def authenticate(self, gui):
        self.gui = gui
        self.username = gui.username_entry.get().strip()
        password = gui.password_entry.get().strip()

        if not self.username or not password:
            messagebox.showerror("Error", "Username and password cannot be empty")
            return

        try:
            # Send username and password
            msg = self.username.encode('utf-8')
            self.client_socket.send(struct.pack('I', len(msg)))
            self.client_socket.send(msg)

            msg = password.encode('utf-8')
            self.client_socket.send(struct.pack('I', len(msg)))
            self.client_socket.send(msg)

            # Wait for server's authentication response
            ml = self.client_socket.recv(4)
            l = struct.unpack('I', ml)[0]
            auth_response = self.client_socket.recv(l).decode('utf-8')

            if "successful" in auth_response:
                gui.setup_chat_gui()
                threading.Thread(target=self.receive_messages, daemon=True).start()
            else:
                gui.unauthenticated()
        except Exception as e:
            messagebox.showerror("Error", f"Authentication failed: {e}")
            self.client_socket.close()



    def receive_messages(self):
        while True:
            try:
                ml = self.client_socket.recv(4)
                l = struct.unpack('I', ml)[0]
                message = self.client_socket.recv(l).decode('utf-8')
                print(f"Received: {message}")  # Debugging

                if message.startswith("USERLIST:"):
                    self.update_user_list(message[9:])
                else:
                    sender, receiver, msg = message.split(':', 2)
                    if sender not in self.chats:
                        self.chats[sender] = []
                    self.chats[sender].append(f"{sender}: {msg}")
                    if self.gui.selected_user == sender:
                        self.gui.display_message(f"{sender}: {msg}")
            except Exception as e:
                print(f"Error in receive_messages: {e}")
                self.client_socket.close()
                break

    def update_user_list(self, user_list_str):
        self.connected_users = user_list_str.split(',')
        self.gui.update_user_list(self.connected_users)

    def send_message(self, message):
        selected_user = self.gui.selected_user
        if selected_user:
            full_message = f"{self.username}:{selected_user}:{message}".encode('utf-8')
            try:
                self.client_socket.send(struct.pack('I', len(full_message)))
                self.client_socket.send(full_message)

                if selected_user not in self.chats:
                    self.chats[selected_user] = []
                self.chats[selected_user].append(f"{self.username}: {message}")
                self.gui.display_message(f"{self.username}: {message}")
            except Exception as e:
                print(f"Error sending message: {e}")

    def start(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))
            self.gui = ClientGui(self)
            self.gui.setup_auth_gui()  # This initializes the login GUI

            # Start the tkinter event loop in the main thread
            self.gui.master.mainloop()
        except Exception as e:
            messagebox.showerror("Error", f"Connection failed: {e}")
            exit(1)



