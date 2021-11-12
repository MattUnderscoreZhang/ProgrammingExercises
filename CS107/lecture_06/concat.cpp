#include <iostream>
using namespace std;

/**
 * Traverses a properly structured list, and returns the ordered
 * concatenation of all strings, including those in nested sublists.
 *
 * When applied to the two lists drawn above, the following strings
 * would be returned:
 *
 * ConcatAll(gameThree) would return "YankeesDiamondbacks"
 * ConcatAll(nestedNumbers) would return "onethreesix"
 */

typedef enum {
    Integer, String, List, Nil
} nodeType;

typedef struct {
    nodeType type;
    int content;
} integerEndNode;

typedef struct {
    nodeType type;
    char* content;
} stringEndNode;

typedef struct {
    nodeType type;
} nilEndNode;

typedef struct {
    nodeType type;
    nodeType* content;
    nodeType* nextNode;
} listNode;

char* ConcatStrings(const char* string_a, const char* string_b) {
    char* combination = (char*)malloc(strlen(string_a) + strlen(string_b));
    strcpy(combination, string_a);
    strcat(combination, string_b);
    return combination;
}

char* ConcatAll(nodeType *node) { 
    switch (*node) {
        case String: return *(char**)(node + 2); // all memory indices count by 2's for some reason due to structs
        case Integer:
        case Nil: return strdup("");
        case List: {
            char* result = ConcatAll(*(nodeType**)(node + 2));
            if (*(nodeType**)(node + 4) != NULL) {
                char* next_node_string = ConcatAll(*(nodeType**)(node + 4));
                result = ConcatStrings(result, next_node_string);
                free(next_node_string);
            }
            return result;
        }
    }
}

void test_1() {
    // (Yankees 2 Diamondbacks 1)
    nilEndNode endNode0 = (nilEndNode){Nil};
    integerEndNode endNode1 = (integerEndNode){Integer, 1};
    stringEndNode endNode2 = (stringEndNode){String, strdup("Diamondbacks")};
    integerEndNode endNode3 = (integerEndNode){Integer, 2};
    stringEndNode endNode4 = (stringEndNode){String, strdup("Yankees")};
    listNode node0 = (listNode){List, &endNode0.type, NULL};
    listNode node1 = (listNode){List, &endNode1.type, &node0.type};
    listNode node2 = (listNode){List, &endNode2.type, &node1.type};
    listNode node3 = (listNode){List, &endNode3.type, &node2.type};
    listNode node4 = (listNode){List, &endNode4.type, &node3.type};
    nodeType* gameThree = &node4.type;

    char* result = ConcatAll(gameThree);
    cout << result << endl;
    free(result);
}

void test_2() {
    // (one (2 (three 4)) 5 six)
    nilEndNode endNode0 = (nilEndNode){Nil};
    stringEndNode endNode1 = (stringEndNode){String, strdup("six")};
    integerEndNode endNode2 = (integerEndNode){Integer, 5};
    nilEndNode endNode3_0_0 = (nilEndNode){Nil};
    integerEndNode endNode3_0_1 = (integerEndNode){Integer, 4};
    stringEndNode endNode3_0_2 = (stringEndNode){String, strdup("three")};
    integerEndNode endNode3_1 = (integerEndNode){Integer, 2};
    stringEndNode endNode4 = (stringEndNode){String, strdup("one")};
    listNode node0 = (listNode){List, &endNode0.type, NULL};
    listNode node1 = (listNode){List, &endNode1.type, &node0.type};
    listNode node2 = (listNode){List, &endNode2.type, &node1.type};
    listNode node3_0_0 = (listNode){List, &endNode3_0_0.type, NULL};
    listNode node3_0_1 = (listNode){List, &endNode3_0_1.type, &node3_0_0.type};
    listNode node3_0_2 = (listNode){List, &endNode3_0_2.type, &node3_0_1.type};
    listNode node3_1 = (listNode){List, &node3_0_2.type, NULL};
    listNode node3 = (listNode){List, &node3_1.type, &node2.type};
    listNode node4 = (listNode){List, &endNode4.type, &node3.type};
    nodeType* nestedNumbers = &node4.type;

    char* result = ConcatAll(nestedNumbers);
    cout << result << endl;
    free(result);
}

int main(int argc, char* argv[]) {
    test_1();
    test_2();
}
