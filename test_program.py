import os
from Program import main

def read_csv(file_path):
    with open(file_path, 'r') as f:
        return [line.strip() for line in f.readlines()[1:] if line.strip()]

def test_outputs():
    # Run the program
    main()

    # Check that output files exist
    assert os.path.exists("tag_counts.csv"), "tag_counts.csv was not created!"
    assert os.path.exists("port_protocol_counts.csv"), "port_protocol_counts.csv was not created!"

    # Read outputs
    tag_lines = read_csv("tag_counts.csv")
    port_proto_lines = read_csv("port_protocol_counts.csv")

    # Validate expected tag counts
    expected_tags = {
        "sv_P2,1",
        "sv_P1,2",
        "email,3",
        "Untagged,8"
    }

    for line in expected_tags:
        assert line in tag_lines, f"Missing tag count line: {line}"

    # Validate expected port/protocol counts
    expected_ports = {
        "49153,tcp,1",
        "49154,tcp,1",
        "49155,tcp,1",
        "49156,tcp,1",
        "49157,tcp,1",
        "49158,tcp,1",
        "80,tcp,1",
        "1024,tcp,1",
        "443,tcp,1",
        "23,tcp,1",
        "25,tcp,1",
        "110,tcp,1",
        "993,tcp,1",
        "143,tcp,1"
    }

    for line in expected_ports:
        assert line in port_proto_lines, f"Missing port/protocol line: {line}"

    print("Good job ✅✅✅ — All tests passed!")

if __name__ == "__main__":
    test_outputs()