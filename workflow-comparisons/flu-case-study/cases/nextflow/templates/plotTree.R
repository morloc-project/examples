#!/usr/bin/env Rscript

flutree::plotTree("tree.pdf", ape::read.tree("${labeled_tree}"))
