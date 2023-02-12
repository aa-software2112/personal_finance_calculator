from classes.parser import *
from classes.finance_display import FinanceDisplay
from classes.transaction_graph import TransactionGraph
from classes.category_searcher import CategorySearcher
import networkx as nx

config = parse_config("./CONFIG.txt")
transactions = parse_transactions("./rbc_transaction_csvs", config)

mapping_graph = nx.MultiDiGraph()
parse_mapping("./mappings/mapping1.txt", mapping_graph)

# Grab the leafs... These are the categories
leaves = []
for node in mapping_graph.nodes:
    if mapping_graph.out_degree[node] == 0:
        leaves.append(node)

cs = CategorySearcher(leaves)
undefined = cs.undefined_transactions(transactions)
assert len(undefined) == 0, "The following transactions have undefined category(ies)\n\t" + "\n\t".join([u + ": " + str(len(u)) for u in undefined])

tg = TransactionGraph(mapping_graph, transactions, cs)

# Should refactor the display to take the graph and grab what it needs... Display based on "all" or "roots", etc...
tmap = tg.get_cost_map(config)

display = FinanceDisplay(tmap)
display.display()
# for a, b, _ in mapping_graph.edges:
#     print(a, mapping_graph.nodes[a], b, mapping_graph.nodes[b])