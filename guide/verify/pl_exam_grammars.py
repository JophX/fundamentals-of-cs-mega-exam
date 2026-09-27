"""Verify the grammar answers for the Programspråk (5DV086) exams."""
import re
from fl import check_grammar, generates, EPS

def an_bm(w):
    m = re.fullmatch(r"(a*)(b*)", w)
    return (len(m.group(1)), len(m.group(2))) if m else None

# 2023-05-05 Problem 1, reading A (the formula):  n != 2m   (#a != 2*#b)
G_formula = """S -> A | B
A -> aA | aE
E -> aaEb | ε
B -> aaBb | aUb | Ub
U -> aaUb | aUb | Ub | ε"""
def L_formula(w):
    p = an_bm(w); return p is not None and p[0] != 2 * p[1]
check_grammar(G_formula, "ab", L_formula, 14, "2023-05-05 P1, formula reading  a^n b^m, n != 2m")

# Reading B (the Swedish sentence): #a is not half of #b, i.e. m != 2n
G_sentence = """S -> A | B
A -> Ab | Eb
E -> aEbb | ε
B -> aBbb | aUb | aU
U -> aUbb | aUb | aU | ε"""
def L_sentence(w):
    p = an_bm(w); return p is not None and p[1] != 2 * p[0]
check_grammar(G_sentence, "ab", L_sentence, 14, "2023-05-05 P1, sentence reading a^n b^m, m != 2n")

# Problem 2 (both exams): Dyck-like language
def L1(w):
    bal = 0
    for c in w:
        bal += 1 if c == "a" else -1
        if bal < 0: return False
    return bal == 0
check_grammar("S -> aSbS | ε", "ab", L1, 14, "L1 with S -> aSbS | ε")
check_grammar("S -> SS | aSb | ε", "ab", L1, 14, "L1 with S -> SS | aSb | ε")

# 2023-03-16 Problem 1: which strings does G generate?
G1 = """S -> SB | aA | cCb
A -> aAb | ε
B -> BB | C
C -> ε"""
print()
print("2023-03-16 Problem 1 — membership of each string:")
for label, w in zip("ABCDEFGHI", ["", "abcb", "aabcb", "cbab", "abc", "acb",
                                  "aaabbbbcccbb", "aaabbbbccbbcc", "ccbbbaab"]):
    print(f"  {label}. {w or EPS:<15} {'YES' if generates(G1, w) else 'no'}")
def L_G1(w):
    if w == "cb": return True
    m = re.fullmatch(r"(a+)(b*)", w)
    return bool(m) and len(m.group(1)) == len(m.group(2)) + 1
check_grammar(G1, "abc", L_G1, 9, "L(G) = { a^(k+1) b^k : k>=0 } ∪ { cb }")
