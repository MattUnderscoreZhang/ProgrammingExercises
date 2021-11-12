#include <stdio.h>
#include <string.h>
#include <assert.h>

typedef enum {
    Integer, String, List, Nil
} nodeType;

typedef struct {
    nodeType type;
    char* content;
} stringEndNode;

int main(int argc, char* argv[]) {
    stringEndNode node = (stringEndNode){String, strdup("Testing")};
    printf("%lu\n", sizeof(nodeType));
    printf("%p\n", &(node.type));
    printf("%p\n", &(node.type) + 1); // Why aren't these the same?
    printf("%p\n", &(node.content)); // Why aren't these the same?

    printf("%s\n", *(char**)(&(node.type) + 2)); // Oh, struct probably has an index for each element
    printf("%s\n", *(&(node.type) + 2));
}
