# Hexagonal numbers increase the fastest, so let's look at those.

from math import sqrt
n=143
while True:
    n+=1
    hex=n*(2*n-1)
    if ((1+sqrt(1+24*hex))/6)%1==0 and ((-1+sqrt(1+8*hex))/2)%1==0:
        print hex
        break
