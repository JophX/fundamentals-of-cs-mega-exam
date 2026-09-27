"""FCS 2022/2025 exam Q4: the language as printed IS context-free. We exhibit a CFG and check it."""
from fl import check_grammar
E = "E -> aEaEbE | aEbEaE | bEaEaE | ε"          # |w|_a = 2|w|_b
check_grammar("S -> " + E.split("->")[1] if False else E, "ab",
              lambda w: w.count("a") == 2 * w.count("b"), 12, "E: |w|_a = 2|w|_b")
G1 = "S -> EaE | EaS ; " + E                    # |w|_a > 2|w|_b
check_grammar(G1, "ab", lambda w: w.count("a") > 2 * w.count("b"), 12, "|w|_a > 2|w|_b")
F = "F -> bFbFaF | bFaFbF | aFbFbF | ε"          # 2|w|_a = |w|_b
G2 = "S -> FbF | FbS ; " + F
check_grammar(G2, "ab", lambda w: 2 * w.count("a") < w.count("b"), 12, "2|w|_a < |w|_b")
G = "S -> A | B ; A -> EaE | EaA ; B -> FbF | FbB ; " + E + " ; " + F
check_grammar(G, "ab", lambda w: w.count("a") > 2*w.count("b") or 2*w.count("a") < w.count("b"), 12,
              "the WHOLE exam language L")
