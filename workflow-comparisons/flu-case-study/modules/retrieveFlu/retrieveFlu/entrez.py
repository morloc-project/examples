import sys
import requests
from Bio import Entrez 
import time

def search_entrez(query, mindate, maxdate, db = "nuccore", retmax = 1000):
    base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": db,
        "term": query,
        "retmode": "json",
        "retmax": str(retmax),
        "datetype": "pdat",
        "mindate": mindate,
        "maxdate": maxdate,
        "idtype": "acc",
    }

    result = dict()

    req = requests.get(base, params=params)
    result = req.json()["esearchresult"]

    return result["idlist"]

def get_nucleotide_accession_data(gb_ids, email):
    """
    Lookup json metadata for a list of ids in entrez.
    """

    print(f"  retrieving {len(gb_ids)} ids", file=sys.stderr)

    Entrez.email = email

    records = []
    success = False

    attempt = 0
    while attempt < 5:
        try:
            recordsXml = Entrez.efetch(db="nucleotide", id=gb_ids, retmode="xml") 
            records = Entrez.read(recordsXml) # a list of dictionaries
            recordsXml.close()
            success = True
            break
        except Exception as err:
            attempt += 1
            print(f"Received error from server {err}", file=sys.stderr)
            print(f"Attempt {str(attempt)} of 5 attempts", file=sys.stderr)
            print(str(gb_ids), file=sys.stderr)
            time.sleep(15)

    if success:
        return(records)
    else:
        raise ValueError("Failed to retrieve ids")
