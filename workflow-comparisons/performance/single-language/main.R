mock <- function(x) {
  # The charToRaw and rawToChar conversions are the main bottlenecks
  raw_x <- charToRaw(x)
  n <- length(raw_x)
  if (n <= 2){
      x
  } else {
      # Swap first and last characters
      temp <- raw_x[1]
      raw_x[1] <- raw_x[n]
      raw_x[n] <- temp
      rawToChar(raw_x)
  }
}


run_linear <- function(data, n) {
  for (i in 1:n) {
    data <- mock(data)
  }
  nchar(data, type="bytes")
}


# Main function
main <- function() {
  args <- commandArgs(trailingOnly=TRUE)
  nodes <- args[[1]]
  inputfile <- args[[2]]

  # Read data from file
  # `useBytes=TRUE` gives a ~10X speedup by not handling for wide characters
  data <- readChar(con=inputfile, nchars=file.size(inputfile), useBytes=TRUE)

  # Run linear processing
  length <- run_linear(data, nodes)

  # Print result
  cat(length, "\n")
}

# Run main function
if (!interactive()) {
  main()
}
