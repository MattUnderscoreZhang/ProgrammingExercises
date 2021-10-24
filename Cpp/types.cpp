#include <iostream>
#include <string>
using namespace std;


void floatToBinary(float f, string& str) {
    union { float f; uint32_t i; } u;
    u.f = f;
    str.clear();

    for (int i = 0; i < 32; i++)
    {
        if (u.i % 2)  str.push_back('1');
        else str.push_back('0');
        u.i >>= 1;
    }

    // Reverse the string since now it's backwards
    string temp(str.rbegin(), str.rend());
    str = temp;
}


int main() {
    float a = 2.3;
    decltype(a) b;
    b = a*2;
    cout << b << endl;

    string c = "Hello"
               " World";
    cout << c << endl;

    float d = 7.0000012312345;
    string d_bits;
    floatToBinary(d, d_bits);
    cout << d_bits << endl;
    short e = *(short*)&d;  // Mac is little-endian
    cout << e << endl;
}
