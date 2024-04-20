import sys
import requests
from Bio import Entrez 
import time

def search_entrez(config, query):
    """
    example:
        config = dict(db="nuccore", retmax=20, mindate="2021/01/01", maxdate="2021/12/31")
        query = "Influenza+A+Virus[Organism]+H5N1"
        result = search_entrez(config, query)
    """
    base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": config["db"],
        "term": query,
        "retmode": "json",
        "retmax": str(config["retmax"]),
        "datetype": "pdat",
        "mindate": config["mindate"],
        "maxdate": config["maxdate"],
        "idtype": "acc",
    }

    result = dict()

    req = requests.get(base, params=params)
    result = req.json()["esearchresult"]

    return result["idlist"]

def get_nucleotide_accession_data(config, gb_ids):
    """
    Lookup json metadata for a list of ids in entrez.
    """

    print(f"retrieving {len(gb_ids)} ids", file=sys.stderr)

    Entrez.email = config["email"]

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
            print(str(config), file=sys.stderr)
            print(str(gb_ids), file=sys.stderr)
            time.sleep(15)

    if success:
        return(records)
    else:
        raise ValueError("Failed to retrieve ids")
