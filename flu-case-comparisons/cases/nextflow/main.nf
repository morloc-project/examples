params.query = "Influenza+A+Virus[Organism]+H3N2[ALL]+HA[ALL]"
params.mindate = "2021/01/01"
params.maxdate = "2021/01/14"
params.email = "wena@mailinator.com"
params.reffile = "/case/test-data/refs.txt"

process RETRIEVE_DATA {
    input:
    val reffile
    
    output:
    path "01-retrieved-data/metadata.json"
    path "01-retrieved-data/sequence.fasta"
    
    script:
    """
    retrieveFlu \
       --mindate "${params.mindate}" \
       --maxdate "${params.maxdate}" \
       --email "${params.email}" \
       --query "${params.query}" \
       "$reffile" \
       "01-retrieved-data"
    """
}

process MAKE_TREE {
    input:
    path tree
    
    output:
    path "unlabeled_tree.newick"
    
    script:
    """
    tree upgma -k 8 $tree > "unlabeled_tree.newick"
    """
}

process CLASSIFY {
    input:
    path tree
    path reffile
    
    output:
    path "class_table.tab"
    
    script:
    """
    tree classify "$tree" "$reffile" > "class_table.tab"
    """
}

process NAME_LEAVES {
    publishDir "results", mode: "copy", overwrite: true

    input:
    path unlabeled_tree
    path metadata
    path class_table
    
    output:
    path "labeled_tree.newick", emit: labeled_tree
    
    script:
    template "nameLeaves.py"
}

process PLOT {
    publishDir "results", mode: "copy", overwrite: true

    input:
    path labeled_tree
    
    output:
    path "tree.pdf"
    
    script:
    template "plotTree.R"
}

workflow {

    RETRIEVE_DATA(params.reffile)

    tree = MAKE_TREE(RETRIEVE_DATA.out[1])

    class_table = CLASSIFY(tree, params.reffile)

    labeled_tree = NAME_LEAVES(tree, RETRIEVE_DATA.out[0], class_table)

    treeplot = PLOT(labeled_tree)
}
