This fold contains tests that compare the performance and implementation of
morloc versus workflow languages (currently just nextflow and snakemake).

## Setup

Create a Docker image that contains everything needed to run all of the
comparisons (morloc, pybind11 for Python/C++ interop, nextflow, snakemake, etc):

```
make build
```

Then enter the container shell:

```
make shell
```

This mounts the current working directory into the container as a virtual
volume. This means that from within the container you may alter this folder and
the changes will persist on your machine, but no other changes (installed
programs, for instance) will be visible.
