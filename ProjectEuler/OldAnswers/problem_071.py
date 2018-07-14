# Matt Zhang
# Last Updated 2014-01-12
# Python 3.3.3

# This problem's a lot simpler than it looks at first.

def compareFractions(fraction1,fraction2):
    numerator1=fraction1[0]*fraction2[1]
    numerator2=fraction1[1]*fraction2[0]
    if numerator1>numerator2:
        return 1
    elif numerator2>numerator1:
        return 2
    else:
        return 0

leftBound=[2,5]

from fractions import gcd

for denominator in range(8,1000001):
    numerator=int(denominator/7*3)
    if gcd(numerator,denominator)>1:
        continue
    if compareFractions(leftBound,[numerator,denominator])==2:
        leftBound=[numerator,denominator]

print(leftBound)
