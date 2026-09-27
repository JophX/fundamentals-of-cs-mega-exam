"""5DV037 exam Q5: is the grammar in CNF, and CYK on 'abcab'."""
from fl import parse_grammar, cyk
G = """S -> SS | XY | XS'
S' -> SY
X -> a
Y -> BC | BB | b
B -> b
C -> CC | c"""
start, prods = parse_grammar(G)
bad = [(A, "".join(r)) for A, rs in prods.items() for r in rs
       if not ((len(r) == 1 and r[0] not in prods) or (len(r) == 2 and all(s in prods for s in r)))]
print("Productions breaking CNF:", bad or "none — the grammar IS in CNF")
ok, V = cyk(start, prods, "abcab")
print("S in top cell?", ok, "=> abcab", "IS" if ok else "is NOT", "in L(G)")
