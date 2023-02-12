from glob import glob
from os import path
MAPPING_CONNECTOR = "->"
CONFIG_DELIMITER = "="
handle_comment = lambda comment: None

month_to_num = {"january": 1,
                "february": 2,
                "march": 3,
                "april": 4,
                "may": 5,
                "june": 6,
                "july": 7,
                "august": 8,
                "september": 9,
                "october": 10,
                "november": 11,
                "december": 12}

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
            assert MAPPING_CONNECTOR in line, f"[LINE {index}] each mapping should have at least one connector"
            connections = line.split(MAPPING_CONNECTOR)
            assert len(connections) == len(set(connections)), f"[LINE {index}] Transaction and categories should be unique... {line}"
            for c in range(len(connections) - 1):
                from_node = connections[c + 1]
                to_node = connections[c]
                
                # if c == 0: # Most detailed category should have a list for later object storage
                    # mapping_graph.add_node(to_node, data)
                mapping_graph.add_node(from_node, transactions=[])
                mapping_graph.add_node(to_node, transactions=[])                
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
        k = k.strip()
        v = v.strip()
        assert not (CONFIG_DELIMITER in v), f"[DELIMITER] Do not put {CONFIG_DELIMITER} in RHS of {line}"
        if v.startswith("["):
            v = eval(v)
        config[k] = v
    return config 

def parse_transactions(csv_folder, config):
    csvs = glob(path.join(csv_folder, "*.csv"))
    
    dmy = config['DATE_FORMAT'].lower().split("/")
    month_idx = -1
    year_idx = -1
    for i in range(len(dmy)):
        if dmy[i] == "mm":
            month_idx = i
        elif dmy[i] == "yyyy":
            year_idx = i
    assert month_idx != -1 and year_idx != -1, "[CONFIG.TXT] Could not find appropriate "\
        " month and year index. Adjust DATE_FORMAT in CONFIG.TXT"
    
    month = month_to_num[config['MONTH'].lower()]
    year = int(config['YEAR'])

    account_label = config['ACCOUNT_TYPE_LABEL']
    date_label = config['DATE_LABEL']
    cost_label = config['COST_LABEL']
    description_label = config['DESCRIPTION_LABEL']
    description_fallback_label = config['DESCRIPTION_FALLBACK_LABEL']
    account_type = config['ACCOUNT_TYPE']

    account_label_idx = -1
    date_label_idx = -1
    cost_label_idx = -1
    description_label_idx = -1
    description_fallback_label_idx = -1
    
    kept_data = []

    for csv in csvs:
        with open(csv, 'r') as file:
            lines = file.readlines()
            assert len(lines) > 1, f"[CSV] {csv} likely has no data. Remove it from listing"

            cols = lines[0].strip().replace("\"", "").split(",")
            for c in range(len(cols)):
                if cols[c] == account_label:
                    account_label_idx = c
                elif cols[c] == date_label:
                    date_label_idx = c
                elif cols[c] == cost_label:
                    cost_label_idx = c
                elif cols[c] == description_label:
                    description_label_idx = c
                elif cols[c] == description_fallback_label:
                    description_fallback_label_idx = c

            assert account_label_idx != -1 and date_label_idx != -1 \
                and cost_label_idx != -1 and description_label_idx != -1 and description_fallback_label_idx != -1, \
                    "[CONFIG] Could not find index for one of the four key labels. See CONFIG.TXT " \
                        f"ACCOUNT: {account_label_idx}, DATE: {date_label_idx}, COST: {cost_label_idx} " \
                            f"DESCRIPTION: {description_label_idx}, DESCRIPTION FALLBACK: {description_fallback_label_idx}"

            for i in range(1, len(lines)):
                line = lines[i].strip().replace("\"", "").split(",")
                account = line[account_label_idx]
                date = line[date_label_idx].split("/")
                trans_month = int(date[month_idx])
                trans_year = int(date[year_idx])

                cost = line[cost_label_idx]
                description = line[description_label_idx]
                description_fallback = line[description_fallback_label_idx]
                assert len(description) > 0 or len(description_fallback) > 0, f"[DESCRIPTION] Line[{i+1}] {lines[i]} missing description"
                if account == account_type and month == trans_month and year == trans_year:
                    desc = description if len(description) > 0 else description_fallback
                    desc = description_fallback if desc in config['FALLBACKS'] else desc
                    desc = desc.strip()
                    kept_data.append({
                        "id": i,
                        "account": account,
                        "date": {"month": month,
                                "year": year},
                        "cost": float(cost),
                        "description": desc,
                        "hash": hash(lines[i]) # For line uniqueness
                    })
    return kept_data


    