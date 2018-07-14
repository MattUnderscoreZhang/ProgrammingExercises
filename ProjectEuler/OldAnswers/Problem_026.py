# The hard part about this problem is that some numbers don't start
# repeating until after a few digits. I'm not doing this in the most efficient
# way.

from decimal import *

getcontext().prec=3000
highestRepeater=0
mostRepeats=0
for i in range(1,1000):
    num=str(Decimal(1)/i)
    for j in range(1,1500):
        if num[10:10+j]==num[10+j:10+2*j]:
            if j>mostRepeats:
                mostRepeats=j
                highestRepeater=i
            break

print str(highestRepeater)+' has the most repeating digits, at '+str(mostRepeats)+'.'
