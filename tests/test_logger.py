# tests/test_logger.py
import unittest
import logging
from chatsphere import setup_logger

class TestLogger(unittest.TestCase):

    def setUp(self):
        # Set up a test logger
        self.logger = setup_logger('test_logger', 'test.log')

    def test_log_info(self):
        """Test if the logger writes an info message."""
        self.logger.info("This is a test info message")
        with open('test.log', 'r') as log_file:
            logs = log_file.read()
            self.assertIn("This is a test info message", logs)

    def test_log_error(self):
        """Test if the logger writes an error message."""
        self.logger.error("This is a test error message")
        with open('test.log', 'r') as log_file:
            logs = log_file.read()
            self.assertIn("This is a test error message", logs)

if __name__ == '__main__':
    unittest.main()
