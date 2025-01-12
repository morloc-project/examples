rmock <- function(x) {
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

rslurp <- function(inputfile) {
  readChar(con=inputfile, nchars=file.size(inputfile), useBytes=TRUE)
}

rnTimes <- function(n, f, x) {
  for (i in 1:n) {
    x <- f(x)
  }
  x
}

rlength <- function(x) {
  nchar(x, type="bytes")
}
