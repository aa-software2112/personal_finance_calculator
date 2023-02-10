
class TransactionGraph:

    def __init__(self, empty_graph, data_to_fill_graph):
        self.g = empty_graph
        self.data = data_to_fill_graph
        self.leaves_categories = self._get_leaves()
    
    def _get_leaves(self):
        leaves = []
        for node in self.g.nodes:
            if self.g.out_degree[node] == 0:
                leaves.append(node)
        return leaves