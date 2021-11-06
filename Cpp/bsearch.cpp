#include <stdlib.h>
#include <iostream>
using namespace std;

int intcmp(const void* a, const void* b) {
    return (*(int*)a - *(int*)b);
}

int main(int argc, char* argv[]) {
    int values[] = {100, 123, 5334, 23, 53, 99};
    qsort(values, 6, sizeof(int), intcmp);
    int search_values[] = {123, 23, 55, 128, 100, 33, 99};
    for (int search_value : search_values) {
        int* value_pointer = (int*)bsearch(&search_value, values, 6, sizeof(int), intcmp);
        if (value_pointer == NULL)
            cout << search_value << " not in array" << endl;
        else
            cout << search_value << " in array" << endl;
    }
    return 0;
}
