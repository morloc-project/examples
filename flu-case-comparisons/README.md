# Comparison of morloc versus other approaches

This repository contains six implementations of the influenza case study
presented in the first morloc paper.

## Setup

These examples may be run on Linux or Mac.

First create a Docker image that contains everything needed to run all of the
comparisons (morloc, pybind11 for Python/C++ interop, nextflow, snakemake, etc):

```
make build
```

Then enter the container shell:

```
make shell
```

This mounts the current working directory into the container as a virtual
volume. This means that from within the container you may alter this folder and
the changes will persist on your machine, but no other changes (installed
programs, for instance) will be visible.


## Six case study implementations

The `cases` folder contains six implementations of the influenza case
study. Each case study may be run by entering the respective directory and
calling `make`. Results may be removed by calling `make clean`.

Each folder has their own local copy of the required `refs.txt` file that
contains the map from strain accession id to clade.

## python

Run a python program with C++ (through `pybind11`) and R interop (through
`rpy2`).

This program uses the following packages (all defined in the `modules` folder):
 * `treebase` - A python package wrapping C++ code for tree manipulation
   using `pybind11` for interop.
 * `retrieveFlu` - A pure python package for retrieving influenza data
 * `flutree` - An R package for plotting trees


## bash

Run the shell script `flu.sh`. Five steps are executed with the scripts below:

 * retrieveFlu - locally installed pure python program
 * tree upgma - locally installed python program that wraps C++ code
 * tree classify - as above, different subcommand
 * scripts/nameLeaves.py - python script with minimal CLI interface
 * scripts/plotTree.R - R script with minimal CLI interface

## snakemake

Uses the same executables as bash (`retrieveFlu` and `tree`) but replaces the
scripts `nameLeaves.py` and `plotTree.R` with simplified Python and R scripts
that use implicit `snakemake` objects. These scripts are simplified since they
require no CLI, but they are tailored to `snakemake` and cannot be tested
independently of it.

Snakemake scripts:
 * retrieveFlu - see bash
 * tree upgma - see bash
 * tree classify - see bash
 * scripts/renamer.py - python script with implicitly passed Snakemake object
 * scripts/plot.R - R script with implicitly passed Snakemake object

## nextflow

Similar to Snakemake.

nextflow scripts:
 * retrieveFlu - see bash
 * tree upgma - see bash
 * tree classify - see bash
 * templates/renamer.py - Python script with nextflow variables interpolated
 * templates/plot.R - R script with nextflow variables interpolated

## morloc

The morloc case study as described in the paper

## hybrid

A Snakemake workflow that uses morloc generated executables for each step.
