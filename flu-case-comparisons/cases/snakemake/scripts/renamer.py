import json
import treebase

def make_rename(meta, clademap):
    def rename(accession):
        clade = clademap[accession]
        length = meta[accession]["GBSeq_length"]
        return f"{clade}|{accession}|{length}" 
    return rename

def make_renamed_file(treefile, metafile, cladefile, outfile):
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

    with open(outfile, "w") as fh:
        print(newick + ";", file=fh)

make_renamed_file(
    treefile = snakemake.input[0],
    metafile = snakemake.input[1],
    cladefile = snakemake.input[2],
    outfile=snakemake.output[0]
)
