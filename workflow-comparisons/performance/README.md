# Performance checks


To run hyperfine benchmarks execute the benchmark.sh script

```
./benchmark.sh
```

You probably want to enter the shell through the container setup in the parent
directory. From there, just run `make shell`. Then return here to run the
benchmarks. Note that the benchmarks may take a few hours to run.

Output is written to stats.csv

See the code in the `analysis` folder for more info on the rationale for each
test and the benchmark conclusions.
