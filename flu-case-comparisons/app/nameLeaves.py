import click
import json
import treebase

def make_rename(meta, clademap):
    def rename(accession):
        clade = clademap[accession]
        length = meta[accession]["GBSeq_length"]
        return f"{clade}|{accession}|{length}" 
    return rename


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.argument('TREEFILE', type=click.Path(exists=True), metavar = "TREEFILE")
@click.argument('METAFILE', type=click.Path(exists=True), metavar = "METAFILE")
@click.argument('CLADEFILE', type=click.Path(exists=True), metavar = "CLADEFILE")
def cli(treefile, metafile, cladefile):
    tree = treebase.readTree(treefile) 
    
    with open(metafile, "r") as fh:
        meta = json.load(fh)

    clademap = dict()
    with open(cladefile, "r") as fh:
        for line in fh.readlines():
            line = line.strip()
            (key,val) = line.split("\t")
            clademap[key] = val

    rename = make_rename(meta, clademap)
    namedTree = treebase.mapLeafSFSS(rename, tree)

    newick = treebase.writeTreeStr(namedTree)

    print(newick + ";")

        
if __name__ == '__main__':
    cli()
