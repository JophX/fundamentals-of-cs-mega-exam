#include <iostream>

class Stack {               // ENCAPSULATION: data + operations in one unit
private:                    // INFORMATION HIDING: invisible from outside
    int data[100];
    int top = -1;
public:                     // the interface: the only way in
    void push(int x) { if (top < 99) data[++top] = x; }
    int  pop()       { return data[top--]; }
    bool isEmpty()   { return top == -1; }
};

int main() {
    Stack s;
    s.push(1); s.push(2); s.push(3);
    while (!s.isEmpty()) std::cout << s.pop() << " ";
    std::cout << "\n";
#ifdef CHEAT
    s.top = 50;              // try to break the stack from outside
#endif
}
