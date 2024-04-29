#!/usr/bin/python3

import json
import treebase

def make_rename(meta, clademap):
    def rename(accession):
        clade = clademap[accession]
        length = meta[accession]["GBSeq_length"]
        return f"{clade}|{accession}|{length}" 
    return rename

tree = treebase.readTree("${unlabeled_tree}") 

with open("${metadata}", "r") as fh:
    meta = json.load(fh)

clademap = dict()
with open("${class_table}", "r") as fh:
    for line in fh.readlines():
        line = line.strip()
        (key,val) = line.split("\t")
        clademap[key] = val

rename = make_rename(meta, clademap)
namedTree = treebase.mapLeafSFSS(rename, tree)

newick = treebase.writeTreeStr(namedTree)

with open("labeled_tree.newick", "w") as fh:
    print(newick + ";", file=fh)
