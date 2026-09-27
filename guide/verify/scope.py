x = 1
def f():
    print("f sees x =", x)
def g():
    x = 2
    f()
g()
