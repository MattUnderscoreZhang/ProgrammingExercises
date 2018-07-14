# Tried algebra, didn't work. Time for brute force! Checking whether a number
# is pentagonal is just a matter of checking the integer-ness of the inverse.

from math import sqrt
found=False
n=0
while not found:
    n+=1
    nNum=n*(3*n-1)/2
    for m in range(1,n):
        sum=nNum+m*(3*m-1)/2
        difference=nNum-m*(3*m-1)/2
        if ((sqrt(24*sum+1)+1)/6)%1==0 and ((sqrt(24*difference+1)+1)/6)%1==0:
            lowestD=difference
            found=True
print lowestD

# I just assumed this gave the lowest number. You can actually prove it because
# the pentagonal numbers become less dense.
