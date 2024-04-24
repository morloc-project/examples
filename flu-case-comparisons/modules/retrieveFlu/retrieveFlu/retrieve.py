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
def retrieve_records(reffile, mindate, maxdate, email, query):
    refmap = read_references(reffile)

    query_ids = search_entrez(
        query
      , mindate = mindate
      , maxdate = maxdate
      , db = "nuccore"
      , retmax = 1000
    )

    ids = list(refmap.keys()) + query_ids 

    chunkSize=30
    records = []

    for i in range(0, len(ids) - 1, chunkSize):
        idsChunk = ids[i:i+chunkSize]
        for record in get_nucleotide_accession_data(idsChunk, email=email):
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
