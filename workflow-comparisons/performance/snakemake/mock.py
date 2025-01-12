def pmock(x):
    if(len(x) <= 2):
        return x
    return x[-1] + x[0:-1] 

with open(snakemake.output[0], "w") as outfh:
    with open(snakemake.input[0], "r") as infh:
        text = pmock(infh.read())
        print(text, file=outfh)
