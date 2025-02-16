import copy

def pmock(x):
    if len(x) <= 2:
        return x
    y = copy.copy(x)
    y[0], y[-1] = y[-1], y[0]
    return y

with open(snakemake.input[0], "rb") as infh:
    data = bytearray(infh.read())

modified_data = pmock(data)

with open(snakemake.output[0], "wb") as outfh:
    outfh.write(modified_data)
