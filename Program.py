import csv


########################################################################
### ---------------------- Parse Lookup Table  --------------------- ###
########################################################################

# Funct parse & create dictionary 
# (dstport + protocol) has unique tag --> key = (dstport + protocol), val = tag

def parse_lookup_table(file_path):
    # Initialize
    lookup = {}
    seen_keys = set()

    # Open and Read CSV File
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)

        for row in reader:
            # Parse Row
            port = row['dstport'].strip()
            protocol = row['protocol'].strip().lower()
            tag = row['tag'].strip()

            # Create Dictionary
            key = (port, protocol)
            if key in seen_keys:
                print(f"Warning: Duplicate entry for ({port}, {protocol}) — overwriting previous tag!")
            seen_keys.add(key)
            lookup[key] = tag

    # File is closed, return lookup dictionary
    return lookup


########################################################################
### --------------------- Parse Flow Log File  --------------------- ###
########################################################################

def parse_flow_logs(file_path, lookup):
    # Initialize
    protocol_map = {'6': 'tcp', '17': 'udp', '1': 'icmp'}
    tag_counts = {}
    port_proto_counts = {}

    # Create "Lines" as a 'List of Cleaned Strings' (one str per log entry)
    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    # Iterate
    for line in lines:
        # Create list of values for line & skip invalid lines
        fields = line.split()
        if len(fields) < 14:
            print(f"Line padded due to missing fields: {line}")
        while len(fields) < 8:
            fields.append('')

        # Find dstport, protocol
        dstport = fields[6]
        protocol_num = fields[7]
        protocol = protocol_map.get(protocol_num, 'unknown')
        key = (dstport, protocol)

        # Find tag, given key
        tag = lookup.get(key, 'Untagged')
        print(f"Tag assigned: {tag} — from dstport={dstport}, protocol={protocol}")

        # Update counter
        tag_counts[tag] = tag_counts.get(tag, 0) + 1
        port_proto_counts[key] = port_proto_counts.get(key, 0) + 1

    return tag_counts, port_proto_counts


########################################################################
### ------------------- Main: Write Output File  ------------------- ###
########################################################################

def write_output_files(tag_counts, port_proto_counts):
    with open("tag_counts.csv", "w") as f:
        f.write("Tag,Count\n")
        for tag, count in tag_counts.items():
            f.write(f"{tag},{count}\n")

    with open("port_protocol_counts.csv", "w") as f:
        f.write("Port,Protocol,Count\n")
        for (port, protocol), count in port_proto_counts.items():
            f.write(f"{port},{protocol},{count}\n")

def main():
    lookup_file = "lookup_table.csv"
    flow_log_file = "flow_logs.txt"

    # Parse the lookup table and flow logs
    lookup = parse_lookup_table(lookup_file)
    tag_counts, port_proto_counts = parse_flow_logs(flow_log_file, lookup)

    # Write the output files
    write_output_files(tag_counts, port_proto_counts)

if __name__ == "__main__":
    main()
