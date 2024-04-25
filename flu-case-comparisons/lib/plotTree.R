#!/usr/bin/env Rscript

args <- commandArgs(trailingOnly = TRUE)

# Check if the correct number of arguments are provided
if (length(args) != 2) {
  stop("Usage: plot_tree.R <treefile> <plotfile>")
}

# Get the file paths
treefile <- args[1]
plotfile <- args[2]

# Read tree and plot
flutree::plotTree(plotfile, ape::read.tree(treefile))
