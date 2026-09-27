"""Chapter 2: every DFA/NFA in the chapter, checked against its English description."""
import re
from fl import DFA, check_dfa, nfa_accepts, subset_construction, all_words, EPS

# Ex 1: even number of b's
d1 = DFA("EO", "ab", {("E","a"):"E",("E","b"):"O",("O","a"):"O",("O","b"):"E"}, "E", "E")
check_dfa(d1, lambda w: w.count("b") % 2 == 0, 12, "even number of b's")

# Ex 2: ends with ab
d2 = DFA(["q0","q1","q2"], "ab", {("q0","a"):"q1",("q0","b"):"q0",
                                  ("q1","a"):"q1",("q1","b"):"q2",
                                  ("q2","a"):"q1",("q2","b"):"q0"}, "q0", ["q2"])
check_dfa(d2, lambda w: w.endswith("ab"), 12, "ends with ab")

# Ex 3: contains aba
d3 = DFA(["q0","q1","q2","q3"], "ab", {("q0","a"):"q1",("q0","b"):"q0",
    ("q1","a"):"q1",("q1","b"):"q2",("q2","a"):"q3",("q2","b"):"q0",
    ("q3","a"):"q3",("q3","b"):"q3"}, "q0", ["q3"])
check_dfa(d3, lambda w: "aba" in w, 12, "contains aba")

# Ex 4: number of a's divisible by 3
d4 = DFA(["r0","r1","r2"], "ab", {("r0","a"):"r1",("r1","a"):"r2",("r2","a"):"r0",
    ("r0","b"):"r0",("r1","b"):"r1",("r2","b"):"r2"}, "r0", ["r0"])
check_dfa(d4, lambda w: w.count("a") % 3 == 0, 12, "#a divisible by 3")

# Ex 5 (exam 2022 Q1 statement 1): starts with a, OR ends with c, OR odd number of b's
# product of three small machines; we just check the language is recognised by a DFA we build by product
import itertools
def step(state, c):
    first, last, parity = state
    if first == "?": first = "A" if c == "a" else "N"
    return (first, c, parity ^ (c == "b"))
states = {("?", "", False)}
todo = [("?", "", False)]; delta = {}
while todo:
    s = todo.pop()
    for c in "abc":
        t = step(s, c); delta[(s, c)] = t
        if t not in states: states.add(t); todo.append(t)
fin = [s for s in states if s[0] == "A" or s[1] == "c" or s[2]]
d5 = DFA(states, "abc", delta, ("?", "", False), fin)
check_dfa(d5, lambda w: w.startswith("a") or w.endswith("c") or w.count("b") % 2 == 1, 8,
          f"exam Q1: starts a / ends c / odd b  (product DFA with {len(states)} states)")

# Product construction example: even #b AND ends with ab
prod = {}
for (p, c), p2 in d1.delta.items():
    for q in d2.states:
        prod[((p, q), c)] = (p2, d2.delta[(q, c)])
d6 = DFA([(p, q) for p in "EO" for q in d2.states], "ab", prod, ("E", "q0"), [("E", "q2")])
check_dfa(d6, lambda w: w.count("b") % 2 == 0 and w.endswith("ab"), 12, "product: even b AND ends with ab")

# NFA: ends with ab
N1 = {("p0","a"):{"p0","p1"}, ("p0","b"):{"p0"}, ("p1","b"):{"p2"}}
bad = [w for w in all_words("ab", 12) if nfa_accepts(N1, "p0", {"p2"}, w) != w.endswith("ab")]
print(f"[{'OK' if not bad else 'MISMATCH'}] NFA for ends-with-ab")
N2 = {("s",EPS):{"x","y"}, ("x","a"):{"x"}, ("y","a"):{"z"}, ("z","b"):{"y"}}
bad = [w for w in all_words("ab", 12) if nfa_accepts(N2, "s", {"x","y"}, w) !=
       bool(re.fullmatch(r"a*|(ab)*", w))]
print(f"[{'OK' if not bad else 'MISMATCH'}] λ-NFA for a* ∪ (ab)*")
# Practice solutions
p1 = DFA(["OK","NB","D"], "ab", {("OK","a"):"NB",("OK","b"):"OK",("NB","b"):"OK",("NB","a"):"D",
                                 ("D","a"):"D",("D","b"):"D"}, "OK", ["OK"])
check_dfa(p1, lambda w: all(w[i+1:i+2] == "b" for i, c in enumerate(w) if c == "a"), 12,
          "practice 1: every a followed by b")
N3 = {("p0","a"):{"p0","p1"}, ("p0","b"):{"p0"}, ("p1","a"):{"p2"}, ("p1","b"):{"p2"}}
bad = [w for w in all_words("ab", 12) if nfa_accepts(N3, "p0", {"p2"}, w) != (len(w) >= 2 and w[-2] == "a")]
print(f"[{'OK' if not bad else 'MISMATCH'}] practice 3: second-to-last letter is a (NFA)")
from fl import subset_construction
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    s0, seen, table = subset_construction(N3, "p0", {"p2"}, "ab")
print(f"      its DFA has {len(seen)} states:", sorted("{" + ",".join(sorted(S)) + "}" for S in seen))
