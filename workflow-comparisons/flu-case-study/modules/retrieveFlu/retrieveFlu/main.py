import click
import json
from pathlib import Path

from retrieveFlu.retrieve import retrieve_records

@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.argument('REFFILE', type=click.Path(exists=True), metavar = "REFFILE")
@click.argument('OUTDIR', type=click.Path(), metavar = "OUTDIR")
@click.option('--mindate', default="2021/01/01", type=str, help='Minimum date (default: 2021/01/01)')
@click.option('--maxdate', default="2021/01/14", type=str, help='Maximum date (default: 2021/01/14)')
@click.option('--email', default="wena@mailinator.com", type=str, help='Email (default: wena@mailinator.com)')
@click.option('--query', default="Influenza+A+Virus[Organism]+H3N2[ALL]+HA[ALL]", type=str, help='Query (default: Influenza+A+Virus[Organism]+H3N2[ALL]+HA[ALL])')
def main(reffile, outdir, mindate, maxdate, email, query):
    """
    Build a tree for queried strains and classify using a reference file

    REFFILE: Path to the reference file. TAB-delimited, headerless file with two columns: accession and clade.
    OUTDIR: Directory to which output should be written

    Creates the files {OUTDIR}/sequence.fasta and {OUTDIR}/metadata.json.
    """

    # retrieve sequence and metadata for all search strains and references
    # this function call 
    records = retrieve_records(
        reffile=reffile,
        mindate=mindate,
        maxdate=maxdate,
        email=email,
        query=query
    )

    Path(outdir).mkdir(parents=True, exist_ok=True)

    # Write fasta file
    with open(f"{outdir}/sequence.fasta", "w") as fh:
        for strain in records:
            print(f'>{strain["accession"]}\n{strain["sequence"]}', file=fh)

    # Write metadata file
    with open(f"{outdir}/metadata.json", "w") as fh:
        meta = {s["accession"] : s["meta"] for s in records} 
        print(json.dumps(meta, indent=2), file=fh)
