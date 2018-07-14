# There are the fewest octagonal numbers, so let's start with those.

from copy import deepcopy

candidates=[]
n=1
while True:
    octagonalNum=n*(3*n-2)
    if len(str(octagonalNum))==4:
        candidates.append(octagonalNum)
    elif len(str(octagonalNum))>4:
        break

# Check for heptagonal numbers.
oldCandidates=deepcopy(candidates)
candidates=[]
for num in oldCandidates:
    header=int(str(num)[2:4])*100
    for i in range(10,100):
        if(((header+i)*40+9)**.5+3)%10==0:
            candidates.append([num,header+i])
