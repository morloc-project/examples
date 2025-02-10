mock <- function(x) {
  n <- length(x)
  if (n <= 2){
      x
  } else {
      # Swap first and last characters
      temp <- x[1]
      x[1] <- x[n]
      x[n] <- temp
      x
  }
}


run_linear <- function(data, n) {
  for (i in 1:n) {
    data <- mock(data)
  }
  length(data)
}


# Main function
main <- function() {
  args <- commandArgs(trailingOnly=TRUE)
  nodes <- args[[1]]
  inputfile <- args[[2]]

  # Read data from file
  # `useBytes=TRUE` gives a ~10X speedup by not handling for wide characters
  data <- readBin(con=inputfile, what = "raw", n = file.info(inputfile)$size)

  # Run linear processing
  length <- run_linear(data, nodes)

  # Print result
  cat(length, "\n")
}

# Run main function
if (!interactive()) {
  main()
}
