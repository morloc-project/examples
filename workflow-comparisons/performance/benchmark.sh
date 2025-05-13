#!/usr/bin/env bash

set -eu

W=5
NODES="0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16"
LOG8="1,2,4,8,16,32,64,128,256"

MORLOC_VERSION=$(morloc --version)

NODES_SIZES=""
STATFILE=$PWD/stats.csv
TEMP=temp-results
EMPTY=test-data-00MB.txt

>$EMPTY
#>$STATFILE

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

##### SINGLE-LANGUAGE TESTS #####

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
  "python3 main.py {node} ../${EMPTY}"
cat $TEMP >> $STATFILE && rm $TEMP

hyperfine \
  -w $W \
  -L node $NODES \
  -L size 0 \
  -L mode testlc \
  -L lang R \
  --export-csv $TEMP \
  "Rscript --vanilla main.R {node} ../${EMPTY}"
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
  -L node 20 \
  -L size $NODES \
  -L mode testlc \
  -L lang python \
  --export-csv $TEMP \
  "python3 main.py {node} ../test-data-{size}0MB.txt"
cat $TEMP >> $STATFILE && rm $TEMP

hyperfine \
  -w $W \
  -L node 20 \
  -L size $NODES \
  -L mode testlc \
  -L lang R \
  --export-csv $TEMP \
  "Rscript --vanilla main.R {node} ../test-data-{size}0MB.txt"
cat $TEMP >> $STATFILE && rm $TEMP

hyperfine \
  -w $W \
  -L node 20 \
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
  "python3 main.py {node} ../test-data-{size}0MB.txt"
cat $TEMP >> $STATFILE && rm $TEMP

hyperfine \
  -w $W \
  -L node 0 \
  -L size $NODES \
  -L mode loading \
  -L lang R \
  --export-csv $TEMP \
  "Rscript --vanilla main.R {node} ../test-data-{size}0MB.txt"
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

echo "Test R"
echo "Morloc linear cis, log2 iterations, size = 0"
hyperfine \
  -w $W \
  -L node 1,2,4,8,16,32,64,128,256,512,1024,2048,4096,8192 \
  -L size 0 \
  -L mode pr,cr \
  -L lang morloc \
  --export-csv $TEMP \
  "./nexus {mode} {node} '$(echo '"../test-data-00MB.txt"')'"
cat $TEMP >> $STATFILE && rm $TEMP

echo "Test Python"
echo "Morloc linear cis, log2 iterations, size = 0"
hyperfine \
  -w $W \
  -L node 1,2,4,8,16,32,64,128,256,512,1024,2048,4096,8192,16384,32768,65536,131072,262144 \
  -L size 0 \
  -L mode cp,rp \
  -L lang morloc \
  --export-csv $TEMP \
  "./nexus {mode} {node} '$(echo '"../test-data-00MB.txt"')'"
cat $TEMP >> $STATFILE && rm $TEMP

echo "Test to C"
echo "Morloc linear cis, log2 iterations, size = 0"
hyperfine \
  -w $W \
  -L node 1,2,4,8,16,32,64,128,256,512,1024,2048,4096,8192,16384,32768,65536,131072,262144,524288 \
  -L size 0 \
  -L mode pc,rc \
  -L lang morloc \
  --export-csv $TEMP \
  "./nexus {mode} {node} '$(echo '"../test-data-00MB.txt"')'"
cat $TEMP >> $STATFILE && rm $TEMP

echo "Test C to C"
echo "Morloc linear cis, log2 iterations, size = 0"
hyperfine \
  -w $W \
  -L node 1,2,4,8,16,32,64,128,256,512,1024,2048,4096,8192,16384,32768,65536,131072,262144,524288,1048576,2097152,4194304,8388608,16777216,33554432,67108864,134217728,268435456,536870912,1073741824,2147483647 \
  -L size 0 \
  -L mode cc \
  -L lang morloc \
  --export-csv $TEMP \
  "./nexus {mode} {node} '$(echo '"../test-data-00MB.txt"')'"
cat $TEMP >> $STATFILE && rm $TEMP

echo "Test Py to Py"
echo "Morloc linear cis, log2 iterations, size = 0"
hyperfine \
  -w $W \
  -L node 1,2,4,8,16,32,64,128,256,512,1024,2048,4096,8192,16384,32768,65536,131072,262144,524288,1048576,2097152,4194304,8388608,16777216,33554432,67108864,134217728 \
  -L size 0 \
  -L mode pp \
  -L lang morloc \
  --export-csv $TEMP \
  "./nexus {mode} {node} '$(echo '"../test-data-00MB.txt"')'"
cat $TEMP >> $STATFILE && rm $TEMP

echo "Test R to R"
echo "Morloc linear cis, log2 iterations, size = 0"
hyperfine \
  -w $W \
  -L node 1,2,4,8,16,32,64,128,256,512,1024,2048,4096,8192,16384,32768,65536,131072,262144,524288,1048576,2097152,4194304,8388608 \
  -L size 0 \
  -L mode rr \
  -L lang morloc \
  --export-csv $TEMP \
  "./nexus {mode} {node} '$(echo '"../test-data-00MB.txt"')'"
cat $TEMP >> $STATFILE && rm $TEMP


# -L mode pp,pr,pc,rp,rr,rc,cp,cr,cc \
echo "Morloc linear, size = n"
hyperfine \
 -w $W \
 -L node 3 \
 -L size $NODES \
 -L mode pp,pc,cp,cc \
 -L lang morloc \
 --export-csv $TEMP \
 "./nexus {mode} {node} '$(echo '"../test-data-{size}0MB.txt"')'"
cat $TEMP >> $STATFILE && rm $TEMP

cd ..

##### SNAKEMAKE PERFORMANCE TEST #####

cd snakemake

echo "Snakemake linear cis, size = 0"
hyperfine \
  -w $W \
  -p "make clean" \
  -L node 1,2,4,8,16,32,64,128,256 \
  -L size 0 \
  -L mode testlc,testlt \
  -L lang snakemake \
  --show-output \
  --export-csv $TEMP \
  "snakemake -c1 --config nnodes={node} inputfile=../${EMPTY} -- {mode}"
cat $TEMP >> $STATFILE && rm $TEMP

echo "Snakemake linear cis, size = n"
hyperfine \
  -w $W \
  -p "make clean" \
  -L node 3 \
  -L size $NODES \
  -L mode testlc \
  -L lang snakemake \
  --export-csv $TEMP \
  "snakemake -c1 --config nnodes={node} inputfile=../test-data-{size}0MB.txt  -- {mode}"
cat $TEMP >> $STATFILE && rm $TEMP

cd ..


###### NEXTFLOW PERFORMANCE TEST ####

echo "Nextflow linear cis, size = 0"
cd nextflow
make deepclean
cp ../test-data* .

# The expand.py script adds a new linear node to the pipeline
for nnodes in 1 2 4 8 16 32 64 128 256 512 1024
do
  cat template.nf > main.nf
  for i in `seq 1 $nnodes`; do python3 expand.py; done

  hyperfine \
    -w $W \
    -p "make clean && sleep 1"  \
    -L node $nnodes  \
    -L size 0  \
    -L mode testlc  \
    -L lang nextflow  \
    --export-csv $TEMP  \
    "nextflow run main.nf --input=${EMPTY} --outdir=results"
  cat $TEMP >> $STATFILE && rm $TEMP
done

cat template.nf > main.nf
python3 expand.py
python3 expand.py
python3 expand.py

hyperfine \
  -w $W \
  -p "make clean && sleep 1" \
  -L node 3 \
  -L size $NODES \
  -L mode testlc \
  -L lang nextflow \
  --export-csv $TEMP \
  "nextflow run main.nf --input=test-data-{size}0MB.txt --outdir=results"
cat $TEMP >> $STATFILE && rm $TEMP

make deepclean

cd ..

##### Cleanup #####

# each benchmarking run writes the same header to stats.csv, so here we need to
# pull out a single one and write it to the beginning of our fial stats file
grep "command,mean" stats.csv | head -1 > stats-$MORLOC_VERSION.csv
# then write all the results minus the header
grep -v "command,mean" stats.csv >> stats-$MORLOC_VERSION.csv
# and make it read only
chmod 400 stats-$MORLOC_VERSION.csv
