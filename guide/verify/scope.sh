x=1
f() { echo "f sees x = $x"; }
g() { local x=2; f; }
g
