from classes.parser import *
from classes.finance_display import FinanceDisplay
from classes.transaction_graph import TransactionGraph
import networkx as nx

config = parse_config("./CONFIG.txt")
transactions = parse_transactions("./rbc_transaction_csvs", config)

mapping_graph = nx.MultiDiGraph()
parse_mapping("./mappings/mapping1.txt", mapping_graph)

tg = TransactionGraph(mapping_graph, transactions)
undefined = TransactionGraph.undefined_transactions(transactions, tg)

assert len(undefined) == 0, "The following transactions have undefined category(ies)\n\t" + "\n\t".join([u + ": " + str(len(u)) for u in undefined])
tmap = tg.get_cost_map(config)

display = FinanceDisplay(tmap)
display.display()
# for a, b, _ in mapping_graph.edges:
#     print(a, mapping_graph.nodes[a], b, mapping_graph.nodes[b])