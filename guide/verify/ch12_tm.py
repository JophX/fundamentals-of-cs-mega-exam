import re
from fl import all_words
B = "□"
d = {("q0","a"):("q1","x","R"),("q0","y"):("q3","y","R"),
     ("q1","a"):("q1","a","R"),("q1","y"):("q1","y","R"),("q1","b"):("q2","y","L"),
     ("q2","y"):("q2","y","L"),("q2","a"):("q2","a","L"),("q2","x"):("q0","x","R"),
     ("q3","y"):("q3","y","R"),("q3",B):("q4",B,"R")}
def run(w, trace=False):
    tape, q, h, ids = dict(enumerate(w)), "q0", 0, []
    for _ in range(10000):
        if trace:
            s = "".join(tape.get(i, B) for i in range(max(tape)+2 if tape else 1)).rstrip(B)
            ids.append(s[:h] + q + (s[h:] or B))
        k = (q, tape.get(h, B))
        if k not in d: break
        q, tape[h], mv = d[k]; h += 1 if mv == "R" else -1
    return q == "q4", ids
bad = [w for w in all_words("ab", 10) if run(w)[0] != bool(re.fullmatch(r"(a+)(b+)", w) and w.count("a") == w.count("b"))]
print(f"[{'OK' if not bad else 'MISMATCH'}] TM accepts exactly a^n b^n (n>=1), all strings up to length 10", bad[:3])
print(" ⊢ ".join(run("aabb", True)[1]))
