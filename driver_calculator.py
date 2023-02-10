from classes.parser import *
import networkx as nx

config = parse_config("./CONFIG.txt")
transactions = parse_rbc_csvs("./rbc_transaction_csvs", config)

# mapping_graph = nx.MultiDiGraph()
# parse_mapping("./mappings/mapping1.txt", mapping_graph)

# for a, b, _ in mapping_graph.edges:
#     print(mapping_graph.nodes[a], mapping_graph.nodes[b])