# tests/test_visualizer.py
import unittest
from chatsphere import NetworkVisualizer

class TestNetworkVisualizer(unittest.TestCase):

    def setUp(self):
        self.visualizer = NetworkVisualizer()

    def test_add_node(self):
        """Test adding a node to the network visualizer."""
        self.visualizer.add_node("peer1")
        self.assertIn("peer1", self.visualizer.graph.nodes)

    def test_add_edge(self):
        """Test adding an edge between two nodes."""
        self.visualizer.add_node("peer1")
        self.visualizer.add_node("peer2")
        self.visualizer.add_edge("peer1", "peer2")
        self.assertIn(("peer1", "peer2"), self.visualizer.graph.edges)

    def test_draw(self):
        """Test drawing the network visualization."""
        self.visualizer.add_node("peer1")
        self.visualizer.add_node("peer2")
        self.visualizer.add_edge("peer1", "peer2")
        # Since we're not validating the visual output, just ensure no exceptions
        try:
            self.visualizer.draw()
        except Exception as e:
            self.fail(f"draw() raised {e} unexpectedly!")

if __name__ == '__main__':
    unittest.main()
