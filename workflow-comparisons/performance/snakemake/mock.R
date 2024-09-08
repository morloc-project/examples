writeLines(
  paste(
    readLines(snakemake@input[[1]]), collapse = ""
  ), snakemake@output[[1]]
)
