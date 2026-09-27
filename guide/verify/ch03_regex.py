"""Chapter 3: every regular expression in the chapter, checked on all strings up to length 12.
Regexes are written in the course (Linz) syntax: + is union, λ is the empty string."""
import re
from fl import all_words

def to_py(r):
    return r.replace("λ", "(?:)").replace("+", "|")

def check(r, pred, name, alphabet="ab", n=12):
    py = re.compile(to_py(r))
    bad = [w for w in all_words(alphabet, n) if bool(py.fullmatch(w)) != pred(w)]
    print(f"[{'OK' if not bad else 'MISMATCH'}] {r:<32} {name}")
    for w in bad[:5]: print("       counterexample:", w or "λ")

check("(a+b)*aba(a+b)*", lambda w: "aba" in w, "contains aba")
check("(a+b)*ab", lambda w: w.endswith("ab"), "ends with ab")
check("a*(ba*ba*)*", lambda w: w.count("b") % 2 == 0, "even number of b's")
check("a*(λ+b)a*", lambda w: w.count("b") <= 1, "at most one b")
check("a*ba*", lambda w: w.count("b") == 1, "exactly one b")
check("(b+ab)*(λ+a)", lambda w: "aa" not in w, "no two consecutive a's")
check("((a+b)(a+b))*", lambda w: len(w) % 2 == 0, "even length")
check("((a+b)(a+b)(a+b))*", lambda w: len(w) % 3 == 0, "length divisible by 3")
check("b*(ab*ab*ab*)*", lambda w: w.count("a") % 3 == 0, "number of a's divisible by 3")
check("a(a+b+c)*+(a+b+c)*c+(a+c)*b(a+c)*(b(a+c)*b(a+c)*)*",
      lambda w: w.startswith("a") or w.endswith("c") or w.count("b") % 2 == 1,
      "exam 2022 Q1: starts a / ends c / odd #b", "abc", 8)
check("(a+b)*a(a+b)", lambda w: len(w) >= 2 and w[-2] == "a", "second-to-last is a")
check("(ab+ba)*", lambda w: len(w) % 2 == 0 and all(w[i] != w[i+1] for i in range(0, len(w), 2)),
      "(ab+ba)* read as: pairs, each pair ab or ba")

print("\nIdentities (checked as languages, strings up to length 10):")
def same(r1, r2, alphabet="ab", n=10, expect=True):
    p1, p2 = re.compile(to_py(r1)), re.compile(to_py(r2))
    ok = all(bool(p1.fullmatch(w)) == bool(p2.fullmatch(w)) for w in all_words(alphabet, n))
    tag = "" if expect else "   (trap: claimed identity is FALSE, e.g. ab)"
    assert ok == expect
    print(f"   {r1:<14} {'=' if ok else '≠'} {r2:<14} {'✔' if ok else '✘'}{tag}")
same("(a*)*", "a*"); same("λ+aa*", "a*"); same("(a+b)*", "(a*b*)*"); same("(a*b*)*", "(a+b)*")
same("a*a*", "a*"); same("(ab)*a", "a(ba)*"); same("(a+b)*", "a*+b*", expect=False)
