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
        case String: return *(char**)(node + 2); // this doesn't work right because of padding or something
        case Integer:
        case Nil: return strdup("");
        case List: {
            char* result = ConcatAll(node + 1);
            if (node + 2 != NULL) {
                char* next_node_string = ConcatAll(node + 2);
                result = ConcatStrings(result, next_node_string);
                free(next_node_string);
            }
            return result;
        }
    }
}

int main(int argc, char* argv[]) {
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
    cout << ConcatAll(&endNode2.type) << endl;
    free(result);

    //cout << sizeof(nodeType) << endl;
    //cout << &(endNode2.type) << endl;
    //cout << &(endNode2.type) + 2 << endl;
    //cout << &(endNode2.content) << " " << endNode2.content << endl;

    //listNode node0 = listNode{List, &nilEndNode{Nil}.type, NULL};
    //listNode node1 = listNode{List, &stringEndNode{String, "six"}.type, &node0.type};
    //listNode node2 = listNode{List, &integerEndNode{Integer, 5}.type, &node1.type};
    //listNode node3 = listNode{List, &integerEndNode{Integer, 2}.type, &node2.type};
    //listNode node4 = listNode{List, &stringEndNode{String, "Yankees"}.type, &node3.type};
    //listNode node5 = listNode{List, &stringEndNode{String, "Yankees"}.type, &node3.type};
    //listNode node6 = listNode{List, &stringEndNode{String, "Yankees"}.type, &node3.type};
    //nodeType* gameThree = &node4.type;
    //{one {2 {three 4}} 5 six};
    //cout << ConcatAll(nestedNumbers) << endl;
}
