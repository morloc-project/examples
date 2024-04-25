import treebase as r

assert list(sorted(r.countKmers(2, "ATTT").items())) == [("AT", 1), ("TT", 2)]

def circle(newick):
    return r.writeTreeStr(r.readTreeStr(f"{newick};"))

def circle_check(newick):
    return circle(newick) == newick

assert circle('("A","B")')
assert circle('("A",("B","C"))')
assert circle('(("A","B"),"C")')
assert circle('(("A":1,"B":2)x:12,("C":3,"D":4)y:11)')
