from numpy import zeros

hits=list(zeros(1001))
for a in range(1,1000):
    for b in range(1,a+1):
        c=(a**2+b**2)**.5
        length=int(a+b+c)
        if length>1000:
            break
        if c%1==0:
            hits[length]+=1

# index() only returns the first hit.
print hits.index(max(hits))
