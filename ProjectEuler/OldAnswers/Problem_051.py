# First try three digits. This includes both varying one digit while holding a
# two-digit number fixed, and varying two digits while holding a one-digit
# number fixed. Continue like that.

from myFunctions import isprime

def checkFamily(fixedRoot,insertions,digits):
    family=[]
    insert=0
    for i in range(len(insertions)):
        if insertions[i]==1:
            insert+=10**i
            fixedRoot+=9*10**i*int(fixedRoot/(10**i))
    for n in range(10):
        family.append(fixedRoot+insert*n)
    familyPrimes=[i for i in family if isprime(i) and i>10**(digits-1)]
    if len(familyPrimes)>=8:
        return min(familyPrimes)
    return 0

digits=5
found=False
while not found:
    for fixedDigits in range(1,digits):
        changingDigits=digits-fixedDigits
        for fixedRoot in range(10**(fixedDigits-1),10**fixedDigits-1):
            # Create every possible permutation of places to insert digits.
            # First permutation.
            insertions=[0]*digits
            for i in range(changingDigits):
                insertions[i]=1
            maxInsertions=[1]*digits
            for i in range(fixedDigits):
                maxInsertions[i]=0
            while True:
                # Insert and check for 8-prime family.
                check=checkFamily(fixedRoot,insertions,digits)
                if check!=0:
                    print check
                    found=True
                # Increment.
                for i in range(digits):
                    if insertions[i]==1:
                        # Find next empty spot up, promote, send others back down.
                        for j in range(i+1,digits):
                            if insertions[j]==0:
                                insertions[j]=1
                                for k in range(j):
                                    insertions[k]=0
                                for k in range(j-i-1):
                                    insertions[k]=1
                                break
                        break
                if insertions==maxInsertions:
                    break
    digits+=1

# Does not print the answer directly, take the smaller one. Also not so fast.
