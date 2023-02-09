CONNECTOR = "->"

def parse_mapping(mapping_filename, mapping_graph):
    handle_comment = lambda comment: print(f"[COMMENT] {comment}")

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
            assert CONNECTOR in line, f"[LINE {index - 1}] each mapping should have at least one connector"
            connections = line.split(CONNECTOR)
            print(connections)
            # for c in range(len(connections - 1)):
            #     mapping_graph()

