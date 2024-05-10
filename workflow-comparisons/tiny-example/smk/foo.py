with open(snakemake.output[0], "w") as fh:
    print(snakemake.params.x +
          snakemake.params.y, file=fh)
