import ahocorasick
from queue import Queue
import collections

class Transaction:

    def __init__(self, t):
        self.id = t['id']
        self.account = t['account']
        self.date = t['date']
        self.cost = t['cost']
        self.description = t['description']

    def get_description(self):
        return self.description
    
    def get_cost(self):
        return self.cost

    def __str__(self):
        return f"[{self.cost}] {self.description}"

class TransactionGraph:

    def __init__(self, empty_graph, transactions):
        self.g = empty_graph
        self.transactions = [Transaction(t) for t in transactions]
        self.leaves_categories = self._get_leaves()
        self.aho = ahocorasick.Automaton()
        self._setup_aho()
        self._setup_transactions()

    def _setup_transactions(self):
        # Put each transaction in its appropriate category based on aho results
        for t in self.transactions:
            desc = t.get_description()
            leaf_category = self.search_category(desc)
            assert len(leaf_category) > 0, f"The description {desc} has no category!"
            leaf_category = leaf_category[0]
            self.g.nodes[leaf_category]['transactions'].append(t)
    
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

    def _get_roots(self):
        roots = []
        for node in self.g.nodes:
            if self.g.in_degree[node] == 0:
                roots.append(node)
        return roots

    def _get_inner_nodes(self):
        inner = []
        for node in self.g.nodes:
            if self.g.in_degree[node] > 0:
                inner.append(node)
        return inner

    def get_cost_map(self, config):
        # Up-propagates transactions, and returns a map 
        # with each category and its enclosing transactions
        # A parent will contain all transactions it can reach through its
        # recursive children in this way
        leaves = self.leaves_categories
        q = Queue()
        # Bottom-most children
        [q.put(l) for l in leaves]

        # Populate initial map of leaf -> transactions within it
        tmap = collections.defaultdict(set)
        for l in leaves:
            tmap[l] = self.g.nodes[l]['transactions']

        while q.qsize() > 0:
            # pop a node
            node = q.get()
            
            # Grab its current transactions
            cts = tmap[node]

            # Grab its parent
            parent = list(self.g.predecessors(node))
            assert len(parent) <= 1, f"No node should have more than one parent! {parent} -> {node}"
            
            if len(parent) == 0: # The node is a root (no parent). It is complete
                continue

            parent = parent[0]

            # Give the parent its child transactions
            tmap[parent].update(cts)

            # Put the parent into the queue
            q.put(parent)

        display_style = config['DISPLAY_STYLE']
        if display_style == "ROOTS":
            inner = self._get_inner_nodes()
            for i in inner:
                del tmap[i]
        elif display_style == "ALL":
            pass

        return tmap


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
