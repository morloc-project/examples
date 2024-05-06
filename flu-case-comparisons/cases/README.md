Here I implement 6 versions of the flu case study.

Each case study may be run by entering the respective directory and running
`make`. Results may be removed by running `make clean`. See the Makefile for
each project to find the execution command.

Each folder has their own local copy of the required `refs.txt` file.

## python

Run a python program with C++ (through `pybind11`) and R interop (through
`rpy2`). The C++ code is all wrapped in the python module `treebase`, which is
defined in `case/modules/treebase`.

## bash

Run the shell script `flu.sh`. Five steps are executed with the scripts below:

   - retrieveFlu - locally installed pure python program
   - tree upgma - locally installed python program that wraps C++ code
   - tree classify - as above, different subcommand
   - scripts/nameLeaves.py - python script with minimal CLI interface
   - scripts/plotTree.R - R script with minimal CLI interface

## snakemake

Uses the same executables as bash (`retrieveFlu` and `tree`) but replaces the
scripts `nameLeaves.py` and `plotTree.R` with simplified Python and R scripts
that use implicit `snakemake` objects. These scripts are simplified since they
require no CLI, but they are tailored to `snakemake` and cannot be tested
independently of it.

Snakemake scripts:
   - retrieveFlu - see bash
   - tree upgma - see bash
   - tree classify - see bash
   - scripts/renamer.py - python script with implicitly passed Snakemake object
   - scripts/plot.R - R script with implicitly passed Snakemake object

## nextflow

Similar to Snakemake.

nextflow scripts:
   - retrieveFlu - see bash
   - tree upgma - see bash
   - tree classify - see bash
   - templates/renamer.py - Python script with nextflow variables interpolated
   - templates/plot.R - R script with nextflow variables interpolated

## morloc

The morloc case study as described in the paper

## hybrid

A Snakemake workflow that uses morloc generated executables for each step.
