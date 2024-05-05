#!/usr/bin/env bash

set +eu

nameLeaves="scripts/nameLeaves.py"
plot="scripts/plotTree.R"

function log () {
  echo $1 > /dev/stderr
}


# write two files into output directory 01-*
#  1. sequence.fasta - retireved sequences with accessions in headers
#  2. metadata.json - JSON list wth accession keys and entrez objects values
dir1="01-retrieved-data"
log "Retrieving data from entrez"
log "- creating $dir1"
mkdir -p $dir1 
# if the data already exists, reuse it
if [[ -s $dir1/metadata.json && -s $dir1/sequence.fasta ]]
then
  log "- retrieved data already exists, reusing"
else
  log "- calling 'retrieveFlu' Python script"
  retrieveFlu \
   --mindate "2021/01/01" \
   --maxdate "2021/01/14" \
   --email "wena@mailinator.com" \
   --query "Influenza+A+Virus[Organism]+H3N2[ALL]+HA[ALL]" \
   "../../test-data/refs.txt" \
   $dir1
fi

dir2="02-unclassified-tree"
log "Building a phylogenetic tree"
log "- creating $dir2"
log "- calling 'tree upgma' Python script"
# Build a tree with accessions on the labels
mkdir -p $dir2
tree upgma -k 8 $dir1/sequence.fasta > $dir2/tree.newick

dir3="03-classifications"
log "Classifying taxa"
log "- creating $dir3"
log "- calling 'tree classify' Python script"
mkdir -p $dir3
tree classify ${dir2}/tree.newick ../../test-data/refs.txt > ${dir3}/class-table.txt

dir4="04-named-tree"
log "Labeling leafs using classification table and metadata"
log "- creating $dir4"
log "- calling '${nameLeaves}' Python script"
mkdir -p $dir4
python3 \
  $nameLeaves \
  $dir2/tree.newick \
  $dir1/metadata.json \
  $dir3/class-table.txt > $dir4/tree.newick

dir5="05-plot"
log "- creating $dir5"
log "- calling '${plot}' R script"
log "Plotting the final tree"
mkdir -p $dir5
Rscript $plot $dir4/tree.newick $dir5/tree.pdf
