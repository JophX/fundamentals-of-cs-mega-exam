"""5DV037 exam Q8 (◇-EQUATION). ◇ is NAND. Verify (1) the exam's example,
(2) the translation  ¬a = a◇1,  a∧b = (a◇b)◇1,  a∨b = (a◇1)◇(b◇1)
is correct and size-linear on random formulas, so  φ satisfiable  ⇔  e_φ = 1 solvable."""
import itertools, random
D = lambda a, b: 0 if (a == 1 and b == 1) else 1

# (1) the example in the exam
sols = []
for x, y, z in itertools.product([0, 1], repeat=3):
    if D(D(D(x, 1), y), D(x, z)) == D(z, 1):
        sols.append((x, y, z))
print("Example ((x◇1)◇y)◇(x◇z) = (z◇1): solutions (x,y,z) =", sols)

# (2) random formulas
def rand_formula(vars_, depth):
    if depth == 0 or random.random() < 0.25:
        return ("var", random.choice(vars_))
    op = random.choice(["not", "and", "or"])
    if op == "not":
        return ("not", rand_formula(vars_, depth - 1))
    return (op, rand_formula(vars_, depth - 1), rand_formula(vars_, depth - 1))

def ev(f, a):
    t = f[0]
    if t == "var": return a[f[1]]
    if t == "not": return 1 - ev(f[1], a)
    if t == "and": return ev(f[1], a) & ev(f[2], a)
    return ev(f[1], a) | ev(f[2], a)

def tr(f):  # formula -> ◇-expression (as nested tuple), each child used ONCE
    t = f[0]
    if t == "var": return ("v", f[1])
    if t == "not": return ("d", tr(f[1]), ("c", 1))
    if t == "and": return ("d", ("d", tr(f[1]), tr(f[2])), ("c", 1))
    return ("d", ("d", tr(f[1]), ("c", 1)), ("d", tr(f[2]), ("c", 1)))

def ev_d(e, a):
    if e[0] == "v": return a[e[1]]
    if e[0] == "c": return e[1]
    return D(ev_d(e[1], a), ev_d(e[2], a))

def size(e): return 1 if e[0] in "vc" else 1 + size(e[1]) + size(e[2])
def fsize(f): return 1 if f[0] == "var" else 1 + sum(fsize(g) for g in f[1:])

random.seed(1)
worst = 0
for _ in range(3000):
    V = ["x", "y", "z", "w"]
    f = rand_formula(V, 6)
    e = tr(f)
    worst = max(worst, size(e) / fsize(f))
    for bits in itertools.product([0, 1], repeat=4):
        a = dict(zip(V, bits))
        assert ev(f, a) == ev_d(e, a)
print("3000 random formulas: translation agrees with the formula on every assignment.")
print(f"Largest size ratio |e_φ| / |φ| = {worst:.2f}  (bounded by a constant ⇒ polynomial reduction)")
