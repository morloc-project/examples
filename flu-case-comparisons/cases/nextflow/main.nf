params.query = "Influenza+A+Virus[Organism]+H3N2[ALL]+HA[ALL]"
params.mindate = "2021/01/01"
params.maxdate = "2021/01/14"
params.email = "wena@mailinator.com"
params.reffile = "/case/test-data/refs.txt"

process retrieve_data {
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

process make_tree {
    input:
    path tree
    
    output:
    path "unlabeled_tree.newick"
    
    script:
    """
    tree upgma -k 8 $tree > "unlabeled_tree.newick"
    """
}

process classify {
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

process name_leaves {
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

process plot {
    publishDir "results", mode: "copy", overwrite: true

    input:
    path labeled_tree
    
    output:
    path "tree.pdf"
    
    script:
    template "plotTree.R"
}

workflow {

    retrieve_data(params.reffile)

    tree = make_tree(retrieve_data.out[1])

    class_table = classify(tree, params.reffile)

    labeled_tree = name_leaves(tree, retrieve_data.out[0], class_table)

    treeplot = plot(labeled_tree)
}
