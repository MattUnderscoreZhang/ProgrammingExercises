#include "hashset.h"
#include <assert.h>
#include <stdlib.h>
#include <string.h>
#include "vector.h"

void HashSetNew(hashset *h, int elemSize, int numBuckets,
		HashSetHashFunction hashfn, HashSetCompareFunction comparefn, HashSetFreeFunction freefn)
{
    assert(elemSize > 0);
    assert(numBuckets > 0);
    assert(hashfn != NULL);
    assert(comparefn != NULL);

    h->elemSize = elemSize;
    h->nBuckets = numBuckets;
    h->hashFn = hashfn;
    h->compareFn = comparefn;
    VectorNew(&h->elemVectors, sizeof(vector), NULL, numBuckets);
    for (int i=0; i<h->nBuckets; i++) {
        vector elemVector;
        VectorNew(&elemVector, h->elemSize, freefn, 4);
        VectorInsert(&h->elemVectors, &elemVector, i);
    }
    h->nElems = 0;
}

void HashSetDispose(hashset *h)
{
    for (int i=0; i<h->nBuckets; i++) {
        VectorDispose(VectorNth(&h->elemVectors, i));
    }
    VectorDispose(&h->elemVectors);
    h->nElems = 0;
}

int HashSetCount(const hashset *h)
{
    return h->nElems;
}

void HashSetMap(hashset *h, HashSetMapFunction mapfn, void *auxData)
{
    assert(mapfn != NULL);
    for (int i=0; i<h->nBuckets; i++) {
        vector* elemVector = VectorNth(&h->elemVectors, i);
        for (int j=0; j<VectorLength(elemVector); j++) {
            mapfn(VectorNth(elemVector, j), auxData);
        }
    }
}

void HashSetEnter(hashset *h, const void *elemAddr)
{
    assert(elemAddr != NULL);
    int bucket = h->hashFn(elemAddr, h->nBuckets);
    assert(bucket >= 0 && bucket < h->nBuckets);
    vector* elemVector = VectorNth(&h->elemVectors, bucket);
    int position = VectorSearch(elemVector, elemAddr, h->compareFn, 0, false);
    if (position != -1) {
        VectorReplace(elemVector, elemAddr, position);
    }
    else
        VectorAppend(elemVector, elemAddr);
    h->nElems++;
}

void *HashSetLookup(const hashset *h, const void *elemAddr)
{
    assert(elemAddr != NULL);
    int bucket = h->hashFn(elemAddr, h->nBuckets);
    assert(bucket >= 0 && bucket < h->nBuckets);
    vector* elemVector = VectorNth(&h->elemVectors, bucket);
    int position = VectorSearch(elemVector, elemAddr, h->compareFn, 0, false);
    if (position != -1)
        return VectorNth(elemVector, position);
    else
        return NULL;
}
