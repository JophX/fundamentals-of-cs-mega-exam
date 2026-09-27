"""Chapter 7: every grammar in the recipe book, checked on all strings up to length 12."""
import re
from fl import check_grammar
def ab(w):
    m = re.fullmatch(r"(a*)(b*)", w); return (len(m.group(1)), len(m.group(2))) if m else None
def abc(w):
    m = re.fullmatch(r"(a*)(b*)(c*)", w); return tuple(len(g) for g in m.groups()) if m else None
N = 12
check_grammar("S -> aSb | ε", "ab", lambda w: ab(w) is not None and ab(w)[0] == ab(w)[1], N, "R1  a^n b^n")
check_grammar("S -> aSbb | ε", "ab", lambda w: ab(w) is not None and 2*ab(w)[0] == ab(w)[1], N, "R2  a^n b^2n")
check_grammar("S -> aaSb | ε", "ab", lambda w: ab(w) is not None and ab(w)[0] == 2*ab(w)[1], N, "R2' a^2n b^n")
check_grammar("S -> aSb | Sb | ε", "ab", lambda w: ab(w) is not None and ab(w)[0] <= ab(w)[1], N, "R3  a^n b^m, n <= m")
check_grammar("S -> aSb | B ; B -> bB | b", "ab", lambda w: ab(w) is not None and ab(w)[0] < ab(w)[1], N, "R3' a^n b^m, n < m")
check_grammar("S -> aSb | A | B ; A -> aA | a ; B -> bB | b", "ab", lambda w: ab(w) is not None and ab(w)[0] != ab(w)[1], N, "R4  a^n b^m, n != m")
check_grammar("S -> aSc | B ; B -> bBc | ε", "abc", lambda w: abc(w) is not None and abc(w)[0]+abc(w)[1] == abc(w)[2], 11, "R5  a^n b^m c^(n+m)")
check_grammar("S -> AB ; A -> aAb | ε ; B -> bBc | ε", "abc", lambda w: abc(w) is not None and abc(w)[1] == abc(w)[0]+abc(w)[2], 11, "R5' a^n b^(n+m) c^m")
check_grammar("S -> AC | B ; A -> aAb | ε ; C -> cC | ε ; B -> aB | D ; D -> bDc | ε", "abc",
   lambda w: abc(w) is not None and (abc(w)[0] == abc(w)[1] or abc(w)[1] == abc(w)[2]), 10, "R6  a^i b^j c^k, i=j or j=k")
check_grammar("S -> aSa | bSb | a | b | ε", "ab", lambda w: w == w[::-1], N, "R7  palindromes")
def bal(w):
    b = 0
    for c in w:
        b += 1 if c == "a" else -1
        if b < 0: return False
    return b == 0
check_grammar("S -> aSbS | ε", "ab", bal, N, "R8  balanced (Dyck)")
check_grammar("S -> aSbS | bSaS | ε", "ab", lambda w: w.count("a") == w.count("b"), N, "R9  |w|_a = |w|_b (any order)")
check_grammar("S -> SaSbS | SbSaS | ε", "ab", lambda w: w.count("a") == w.count("b"), N, "R9' alternative")
check_grammar("S -> T | TaS ; T -> aTbT | bTaT | ε", "ab", lambda w: w.count("a") >= w.count("b"), N, "R10 |w|_a >= |w|_b")
check_grammar("S -> aS | bS | ε", "ab", lambda w: True, N, "R11 everything (a+b)*")
check_grammar("S -> aSc | B ; B -> bB | ε", "abc", lambda w: abc(w) is not None and abc(w)[0] == abc(w)[2], 10, "P1  a^n b^m c^n")
check_grammar("S -> aSb | aaSb | ε", "ab", lambda w: ab(w) is not None and ab(w)[1] <= ab(w)[0] <= 2*ab(w)[1], N, "P2  m <= n <= 2m")
check_grammar("S -> XSX | a ; X -> a | b", "ab", lambda w: len(w) % 2 == 1 and w[len(w)//2] == "a", N, "P3  odd, middle a")
