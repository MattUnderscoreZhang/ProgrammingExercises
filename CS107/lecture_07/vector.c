#include "vector.h"
#include <search.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>

void VectorNew(vector *v, int elemSize, VectorFreeFunction freeFn, int initialAllocation)
{
    v->maxElems = initialAllocation;
    v->nElems = 0;
    v->elemSize = elemSize;
    v->elems = malloc(initialAllocation * elemSize);
    v->freeFn = freeFn;
}

void VectorDispose(vector *v)
{
    if (v->freeFn != NULL) {
        for (int i=0; i<v->nElems; i++) {
            v->freeFn(VectorNth(v, i));
        }
    }
    v->nElems = 0;
}

int VectorLength(const vector *v)
{
    return v->nElems;
}

void *VectorNth(const vector *v, int position)
{
    return ((char*)v->elems) + v->elemSize * position;
}

void VectorReplace(vector *v, const void *elemAddr, int position)
{
    assert(position >= 0 && position < v->nElems);
    if (v->freeFn != NULL)
        v->freeFn(VectorNth(v, position));
    memcpy(VectorNth(v, position), elemAddr, v->elemSize);
}

void VectorInsert(vector *v, const void *elemAddr, int position)
{
    assert(position >= 0 && position <= v->nElems);
    VectorAppend(v, elemAddr);
    memmove(VectorNth(v, position+1), VectorNth(v, position), v->elemSize * (v->nElems - position - 1));
    memcpy(VectorNth(v, position), elemAddr, v->elemSize);
}

void VectorAppend(vector *v, const void *elemAddr)
{
    if (v->nElems >= v->maxElems) {
        v->maxElems *= 2;
        v->elems = realloc(v->elems, v->maxElems * v->elemSize);
    }
    memcpy(VectorNth(v, v->nElems), elemAddr, v->elemSize);
    v->nElems++;
}

void VectorDelete(vector *v, int position)
{
    assert(position >= 0 && position < v->nElems);
    if (v->freeFn != NULL)
        v->freeFn(VectorNth(v, position));
    v->nElems--; 
    memmove(VectorNth(v, position), VectorNth(v, position+1), v->elemSize * (v->nElems - position));
}

void VectorSort(vector *v, VectorCompareFunction compare)
{
    qsort(v->elems, v->nElems, v->elemSize, compare);
}

void VectorMap(vector *v, VectorMapFunction mapFn, void *auxData)
{
    assert(mapFn != NULL);
    for (int i=0; i<v->nElems; i++) {
        mapFn(VectorNth(v, i), auxData);
    }
}

static const int kNotFound = -1;
int VectorSearch(const vector *v, const void *key, VectorCompareFunction searchFn, int startIndex, bool isSorted)
{
    assert(startIndex >= 0 && startIndex <= v->nElems);
    assert(key != NULL);
    assert(searchFn != NULL);
    void* searchBase = VectorNth(v, startIndex);
    size_t nSearchElems = v->nElems - startIndex;
    void* foundElem = 0;
    if (isSorted)
        foundElem = bsearch(key, searchBase, nSearchElems, v->elemSize, searchFn);
    else {
        int* nSearchElemsPtr = &nSearchElems;
        foundElem = lfind(key, searchBase, nSearchElemsPtr, v->elemSize, searchFn);
    }
    if (foundElem != NULL) {
        int index = ((char*)foundElem - (char*)v->elems) / v->elemSize;
        return index;
    }
    else
        return -1;
} 
