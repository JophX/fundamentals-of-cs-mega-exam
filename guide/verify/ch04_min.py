from fl import DFA, minimize_table_filling, check_dfa
# DFA for "ends with ab" with a redundant state q3 (copy of q0)
d = DFA(["q0","q1","q2","q3"], "ab", {
 ("q0","a"):"q1",("q0","b"):"q3",("q1","a"):"q1",("q1","b"):"q2",
 ("q2","a"):"q1",("q2","b"):"q0",("q3","a"):"q1",("q3","b"):"q0"}, "q0", ["q2"])
check_dfa(d, lambda w: w.endswith("ab"), 10, "4-state DFA accepts 'ends with ab'")
minimize_table_filling(d)
