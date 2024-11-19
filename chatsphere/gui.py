import threading
import tkinter as tk
from tkinter import simpledialog, scrolledtext, messagebox


class ClientGui:
    def __init__(self, client):
        self.master = tk.Tk()
        self.master.withdraw()  # Hide until authenticated
        self.client = client
        self.selected_user = None

        
    def setup_auth_gui(self):
        self.auth_window = tk.Toplevel()
        self.auth_window.title("Login")
        tk.Label(self.auth_window, text="Username:").pack(padx=10, pady=5)
        self.username_entry = tk.Entry(self.auth_window)
        self.username_entry.pack(padx=10, pady=5)
        tk.Label(self.auth_window, text="Password:").pack(padx=10, pady=5)
        self.password_entry = tk.Entry(self.auth_window, show='*')
        self.password_entry.pack(padx=10, pady=5)
        tk.Button(
            self.auth_window,
            text="Login",
            command=lambda: self.client.authenticate(self),
        ).pack(padx=10, pady=10)


    def setup_chat_gui(self):
        self.auth_window.destroy()
        self.master.deiconify()
        self.master.title(f"Chat Client : {self.client.username}")

        self.frame = tk.Frame(self.master)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.user_listbox = tk.Listbox(self.frame)
        self.user_listbox.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        self.user_listbox.bind('<<ListboxSelect>>', self.on_user_select)

        self.text_area = scrolledtext.ScrolledText(self.frame)
        self.text_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.text_area.config(state='disabled')

        self.entry_message = tk.Entry(self.master, width=50)
        self.entry_message.pack(padx=20, pady=5)
        self.entry_message.bind("<Return>", self.send_message)

        self.button_send = tk.Button(self.master, text="Send", command=self.send_message)
        self.button_send.pack(padx=20, pady=5)



    def unauthenticated(self):
        print("Unauthenticated")
        messagebox.showerror("Authentication Failed", "Invalid username or password")
        self.auth_window.destroy()
        exit(1)
    
    def update_user_list(self, connected_users):
        self.user_listbox.delete(0, tk.END)
        for user in connected_users:
            if user != self.client.username:
                self.user_listbox.insert(tk.END, user)
    
    def display_message(self, message):
        self.text_area.config(state='normal')
        self.text_area.insert('end', message + '\n')
        self.text_area.config(state='disabled')
        self.text_area.yview('end')
    
    def send_message(self, event=None):
        message = self.entry_message.get()
        if message.strip():
            self.client.send_message(message)
            self.entry_message.delete(0, 'end')
    
    def on_user_select(self, event):
        self.selected_user = self.user_listbox.get(tk.ACTIVE)
        self.text_area.config(state='normal')
        self.text_area.delete(1.0, tk.END)
        if self.selected_user in self.client.chats:
            for msg in self.client.chats[self.selected_user]:
                self.text_area.insert('end', msg + '\n')
        self.text_area.config(state='disabled')