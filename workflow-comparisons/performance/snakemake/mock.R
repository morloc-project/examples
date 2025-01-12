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

input_file <- snakemake@input[[1]]
output_file <- snakemake@output[[1]]

data <- readChar(con=input_file, nchars=file.size(input_file), useBytes=TRUE)
data <- mock(data)

write(data, file=output_file)
