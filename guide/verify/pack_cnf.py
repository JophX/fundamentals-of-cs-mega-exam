"""Priority pack: verify the CNF conversions and CYK tables."""
import sys
from fl import parse_grammar, earley, all_words, cyk

def is_cnf(text):
    s, p = parse_grammar(text)
    return all((len(r) == 1 and r[0] not in p) or (len(r) == 2 and all(x in p for x in r))
               for rs in p.values() for r in rs)

def same_minus_lambda(g1, g2, alphabet, n, name):
    s1, p1 = parse_grammar(g1); s2, p2 = parse_grammar(g2)
    bad = [w for w in all_words(alphabet, n) if w and earley(s1, p1, w) != earley(s2, p2, w)]
    print(f"[{'OK' if not bad else 'MISMATCH'}] {name}: L(CNF) = L(G) − {{λ}} on all strings up to length {n}; in CNF: {is_cnf(g2)}")
    for w in bad[:5]: print("    ", w)

# Example 1 (Sipser's classic, done in Linz's order)
G1 = "S -> ASA | aB ; A -> B | S ; B -> b | ε"
G1_step1 = "S -> ASA | SA | AS | S | aB | a ; A -> B | S ; B -> b"
G1_step2 = "S -> ASA | SA | AS | aB | a ; A -> b | ASA | SA | AS | aB | a ; B -> b"
G1_cnf = "S -> AX | SA | AS | UB | a ; A -> b | AX | SA | AS | UB | a ; B -> b ; U -> a ; X -> SA"
# Example 2 (the exam's Dyck grammar)
G2 = "S -> aSbS | ε"
G2_step1 = "S -> aSbS | abS | aSb | ab"
G2_cnf = "S -> AX | AY | AZ | AB ; X -> SW ; W -> BS ; Y -> BS ; Z -> SB ; A -> a ; B -> b"
# Example 3: unit chains + useless symbols
G3 = "S -> Aa | B | C ; A -> a | bA ; B -> A | bb ; C -> cC"
G3_cnf = "S -> AV | a | TA | TT ; A -> a | TA ; V -> a ; T -> b"

if __name__ == "__main__" and "--check" in sys.argv:
    same_minus_lambda(G1, G1_step1, "ab", 10, "Ex1 after removing λ")
    same_minus_lambda(G1, G1_step2, "ab", 10, "Ex1 after removing units")
    same_minus_lambda(G1, G1_cnf, "ab", 10, "Ex1 final CNF")
    same_minus_lambda(G2, G2_step1, "ab", 12, "Ex2 after removing λ")
    same_minus_lambda(G2, G2_cnf, "ab", 12, "Ex2 final CNF")
    same_minus_lambda(G3, G3_cnf, "abc", 9, "Ex3 final CNF")
if "--cyk1" in sys.argv:
    s, p = parse_grammar(G2_cnf); ok, _ = cyk(s, p, "aabab"); print("S in top cell:", ok)
if "--cyk2" in sys.argv:
    s, p = parse_grammar(G2_cnf); ok, _ = cyk(s, p, "abaabb"); print("S in top cell:", ok)
if "--cyk3" in sys.argv:
    s, p = parse_grammar(G1_cnf); ok, _ = cyk(s, p, "abaab"); print("S in top cell:", ok)
