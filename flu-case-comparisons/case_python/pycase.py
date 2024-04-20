import rooted_tree as tree
import retrieveFlu as retrieve
import sys

treefile="z.newick"

config =  { "mindate" : "2021/01/01"
          , "maxdate" : "2021/01/14"
          , "reffile" : "../test-data/refs.txt"
          , "treefile" : "tree.pdf"
          , "email" : "zbwrnz@gmail.com"
          , "query" : "Influenza+A+Virus[Organism]+H3N2[ALL]+HA[ALL]"
          }


def make_setLeafName(records):

    def setLeafName(leaf):
        (clade, index) = leaf
        return ( clade + "|" +
                 records[index]["accession"] + "|" +
                 records[index]["meta"]["GBSeq_length"]
               )
    
    return setLeafName


def make_refmap(records, reffile):
    acc2clade = dict()
    with open(reffile, "r") as fh:
        for line in fh.readlines():
            (acc, clade) = line.strip().split("\t")
            acc2clade[acc] = clade;
    refmap = []
    for record in records:
        refacc = record["accession"]
        if refacc in acc2clade:
            refmap.append(acc2clade[refacc])
        else:
            refmap.append("")
    return refmap

if __name__ == '__main__':
    # list of dictionaries with the keys:
    #  * accession
    #  * sequence
    #  * clade
    #  * meta
    print("Retrieving data from entrez", file=sys.stderr)
    records = retrieve.retrieve_records(config)

    # Make the UPGMA tree
    # upgmaTree :: RootedTree Int double Int

    print("Making UPGMA tree", file=sys.stderr)
    upgmaTree = tree.makeTree(4, [x["sequence"] for x in records]) 

    refmap = make_refmap(records, config["reffile"])

    print("Classifying leaves", file=sys.stderr)
    # Assign classifications to all leaves
    classTree = tree.classify(refmap, upgmaTree)

    setLeafName = make_setLeafName(records)

    print("Setting names", file=sys.stderr)
    # make leaf labels
    labeledTree = tree.mapLeaf(setLeafName, classTree)

    print(f"Writing file tree to {treefile}", file=sys.stderr)
    tree.writeTree(labeledTree, treefile)

    # rpy2
    # call R plotting code
