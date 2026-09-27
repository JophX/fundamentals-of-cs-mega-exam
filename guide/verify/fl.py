"""Small formal-languages toolkit used to *verify* every answer in the guide.

Grammars are written as strings like
    "S -> aSb | ε ; A -> ..."
Nonterminals are single uppercase letters (optionally followed by ' or digits),
everything else is a terminal. 'ε' (or empty alternative) is the empty string.
"""
import itertools
import re
from collections import defaultdict

EPS = "ε"


# ------------------------------------------------------------------ grammars
def tokenize_rhs(rhs):
    toks = re.findall(r"[A-Z](?:'|\d)*|.", rhs.replace(" ", ""))
    return tuple(t for t in toks if t != EPS)


def parse_grammar(text):
    """Return (start, {nt: [tuple(symbols), ...]})."""
    prods = defaultdict(list)
    start = None
    for rule in re.split(r"[;\n]", text):
        if not rule.strip():
            continue
        lhs, rhs = rule.split("->")
        lhs = lhs.strip()
        start = start or lhs
        for alt in rhs.split("|"):
            prods[lhs].append(tokenize_rhs(alt.strip()))
    return start, dict(prods)


def is_nt(sym, prods):
    return sym in prods


def earley(start, prods, word):
    """Earley recognizer for arbitrary CFGs (handles ε and left recursion)."""
    nullable = set()
    changed = True
    while changed:
        changed = False
        for A, alts in prods.items():
            if A not in nullable and any(all(s in nullable for s in alt) for alt in alts):
                nullable.add(A)
                changed = True
    n = len(word)
    chart = [set() for _ in range(n + 1)]
    for alt in prods[start]:
        chart[0].add((start, alt, 0, 0))
    for i in range(n + 1):
        agenda = list(chart[i])
        while agenda:
            A, alt, dot, org = agenda.pop()
            if dot < len(alt):
                X = alt[dot]
                if X in prods:  # predict
                    for beta in prods[X]:
                        it = (X, beta, 0, i)
                        if it not in chart[i]:
                            chart[i].add(it)
                            agenda.append(it)
                    if X in nullable:
                        it = (A, alt, dot + 1, org)
                        if it not in chart[i]:
                            chart[i].add(it)
                            agenda.append(it)
                elif i < n and word[i] == X:  # scan
                    chart[i + 1].add((A, alt, dot + 1, org))
            else:  # complete
                for (B, balt, bdot, borg) in list(chart[org]):
                    if bdot < len(balt) and balt[bdot] == A:
                        it = (B, balt, bdot + 1, borg)
                        if it not in chart[i]:
                            chart[i].add(it)
                            agenda.append(it)
    return any(A == start and dot == len(alt) and org == 0 for (A, alt, dot, org) in chart[n])


def generates(grammar_text, word):
    s, p = parse_grammar(grammar_text)
    return earley(s, p, word)


def all_words(alphabet, maxlen):
    for n in range(maxlen + 1):
        for t in itertools.product(alphabet, repeat=n):
            yield "".join(t)


def check_grammar(grammar_text, alphabet, predicate, maxlen, name=""):
    """Compare L(G) with {w : predicate(w)} on every word up to maxlen."""
    s, p = parse_grammar(grammar_text)
    bad = []
    count = 0
    for w in all_words(alphabet, maxlen):
        g, want = earley(s, p, w), predicate(w)
        count += 1
        if g != want:
            bad.append((w or EPS, "grammar says " + str(g), "definition says " + str(want)))
    status = "OK" if not bad else "MISMATCH"
    print(f"[{status}] {name}: checked all {count} strings over {{{','.join(alphabet)}}} up to length {maxlen}")
    for b in bad[:10]:
        print("    ", *b)
    return not bad


# ------------------------------------------------------------------ CYK
def cyk(start, prods, word, show=True):
    """CYK for a CNF grammar. Prints the triangular table (Linz/Sipser style)."""
    n = len(word)
    V = {}
    for i in range(n):
        V[(i, i)] = {A for A, alts in prods.items() if (word[i],) in alts}
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            cell = set()
            for k in range(i, j):
                for A, alts in prods.items():
                    for alt in alts:
                        if len(alt) == 2 and alt[0] in V[(i, k)] and alt[1] in V[(k + 1, j)]:
                            cell.add(A)
            V[(i, j)] = cell
    if show:
        w = max(10, max(len(fmt(V[k])) for k in V) + 2)
        print("Row = substring length; column = start position (1-based)")
        print(" " * 6 + "".join(f"{c}:{ch}".ljust(w) for c, ch in enumerate(word, 1)))
        for length in range(1, n + 1):
            row = "".join(fmt(V[(i, i + length - 1)]).ljust(w) for i in range(n - length + 1))
            print(f"len{length}: " + row)
    return start in V[(0, n - 1)], V


def fmt(s):
    return "{" + ",".join(sorted(s)) + "}" if s else "∅"


# ------------------------------------------------------------------ automata
class DFA:
    def __init__(self, states, alphabet, delta, start, finals):
        self.states, self.alphabet, self.delta = list(states), list(alphabet), delta
        self.start, self.finals = start, set(finals)

    def accepts(self, w):
        q = self.start
        for c in w:
            q = self.delta.get((q, c))
            if q is None:
                return False
        return q in self.finals


def check_dfa(dfa, predicate, maxlen, name=""):
    bad = [w for w in all_words(dfa.alphabet, maxlen) if dfa.accepts(w) != predicate(w)]
    print(f"[{'OK' if not bad else 'MISMATCH'}] {name}: all strings up to length {maxlen}")
    for w in bad[:10]:
        print("    ", w or EPS)
    return not bad


def nfa_accepts(delta, start, finals, w):
    """delta: {(q, symbol_or_'ε'): set(states)}"""
    def closure(S):
        stack, out = list(S), set(S)
        while stack:
            q = stack.pop()
            for r in delta.get((q, EPS), ()):
                if r not in out:
                    out.add(r)
                    stack.append(r)
        return out
    cur = closure({start})
    for c in w:
        nxt = set()
        for q in cur:
            nxt |= set(delta.get((q, c), ()))
        cur = closure(nxt)
    return bool(cur & set(finals))


def subset_construction(delta, start, finals, alphabet, show=True):
    def closure(S):
        stack, out = list(S), set(S)
        while stack:
            q = stack.pop()
            for r in delta.get((q, EPS), ()):
                if r not in out:
                    out.add(r)
                    stack.append(r)
        return frozenset(out)
    s0 = closure({start})
    todo, seen, table = [s0], {s0}, {}
    order = [s0]
    while todo:
        S = todo.pop(0)
        for c in alphabet:
            T = set()
            for q in S:
                T |= set(delta.get((q, c), ()))
            T = closure(T)
            table[(S, c)] = T
            if T not in seen:
                seen.add(T)
                todo.append(T)
                order.append(T)
    def nm(S):
        return "{" + ",".join(sorted(S)) + "}" if S else "∅"
    if show:
        print("DFA state".ljust(16) + "".join(c.ljust(16) for c in alphabet) + "final?")
        for S in order:
            mark = "→" if S == s0 else " "
            print((mark + nm(S)).ljust(16) + "".join(nm(table[(S, c)]).ljust(16) for c in alphabet)
                  + ("yes" if S & set(finals) else ""))
    return s0, seen, table


def minimize_table_filling(dfa, show=True):
    """Table-filling (marking) algorithm. Returns the equivalence classes."""
    Q = [q for q in dfa.states]
    marked = {}
    rnd = 0
    for i, p in enumerate(Q):
        for q in Q[i + 1:]:
            if (p in dfa.finals) != (q in dfa.finals):
                marked[frozenset((p, q))] = 0
    if show:
        print("round 0: mark every (final, non-final) pair:", ", ".join("(" + ",".join(sorted(k)) + ")" for k in marked))
    changed = True
    while changed:
        changed = False
        rnd += 1
        new = {}
        for i, p in enumerate(Q):
            for q in Q[i + 1:]:
                pq = frozenset((p, q))
                if pq in marked:
                    continue
                for c in dfa.alphabet:
                    a, b = dfa.delta[(p, c)], dfa.delta[(q, c)]
                    if a != b and frozenset((a, b)) in marked:
                        new[pq] = (rnd, c, a, b)
                        break
        for k, v in new.items():
            marked[k] = v[0]
            changed = True
            if show:
                p, q = sorted(k)
                print(f"round {v[0]}: mark ({p},{q}) because on '{v[1]}' they go to ({v[2]},{v[3]}) which is marked")
    classes = []
    for q in Q:
        for cl in classes:
            if frozenset((q, cl[0])) not in marked:
                cl.append(q)
                break
        else:
            classes.append([q])
    if show:
        print("Unmarked pairs are indistinguishable → classes:", ", ".join("{" + ",".join(c) + "}" for c in classes))
    return classes
