import time
import sys
from retrieveFlu.entrez import search_entrez, get_nucleotide_accession_data

def read_references(reffile):
    with open(reffile, "r") as fh:
        refmap = dict()
        for line in fh.readlines():
            try:
                (k, v) = line.strip().split("\t")
                refmap[k] = v
            except:
                sys.exit(f'''Failed to read file {reffile}: expected TAB delimited key/val columns, found "{line}"''')
    return refmap

# This function contains the same basic logic as the `searchEntrez` function in the morloc script
def retrieve_records(config):
    search_config = dict(
        email = config["email"]
      , db = "nuccore"
      , mindate = config["mindate"]
      , maxdate = config["maxdate"]
      , retmax = 1000
      )
    fetch_config = dict( email = config["email"] )
    refmap = read_references(config["reffile"])

    ids = list(refmap.keys()) + search_entrez(search_config, config["query"])

    chunkSize=30
    records = []

    for i in range(0, len(ids) - 1, chunkSize):
        idsChunk = ids[i:i+chunkSize]
        for record in get_nucleotide_accession_data(fetch_config, idsChunk):
            sequence = record["GBSeq_sequence"].upper() 
            accession = record["GBSeq_primary-accession"]
            del record["GBSeq_sequence"]
            del record["GBSeq_primary-accession"]

            if accession in refmap:
                clade = refmap[accession]
            else:
                clade = None

            records.append(
                { "accession" : accession
                , "sequence" : sequence
                , "clade" : clade
                , "meta" : record
                }
            )
        time.sleep(1)

    return records
