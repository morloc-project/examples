import sys
import click


def plotTree(filename, tree):
    """
    Send a RootedTree object to R for plotting

    @param filename Name of the pdf with the tree plot
    @param tree RootedTree object

    @return Nothing
    """

    # These are imported within this function to avoid the costs of importing
    # the modules unnecessarily when the plotting step is not run. For example,
    # when just the usage statement is requested. Plotting is a rather heavy
    # step that is unlikely to ever be run in an inner loop, so the cost of
    # placing the interop code inside this function should be minimal.

    import rpy2.robjects.packages as rpackages
    import rpy2.rinterface as ri
    from rpy2.robjects.conversion import Converter
    from rpy2.robjects import default_converter
    import rooted_tree as rt

    #### Set up handling for converting Py/C++ tree object to R phylo objects
    flutree = rpackages.importr('flutree')

    def rooted_tree_conversion(tree):
        """
        Handle conversion from a RootedTree<string,double,string> object to an unpacked R tree

        The return value is an R list of three elements:
          1) a character vector of node names
          2) an edge map represented by a list of 3-element lists (parent node index, child index, branch length)
          3) a character vector of leaf names
        """
        (leafs, edges, nodes) = rt.unpack(tree)
        rleafs = ri.StrSexpVector(leafs)
        redges = ri.ListSexpVector([ri.ListSexpVector([ri.IntSexpVector([i]), ri.IntSexpVector([j]), ri.FloatSexpVector([e])])  for (i,j,e) in edges])
        rnodes = ri.StrSexpVector(nodes)
        return (ri.ListSexpVector([rleafs, redges, rnodes]))

    tree_converter = Converter('tree converter')
    tree_converter.py2rpy.register(rt.RootedTreeSFS, rooted_tree_conversion)

    extended_converter = tree_converter + default_converter

    with extended_converter.context():
        phylo_obj = flutree.pack(tree)
        flutree.plotTree(filename, phylo_obj)


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

def run(config):
    import rooted_tree as rt
    import retrieveFlu as retrieve

    # list of dictionaries with the keys:
    #  * accession
    #  * sequence
    #  * clade
    #  * meta
    print("Python: retrieving data from entrez", file=sys.stderr)
    records = retrieve.retrieve_records(config)

    print("Py to C++: making UPGMA tree", file=sys.stderr)
    upgmaTree = rt.makeTree(4, [x["sequence"] for x in records]) 

    print("Py to C++: classifying leaves", file=sys.stderr)
    classTree = rt.classify(make_refmap(records, config["reffile"]), upgmaTree)

    print("Py to C++/Py: setting leaf names", file=sys.stderr)
    labeledTree = rt.mapLeaf(make_setLeafName(records), classTree)

    print(f'''Py to C++: writing file tree to {config["treefile"]}''', file=sys.stderr)
    rt.writeTree(labeledTree, config["treefile"])

    print(f'''Py to R: plotting the tree to {config["plotfile"]}''', file=sys.stderr)
    plotTree(config["plotfile"], labeledTree)


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.argument('REFFILE', type=click.Path(exists=True), metavar = "REFFILE")
@click.option('--mindate', default="2021/01/01", type=str, help='Minimum date (default: 2021/01/01)')
@click.option('--maxdate', default="2021/01/14", type=str, help='Maximum date (default: 2021/01/14)')
@click.option('--plotfile', default="tree.pdf", type=click.Path(), help='Plot file (default: tree.pdf)')
@click.option('--treefile', default="tree.newick", type=click.Path(), help='Tree file (default: tree.newick)')
@click.option('--email', default="wena@mailinator.com", type=str, help='Email (default: wena@mailinator.com)')
@click.option('--query', default="Influenza+A+Virus[Organism]+H3N2[ALL]+HA[ALL]", type=str, help='Query (default: Influenza+A+Virus[Organism]+H3N2[ALL]+HA[ALL])')
def cli(reffile, mindate, maxdate, plotfile, treefile, email, query):
    """
    Build a tree for queried strains and classify using a reference file

    REFFILE: Path to the reference file. TAB-delimited, headerless file with two columns: accession and clade.
    """
    config = {
        "mindate": mindate,
        "maxdate": maxdate,
        "reffile": reffile,
        "plotfile": plotfile,
        "treefile": treefile,
        "email": email,
        "query": query
    }

    run(config)

if __name__ == '__main__':
    cli()
