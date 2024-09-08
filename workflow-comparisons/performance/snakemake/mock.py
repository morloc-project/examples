with open(snakemake.output[0], "w") as outfh:
    with open(snakemake.input[0], "r") as infh:
        lines = infh.readlines()
        print("".join(lines), file=outfh)
