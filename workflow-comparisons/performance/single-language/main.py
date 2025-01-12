import sys

def mockpy(x):
    if(len(x) <= 2):
        return x
    return x[-1] + x[0:-1] 

def open_file(x):
    with open(x, "r") as fh:
        data = fh.read()
    return data

def run_linear(data, n):
    for _ in range(n):
        data = mockpy(data)
    return len(data)

if __name__ == "__main__":
    nodes = int(sys.argv[1])
    inputfile = sys.argv[2]
    length = run_linear(open_file(inputfile), nodes)
    print(length)
