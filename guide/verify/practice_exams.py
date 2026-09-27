import re
from fl import parse_grammar, cyk, all_words, nfa_accepts
from pack_cnf import same_minus_lambda
same_minus_lambda("S -> aSb | SS | ε", "S -> AX | AB | SS ; X -> SB ; A -> a ; B -> b", "ab", 12, "FCS practice 5 CNF")
s, p = parse_grammar("S -> AX | AB | SS ; X -> SB ; A -> a ; B -> b"); print("  CYK aabb accepted:", cyk(s, p, "aabb", show=False)[0])
same_minus_lambda("S -> aSb | bA | ε ; A -> aA | a", "S -> UX | UT | TA ; X -> ST ; A -> UA | a ; U -> a ; T -> b", "ab", 12, "PL practice 2 CNF")
N = {("p0","a"):{"p0"},("p0","b"):{"p0","p1"},("p1","a"):{"p2"}}
print("[OK]" if all(nfa_accepts(N,"p0",{"p2"},w) == w.endswith("ba") for w in all_words("ab",10)) else "[BAD]", "FCS practice 3: NFA = ends with ba")
