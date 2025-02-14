# Performance checks

To run benchmarks:

```
# enter the flu case study shell
$ make shell 

# run hyperfine benchmarks from inside the shell
$ ./benchmark.sh
```

Output is written to stats.csv

See the code in the `analysis` folder for more info on the rationale for each
test and the benchmark conclusions.
