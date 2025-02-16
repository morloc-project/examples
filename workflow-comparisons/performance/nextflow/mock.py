import sys
import copy

def mockpy(x):
    if len(x) <= 2:
        return x
    y = copy.copy(x)
    y[0], y[-1] = y[-1], y[0]
    return y

def open_file(x):
    with open(x, "rb") as fh:
        data = bytearray(fh.read())
    return data

def write_file(x, filename):
    with open(filename, "wb") as fh:
        fh.write(x)

if __name__ == "__main__":
    inputfile = sys.argv[1]
    outputfile = sys.argv[2]
    data = open_file(inputfile)
    modified_data = mockpy(data)
    write_file(modified_data, outputfile)
