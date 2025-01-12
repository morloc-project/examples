#!/usr/bin/env bash

set -eu

W=3
NODES="1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16"
STATFILE=$PWD/stats.csv
TEMP=temp-results
EMPTY=test-data-empty.txt

>$EMPTY
>$STATFILE

echo "GATTAGATTAGATTAGATTAGATTAGATTAGATTAGATTAGATTAGATTAGATTAGATTAGATTAGATTAGATTAGATTAGATTAGATTAGATTAGATTA" > test-data-line.txt

>test-data-100kb.txt
for i in `seq 1 1000`
do
  cat test-data-line.txt >> test-data-100kb.txt
done

>test-data-10MB.txt
for i in `seq 1 100`
do
  cat test-data-100kb.txt >> test-data-10MB.txt
done

for i in 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
do
  for j in `seq 1 $i`
  do
    cat test-data-10MB.txt
  done > test-data-${i}0MB.txt
done

### SINGLE-LANGUAGE TESTS #####

cd single-language
make

echo "Single-language linear cis, size = 0"
hyperfine \
  -w $W \
  -L node $NODES \
  -L size 0 \
  -L mode testlc \
  -L lang python \
  --export-csv $TEMP \
  "python3 main.py --nodes {node} --inputfile ../${EMPTY}"
cat $TEMP >> $STATFILE && rm $TEMP

hyperfine \
  -w $W \
  -L node $NODES \
  -L size 0 \
  -L mode testlc \
  -L lang R \
  --export-csv $TEMP \
  "Rscript --vanilla main.R --nodes {node} --inputfile ../${EMPTY}"
cat $TEMP >> $STATFILE && rm $TEMP

hyperfine \
  -w $W \
  -L node $NODES \
  -L size 0 \
  -L mode testlc \
  -L lang C \
  --export-csv $TEMP \
  "./cmain {node} ../${EMPTY}"
cat $TEMP >> $STATFILE && rm $TEMP

echo "Single-language linear cis, size = n"
hyperfine \
  -w $W \
  -L node 4 \
  -L size $NODES \
  -L mode testlc \
  -L lang python \
  --export-csv $TEMP \
  "python3 main.py --nodes {node} --inputfile ../test-data-{size}0MB.txt"
cat $TEMP >> $STATFILE && rm $TEMP

hyperfine \
  -w $W \
  -L node 4 \
  -L size $NODES \
  -L mode testlc \
  -L lang R \
  --export-csv $TEMP \
  "Rscript --vanilla main.R --nodes {node} --inputfile ../test-data-{size}0MB.txt"
cat $TEMP >> $STATFILE && rm $TEMP

hyperfine \
  -w $W \
  -L node 4 \
  -L size $NODES \
  -L mode testlc \
  -L lang C \
  --export-csv $TEMP \
  "./cmain {node} ../test-data-{size}0MB.txt"
cat $TEMP >> $STATFILE && rm $TEMP

# Test loading times
echo "Single-language linear cis, size = n, nodes = 0"
hyperfine \
  -w $W \
  -L node 0 \
  -L size $NODES \
  -L mode loading \
  -L lang python \
  --export-csv $TEMP \
  "python3 main.py --nodes {node} --inputfile ../test-data-{size}0MB.txt"
cat $TEMP >> $STATFILE && rm $TEMP

hyperfine \
  -w $W \
  -L node 0 \
  -L size $NODES \
  -L mode loading \
  -L lang R \
  --export-csv $TEMP \
  "Rscript --vanilla main.R --nodes {node} --inputfile ../test-data-{size}0MB.txt"
cat $TEMP >> $STATFILE && rm $TEMP

hyperfine \
  -w $W \
  -L node 0 \
  -L size $NODES \
  -L mode loading \
  -L lang C \
  --export-csv $TEMP \
  "./cmain {node} ../test-data-{size}0MB.txt"
cat $TEMP >> $STATFILE && rm $TEMP


cd ..


##### MORLOC PERFORMANCE TEST #####
cd morloc
morloc make main.loc

echo "Morloc linear cis, size = 0"
hyperfine \
  -w $W \
  -L node $NODES \
  -L size 0 \
  -L mode pp,pr,pc,rp,rr,rc,cp,cr,cc \
  -L lang morloc \
  --export-csv $TEMP \
  "./nexus.py {mode} {node} '$(echo '"../test-data-empty.txt"')'"
cat $TEMP >> $STATFILE && rm $TEMP

echo "Morloc linear, size = n"
hyperfine \
 -w $W \
 -L node 4 \
 -L size $NODES \
 -L mode pp,pr,pc,rp,rr,rc,cp,cr,cc \
 -L lang morloc \
 --export-csv $TEMP \
 "./nexus.py {mode} {node} '$(echo '"../test-data-{size}0MB.txt"')'"
cat $TEMP >> $STATFILE && rm $TEMP

cd ..

##### SNAKEMAKE PERFORMANCE TEST #####

cd snakemake

echo "Snakemake linear cis, size = 0"
hyperfine \
  -w $W \
  -p "make clean" \
  -L node $NODES \
  -L size 0 \
  -L mode testlc,testlt \
  -L lang snakemake \
  --export-csv $TEMP \
  "snakemake -c1 --config nnodes={node} inputfile=../${EMPTY} -- {mode}"
cat $TEMP >> $STATFILE && rm $TEMP

echo "Snakemake linear cis, size = n"
hyperfine \
  -w $W \
  -p "make clean" \
  -L node 4 \
  -L size $NODES \
  -L mode testlc,testlt \
  -L lang snakemake \
  --export-csv $TEMP \
  "snakemake -c1 --config nnodes={node} inputfile=../test-data-{size}0MB.txt  -- {mode}"
cat $TEMP >> $STATFILE && rm $TEMP

cd ..

 
##### NEXTFLOW PERFORMANCE TEST ####

echo "Nextflow linear cis, size = 0"
cd nextflow
mv ../test-data* .
cat template.nf > main.nf

# The expand.py script adds a new linear node to the pipeline
for nnodes in `seq 1 16`
do
  python3 expand.py
  hyperfine \
    -w $W \
    -p "make clean && sleep 1"  \
    -L node $nnodes  \
    -L size 0  \
    -L mode testlc  \
    -L lang nextflow  \
    --show-output \
    --export-csv $TEMP  \
    "nextflow run main.nf --input=${EMPTY} --outdir=results"
  cat $TEMP >> $STATFILE && rm $TEMP
done

cat template.nf > main.nf
python3 expand.py
python3 expand.py
python3 expand.py
python3 expand.py

hyperfine \
  -w $W \
  -p "make clean && sleep 1" \
  -L node 4 \
  -L size $NODES \
  -L mode testlc \
  -L lang nextflow \
  --export-csv $TEMP \
  "nextflow run main.nf --input=test-data-{size}0MB.txt --outdir=results"
cat $TEMP >> $STATFILE && rm $TEMP

make deepclean

cd ..
