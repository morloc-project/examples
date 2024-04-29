#!/usr/bin/env bash

nameLeaves="scripts/nameLeaves.py"
plot="scripts/plotTree.R"

# write two files into output directory 01-*
#  1. sequence.fasta - retireved sequences with accessions in headers
#  2. metadata.json - JSON list wth accession keys and entrez objects values
mkdir -p 01-retrieved-data
retrieveFlu \
 --mindate "2021/01/01" \
 --maxdate "2021/01/14" \
 --email "wena@mailinator.com" \
 --query "Influenza+A+Virus[Organism]+H3N2[ALL]+HA[ALL]" \
 "../../test-data/refs.txt" \
 "01-retrieved-data"

# Build a tree with accessions on the labels
mkdir -p 02-unclassified-tree
tree upgma -k 8 01-retrieved-data/sequence.fasta > 02-unclassified-tree/tree.newick

mkdir -p 03-classifications
tree classify 02-unclassified-tree/tree.newick ../../test-data/refs.txt > 03-classifications/class-table.txt

# label leafs using classification table and metadata
mkdir -p 04-named-tree
python3 \
  $nameLeaves \
  02-unclassified-tree/tree.newick \
  01-retrieved-data/metadata.json \
  03-classifications/class-table.txt > 04-named-tree/tree.newick

# call R plotting function
mkdir -p 05-plot
Rscript $plot 04-named-tree/tree.newick 05-plot/tree.pdf
