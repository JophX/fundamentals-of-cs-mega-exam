from fl import subset_construction
N1 = {("p0","a"):{"p0","p1"}, ("p0","b"):{"p0"}, ("p1","b"):{"p2"}}
subset_construction(N1, "p0", {"p2"}, "ab")
