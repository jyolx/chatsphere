# tests/test_gui.py
import unittest
from chatsphere import ChatGUI
from chatsphere import Peer
import tkinter as tk

class TestChatGUI(unittest.TestCase):

    def setUp(self):
        # Create a mock peer for the GUI
        self.peer = Peer(port=5000)
        self.gui = ChatGUI(self.peer)

    def test_gui_components(self):
        """Test if the GUI components are created."""
        self.assertIsInstance(self.gui.root, tk.Tk)
        self.assertIsInstance(self.gui.chat_area, tk.scrolledtext.ScrolledText)
        self.assertIsInstance(self.gui.msg_entry, tk.Entry)
        self.assertIsInstance(self.gui.send_button, tk.Button)

    def test_display_message(self):
        """Test if the display_message function works."""
        test_message = "Hello, World!"
        self.gui.display_message(test_message)
        # Check if the message appears in the chat area
        self.assertIn(test_message, self.gui.chat_area.get("1.0", tk.END))

if __name__ == '__main__':
    unittest.main()
