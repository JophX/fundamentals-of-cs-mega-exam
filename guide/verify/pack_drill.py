"""Verify every grammar answer in the Priority Pack drill section."""
import re, sys
from fl import check_grammar, parse_grammar, earley, all_words
from pack_cnf import same_minus_lambda, is_cnf

if "--check" in sys.argv:
    # G1: even palindromes
    same_minus_lambda("S -> aSa | bSb | ε",
        "S -> AX | BY | AA | BB ; X -> SA ; Y -> SB ; A -> a ; B -> b", "ab", 12, "Drill 2 (even palindromes)")
    # G2
    same_minus_lambda("S -> AB | aB ; A -> aab | ε ; B -> bbA",
        "S -> AB | UB | TW | TT ; A -> UV ; V -> UT ; B -> TW | TT ; W -> TA ; U -> a ; T -> b", "ab", 12, "Drill 3")
    # G3
    same_minus_lambda("S -> A | aSb ; A -> bA | b",
        "S -> TA | b | UX ; X -> ST ; A -> TA | b ; U -> a ; T -> b", "ab", 12, "Drill 4 (unit rules)")
    # exam grammars
    def L1(w):
        bal = 0
        for c in w:
            bal += 1 if c == "a" else -1
            if bal < 0: return False
        return bal == 0
    check_grammar("S -> aSbS | ε", "ab", L1, 14, "Drill 15: Dyck grammar")
    def neq(w):
        m = re.fullmatch(r"(a*)(b*)", w); return bool(m) and len(m.group(1)) != len(m.group(2))
    check_grammar("S -> aSb | A | B ; A -> aA | a ; B -> bB | b", "ab", neq, 14, "Drill 16: a^n b^m, n != m")
