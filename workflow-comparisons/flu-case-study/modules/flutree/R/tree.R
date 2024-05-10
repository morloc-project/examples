library(ape)

# Convert an unpacked tree into a phylo object
#
# The unpacked tree has the type:
#
#   ([string], [(int, int, float)], [string])
#
# The first list of strings are leaf names
# The list of (int, int, float) tuples is the edge map and branch lengths
# The second list of strings are node names
pack <- function(x){
    nodes <- x[[1]]
    edges <- sapply(x[[2]], function(e) e[[3]])
    leafs <- x[[3]]

    edge_map <- lapply(x[[2]], function(e) { c(e[[1]], e[[2]])})
    edge_map <- do.call(rbind, edge_map)
    edge_map[,1] <- edge_map[,1] + length(leafs) + 1
    edge_map[,2] <- ifelse(edge_map[,2] < length(nodes), edge_map[,2] + length(leafs) + 1, edge_map[,2] - length(nodes) + 1)

    tree <- list()
    class(tree) <- "phylo"
    tree$edge <- edge_map
    tree$tip.label <- leafs
    tree$Nnode <- as.integer(length(nodes))
    tree$edge.length <- edges
    tree
}

plotTree <- function(outputpdffilename, tree) {
  pdf(
    outputpdffilename,
    width = 8,
    height = length(tree$tip.label) * 0.1
  )

  # Adjusts the label font size for readability
  par(cex = 0.7)

  # Plots the tree with tip labels
  ape::plot.phylo(tree, show.tip.label = TRUE, cex = 0.7)

  # Closes the PDF device
  dev.off()  

  # Return nothing
  NULL
}
