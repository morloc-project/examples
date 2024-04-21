import sys
import json
from pathlib import Path

from retrieveFlu.retrieve import retrieve_records

def main(config, output_dir):

    # retrieve sequence and metadata for all search strains and references
    # this function call 
    records = retrieve_records(config)

    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Write fasta file
    with open(f"{output_dir}/sequence.fasta", "w") as fh:
        for strain in records:
            print(f'>{strain["accession"]}\n{strain["sequence"]}', file=fh)

    # Write metadata file
    with open(f"{output_dir}/metadata.json", "w") as fh:
        meta = {s["accession"] : s["meta"] for s in records} 
        print(json.dumps(meta, indent=2), file=fh)


if __name__ == '__main__':
    """
    When run as an standalone application, this program will take a config file
    and produce two files
    """

    config_file = sys.argv[1]
    output_dir = sys.argv[2]

    with open(sys.argv[1], "r") as fh:
        config = json.loads(fh.read())
        main(config, output_dir)
