import ahocorasick


class TransactionGraph:

    def __init__(self, empty_graph, data_to_fill_graph):
        self.g = empty_graph
        self.data = data_to_fill_graph
        self.leaves_categories = self._get_leaves()
        self.aho = ahocorasick.Automaton()
        self._setup_aho()
    
    def _get_leaves(self):
        leaves = []
        for node in self.g.nodes:
            if self.g.out_degree[node] == 0:
                leaves.append(node)
        return leaves

    def _setup_aho(self):
        for category in self.leaves_categories:
            self.aho.add_word(category, category)
        self.aho.make_automaton()

    def search_category(self, v):
        ret = [v[1] for v in list(self.aho.iter(v))]
        assert len(ret) <= 1, f"[AHO] The search for {v} returned multiple entries... {ret}. Only 0 or 1 should match. Fix Mapping"
        return ret
    
    @staticmethod
    def undefined_transactions(transactions, tgraph):
        undef = []
        # Returns the transactions that could not be linked to a category
        for transaction in transactions:
            description = transaction['description']
            ret = tgraph.search_category(description)
            if len(ret) == 0:
                undef.append(description)
        return set(undef)