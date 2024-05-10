# Open newick formatted tree
# Read the file from the object "snakemake" provided by the snakemake runtime
tree <- ape::read.tree(snakemake@input[[1]])

# Create plot
# Write to the PDF file passed from the snakemake runtime
pdf(snakemake@output[[1]], width = 8, height = length(tree$tip.label) * 0.1)
par(cex = 0.7)
plot(tree, show.tip.label = TRUE, cex = 0.7)
dev.off()
