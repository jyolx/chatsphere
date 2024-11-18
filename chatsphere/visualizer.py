import networkx as nx
import matplotlib.pyplot as plt

class NetworkVisualizer:
    def __init__(self):
        self.graph = nx.Graph()

    def add_node(self, node_id):
        self.graph.add_node(node_id)

    def add_edge(self, node1, node2):
        self.graph.add_edge(node1, node2)

    def draw(self):
        plt.figure(figsize=(8, 8))
        nx.draw(self.graph, with_labels=True, node_color='skyblue', font_weight='bold', node_size=2000)
        plt.show()
