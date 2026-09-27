#include <iostream>
using namespace std;

void swapByValue(int x, int y)      { int t = x; x = y; y = t; }
void swapByReference(int &x, int &y) { int t = x; x = y; y = t; }

void fRef(int &x, int &y) { x = x + 1; y = y * 2; }        // called as fRef(a, a)

int main() {
    int a = 1, b = 2;
    swapByValue(a, b);
    cout << "after swapByValue(a, b):     a = " << a << ", b = " << b << "\n";
    swapByReference(a, b);
    cout << "after swapByReference(a, b): a = " << a << ", b = " << b << "\n";

    int c = 5;
    fRef(c, c);                                             // x and y are ALIASES of c
    cout << "by reference, f(c, c) with c = 5:    c = " << c << "\n";

    // pass-by-value-result, simulated: copy in, work on copies, copy out (left to right)
    int d = 5;
    int x = d, y = d;          // copy in
    x = x + 1; y = y * 2;      // body works on local copies
    d = x; d = y;              // copy out: x first, then y (the last copy wins)
    cout << "by value-result, f(d, d) with d = 5: d = " << d << "  (would be " << x
         << " if copied out in the other order)\n";
}
