import rooted_tree as r

assert list(sorted(r.countKmers(2, "ATTT").items())) == [("AT", 1), ("TT", 2)]
