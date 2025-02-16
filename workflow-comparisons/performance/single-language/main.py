import sys
import copy

def mockpy(x):
    if(len(x) <= 2):
        return x
    y = copy.copy(x)
    temp = y[0]
    y[0] = y[-1]
    y[-1] = temp
    return y

def open_file(x):
    with open(x, "rb") as fh:
        data = bytearray(fh.read())
    return data

def run_linear(data, n):
    if(n == 0):
        return len(data)
    for _ in range(n):
        data = mockpy(data)
    return len(data)

if __name__ == "__main__":
    nodes = int(sys.argv[1])
    inputfile = sys.argv[2]
    length = run_linear(open_file(inputfile), nodes)
    print(length)
