import click
import treebase

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])

def read_fasta(fasta_fh):
    entries = []
    header = None
    seqs = []
    for line in fasta_fh.readlines():
        line = line.strip()
        if line[0] == ">":
            if not (header is None):
                entries.append((header, "".join(seqs)))
                seqs = []
            header = line[1:]
        else:
            seqs.append(line)
    if not (header is None):
        entries.append((header, "".join(seqs)))
    return entries
                
def make_setLeafName(pairmap):
    def setLeafName(key):
        return pairmap[key]
    return setLeafName

def tree_from_fasta(entries, k=8):
    headers = [x[0] for x in entries]
    seqs = [x[1] for x in entries]
    upgma_tree = treebase.makeTree(k, seqs)
    named_tree = treebase.mapLeaf(make_setLeafName(headers), upgma_tree)
    return named_tree


@click.group(
    help="Simple tree functions",
    context_settings=CONTEXT_SETTINGS,
)
def main():
    pass

@click.command(name="upgma")
@click.argument("FASTA", type=click.Path(exists=True))
@click.option("-k", type=int, default=8, help="k-mer length for distance calculation")
def upgma_cmd(fasta, k=8):

    with open(fasta, "r") as fasta_fh:
        entries = read_fasta(fasta_fh)

        upgma_tree = tree_from_fasta(entries, k=k)

        treebase.writeTree(upgma_tree, "/dev/stdout")

def readMap(filename):
    pair = dict()
    with open(filename, "r") as fh:
        for line in fh.readlines():
            line = line.strip()
            (key, val) = line.split("\t")
            pair[key] = val
    return pair


@click.command(name="classify")
@click.argument("TREEFILE", type=click.Path(exists=True))
@click.argument("REFFILE", type=click.Path(exists=True))
def classify_cmd(treefile="02-unclassified-tree/tree.newick", reffile="../../test-data/refs.txt"):
    """
    Classify each leaf in a tree given a reference file
    """

    # RootedTree Str Float Str
    tree = treebase.readTree(treefile)

    # extract all leaves from tree
    leafs = treebase.getLeafs(tree)

    # map leaves to indices
    leafIndexMap = {name : index for (index, name) in enumerate(leafs)} 

    # map indices to tree
    index_tree = treebase.mapLeaf(make_setLeafName(leafIndexMap), tree)

    # classify with refmap
    refmap = readMap(reffile)
    refmap_vector = []
    for k in leafs:
        if k in refmap:
            refmap_vector.append(refmap[k])
        else:
            refmap_vector.append("")
    clade_tree = treebase.classify(refmap_vector, index_tree)

    clade_leafs = treebase.getLeafs(clade_tree)
    for (clade, index) in clade_leafs:
        print(f"{leafs[index]}\t{clade}")

main.add_command(upgma_cmd)
main.add_command(classify_cmd)
