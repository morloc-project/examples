import sys

def mockpy(x : str) -> str:
    if(len(x) <= 2):
        return x
    return x[-1] + x[0:-1]

def read_file(filename):
    with open(filename, "r") as fh:
        data = fh.read()
    return data

def write_file(x, filename):
    with open(filename, "w") as fh:
        fh.write(x)


if __name__ == "__main__":
    inputfile = sys.argv[1]
    outputfile = sys.argv[2]
    write_file(mockpy(read_file(inputfile)), outputfile)
