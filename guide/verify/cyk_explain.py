"""Print every CYK cell with every split tried: python3 cyk_explain.py '<grammar>' word"""
import sys
from fl import parse_grammar, fmt
g, w = sys.argv[1], sys.argv[2]
start, P = parse_grammar(g)
n = len(w); V = {}
for i in range(n):
    V[(i, i)] = {A for A, rs in P.items() if (w[i],) in rs}
    print(f"V{i+1}{i+1} ('{w[i]}'): variables with a rule → {w[i]}: {fmt(V[(i,i)])}")
for L in range(2, n + 1):
    print()
    for i in range(n - L + 1):
        j = i + L - 1; cell = set(); tries = []
        for k in range(i, j):
            left, right = V[(i, k)], V[(k+1, j)]
            got = {A for A, rs in P.items() for r in rs if len(r) == 2 and r[0] in left and r[1] in right}
            cell |= got
            tries.append(f"{w[i:k+1]}|{w[k+1:j+1]}: {fmt(left)}·{fmt(right)} → {fmt(got)}")
        V[(i, j)] = cell
        print(f"V{i+1}{j+1} ('{w[i:j+1]}'): " + ";  ".join(tries) + f"   ⇒ {fmt(cell)}")
print(f"\nStart symbol {start} {'∈' if start in V[(0,n-1)] else '∉'} V1{n}  ⇒  '{w}' {'IS' if start in V[(0,n-1)] else 'is NOT'} in L(G)")
