import tkinter as tk
from tkinter import scrolledtext

class ChatGUI:
    def __init__(self, peer):
        self.peer = peer

        # Setup GUI
        self.root = tk.Tk()
        self.root.title(f"ChatSphere - {peer.port}")
        self.chat_area = scrolledtext.ScrolledText(self.root, state='disabled', wrap=tk.WORD)
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.msg_entry = tk.Entry(self.root)
        self.msg_entry.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.X, expand=True)
        self.send_button = tk.Button(self.root, text="Send", command=self._send_message)
        self.send_button.pack(side=tk.RIGHT, padx=10, pady=10)

    def _send_message(self):
        message = self.msg_entry.get()
        if message:
            self.peer.logger.info(f"Sending message: {message}")
            self.display_message(f"You: {message}")
            self.msg_entry.delete(0, tk.END)

    def display_message(self, message):
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, f"{message}\n")
        self.chat_area.config(state='disabled')
        self.chat_area.yview(tk.END)

    def run(self):
        self.root.mainloop()
