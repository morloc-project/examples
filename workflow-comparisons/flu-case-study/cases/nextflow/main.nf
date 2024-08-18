params.query = "Influenza+A+Virus[Organism]+H3N2[ALL]+HA[ALL]"
params.mindate = "2021/01/01"
params.maxdate = "2021/01/14"
params.email = "wena@mailinator.com"
params.reffile = "/workflow-comparisons/test-data/refs.txt"

process RETRIEVE_DATA {
    input:
    val reffile
    
    output:
    path "01-retrieved-data/metadata.json", emit: metadata
    path "01-retrieved-data/sequence.fasta", emit: sequence
    
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
    path "labeled_tree.newick"
    
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

    ch_tree = MAKE_TREE(RETRIEVE_DATA.out.sequence)

    ch_class_table = CLASSIFY(ch_tree, params.reffile)

    ch_treeplot = NAME_LEAVES(ch_tree, RETRIEVE_DATA.out.metadata, ch_class_table)
    | PLOT
}
