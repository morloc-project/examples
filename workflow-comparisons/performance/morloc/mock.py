def mockpy(x):
    return "".join(x.split("\n"))

def slurp(filename):
    with open(filename, "r") as fh:
        return fh.read()
