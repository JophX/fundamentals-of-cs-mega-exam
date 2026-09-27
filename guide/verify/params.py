def example2(weight=20, length=57):
    print(weight, length)

def example4(p1, *p2):
    print(p1, p2)

def example5(weight=20, length=57, **parameters):
    print(weight, length, parameters)

example2(length=12)                    # keyword argument, default for weight
example4(1)                            # no extra arguments
example4(1, 2, 3, 4, 5)                # extra positional -> tuple
example5(length=12, myname="Halvard")  # extra keyword -> dict
