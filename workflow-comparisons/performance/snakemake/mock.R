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

inputfile <- snakemake@input[[1]]
outputfile <- snakemake@output[[1]]

data <- readBin(con = inputfile, what = "raw", n = file.info(inputfile)$size)
data <- mock(data)

writeBin(data, con = outputfile)
