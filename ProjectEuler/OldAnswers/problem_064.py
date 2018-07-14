# Matt Zhang
# 2014-01-06
# Python 3.3.3

from math import floor,sqrt,ceil
from gmpy import is_square

oddPeriods=0
for n in range(1,10001):
    if is_square(n):
        continue
    subtractor=floor(sqrt(n))
    numerator=1
    firstSubtractor=subtractor
    firstNumerator=numerator
    period=0
    while True:
        period+=1
        denominator=(n-subtractor**2)//numerator
        integerPart=(sqrt(n)+subtractor)//denominator
        subtractor=denominator*integerPart-subtractor
        numerator=denominator
        if numerator==firstNumerator and subtractor==firstSubtractor:
            break
    if period%2==1:
        oddPeriods+=1
print(oddPeriods)
