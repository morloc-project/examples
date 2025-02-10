rmock <- function(x) {
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

rslurp <- function(inputfile) {
  readBin(con = inputfile, what = "raw", n = file.info(inputfile)$size)
}

rnTimes <- function(n, f, x) {
  for (i in 1:n) {
    x <- f(x)
  }
  x
}
