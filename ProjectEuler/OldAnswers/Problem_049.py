from itertools import permutations
from myFunctions import isprime

def primePermute(num):
    permute=[int(''.join(i)) for i in list(permutations(str(num)))]
    answer=[]
    for i in permute:
        if i not in answer and isprime(i) and i>1000:
            answer.append(i)
    return sorted(answer)

def threeChain(listNums):
    for i in range(len(listNums)):
        for j in range(i+1,len(listNums)):
            if (2*listNums[j]-listNums[i]) in listNums:
                print str(listNums[i])+str(listNums[j])+str(2*listNums[j]-listNums[i])
                return True
    return False

candidates=[]
for a in range(10):
    for b in range(10):
        for c in range(10):
            for d in range(1,min(a,b,c)+1):
                num=d*1000+c*100+b*10+a
                if isprime(num):
                    if threeChain(primePermute(num)):
                        candidates.append(num)

# Doesn't return in the exact form, but the answer's there.
