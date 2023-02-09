from glob import glob
from os import path
MAPPING_CONNECTOR = "->"
CONFIG_DELIMITER = "="
handle_comment = lambda comment: print(f"[COMMENT] {comment}")

def parse_mapping(mapping_filename, mapping_graph):
    assert mapping_graph != None


    expected_parse_version = "1"
    lines = []
    
    with open(mapping_filename, 'r') as file:
        lines = file.readlines()

    # Strip lines
    lines = [l.strip() for l in lines]

    # Find and assert version
    index = 0
    correct_version = False
    while index < len(lines):
        line = lines[index]
        index += 1
        if "DSL_VERSION:" in line:
            actual_version = line.split(":")[-1]
            assert actual_version == expected_parse_version, f"[DSL VERSION] actual version {actual_version} " \
                    f"!= expected version {expected_parse_version}..."
            correct_version = True
            break
    
    assert correct_version == True, "[DSL VERSION] could not find version in file..."

    # Parse remainder of file
    while index < len(lines):
        line = lines[index]
        index += 1
        if line.startswith("#"): # comment
            handle_comment(line)
        elif len(line) == 0 or len(line.strip()) == 0: # empty line
            continue
        else: # Possibly a regular line
            assert MAPPING_CONNECTOR in line, f"[LINE {index - 1}] each mapping should have at least one connector"
            connections = line.split(MAPPING_CONNECTOR)
            for c in range(len(connections) - 1):
                from_node = connections[c + 1]
                to_node = connections[c]
                # if c == 0: # Most detailed category should have a list for later object storage
                    # mapping_graph.add_node(to_node, data)
                mapping_graph.add_nodes_from([from_node, to_node], listing=[])
                mapping_graph.add_edge(from_node, to_node)

def parse_config(config_filename):
    lines = []
    with open(config_filename, 'r') as file:
        lines = file.readlines()
    lines = [l.strip() for l in lines]

    config = {}
    COMMENT = "#"
    for line in lines:
        if line.startswith(COMMENT):
            handle_comment(line)
            continue
        elif len(line) == 0:
            continue

        assert CONFIG_DELIMITER in line, f"[DELIMIER] The character {CONFIG_DELIMITER} should appear in {line}"
        k, v = line.split("=")
        assert not (CONFIG_DELIMITER in v), f"[DELIMITER] Do not put {CONFIG_DELIMITER} in RHS of {line}"
        config[k] = v
    return config 

def parse_rbc_csvs(csv_folder):
    csvs = glob(path.join(csv_folder, "*.csv"))
    print(csvs)