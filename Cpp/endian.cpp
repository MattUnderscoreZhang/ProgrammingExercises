#include <iostream>
using namespace std;


int main(int argc, char* argv[]) {
    int number = 65;
    cout << number << endl;
    cout << *(&number) << endl;
    char* pointer = (char*) &number;
    cout << pointer[0] << endl; // prints A here = little-endian
    cout << pointer[1] << endl;
    cout << pointer[2] << endl;
    cout << pointer[3] << endl; // prints A here = big-endian
}
