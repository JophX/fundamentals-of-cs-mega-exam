from fl import subset_construction, EPS
N2 = {("s",EPS):{"x","y"}, ("x","a"):{"x"}, ("y","a"):{"z"}, ("z","b"):{"y"}}
subset_construction(N2, "s", {"x","y"}, "ab")
