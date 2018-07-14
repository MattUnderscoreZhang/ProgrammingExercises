# Matt Zhang
# 2014-01-06
# Python 3.3.3

# This problem has nothing to do with convergents. Just adding a series. It's easiest
# to start backwards with the last term. The hundredth term ends on ...1,66,1,1.

from fractions import gcd

numerator=0
denominator=1
for i in range(99,0,-1):
    if (i+1)%3==0:
        n=(i+1)//3*2
    else:
        n=1
    numerator+=denominator*n
    placeholder=numerator
    numerator=denominator
    denominator=placeholder
numerator+=2*denominator
commonDenominator=gcd(numerator,denominator)
numerator=numerator//commonDenominator
denominator=denominator//commonDenominator
digits=[int(i) for i in str(numerator)]
print(sum(digits))
