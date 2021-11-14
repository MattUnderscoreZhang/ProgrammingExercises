#include <iostream>
#include <algorithm>
using namespace std;

int main(int argc, char* argv[]) {
    int a1 = 10, b1 = 20;
    cout << a1 << " " << b1 << " " << &a1 << " " << &b1 << endl;
    swap(a1, b1);
    cout << a1 << " " << b1 << " " << &a1 << " " << &b1 << endl;

    cout << endl;

    int a4 = 10, b4 = 20;
    int *c4 = &a4, *d4 = &b4;
    cout << a4 << " " << b4 << " " << &a4 << " " << &b4 << endl;
    cout << c4 << " " << d4 << " " << &c4 << " " << &d4 << endl;
    swap(*c4, *d4);
    cout << a4 << " " << b4 << " " << &a4 << " " << &b4 << endl;
    cout << c4 << " " << d4 << " " << &c4 << " " << &d4 << endl;
}
