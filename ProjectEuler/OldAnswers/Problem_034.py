# Since 9!=362880, the largest candidate number is 7*9!=2540160, which has
# 7 digits. First calculate all the factorials to save time.
import math
from random import randint
from copy import deepcopy
factorials=[math.factorial(0),math.factorial(1),math.factorial(2),math.factorial(3),math.factorial(4),math.factorial(5),math.factorial(6),math.factorial(7),math.factorial(8),math.factorial(9)]
sum=0
for num in range(10,1000):
    number=str(num)
    testSum=0
    for i in range(0,len(number)):
        testSum+=factorials[int(number[i])]
        if testSum==num:
            sum+=num
# For numbers with more than 3 digits, it starts taking too long to look at
# all of them. So instead we pick someplace random to start, see if it has
# the right number of digits, then keep dividing in half until we find a
# place.
for digits in range(4,8):
    # How many of each digit there is. That is, how many 0's, how many 1's, etc.
    numDigits=[0]*10
    for i in range(0,digits):
        numDigits[i]=1
    while True:
        testSum=0
        for i in range(0,10):
            testSum+=numDigits[i]*factorials[i]
        if len(str(testSum))!=digits:
            # Randomize new test number.
            numDigits=[0]*10
            for i in range(0,digits):
                randDigit=randint(0,9) # Inclusive.
                numDigits[randDigit]+=1
        else:
            testNum=''
            for i in range(0,10):
                for j in range(0,numDigits[i]):
                    testNum+=str(i)
            if ''.join(sorted(str(testSum)))==testNum:
                sum+=testSum
            # Look up. Deep copy to prevent creating a pointer.
            holdMyDigits=deepcopy(numDigits)
            while True:
                testSum=0
                # Next largest number.
                for i in range(0,9):
                    if numDigits[i]!=0:
                        numDigits[0]=numDigits[i]-1
                        if i!=0:
                            numDigits[i]=0
                        numDigits[i+1]+=1
                        break
                for i in range(0,10):
                    testSum+=numDigits[i]*factorials[i]
                numLength=len(str(testSum))
                # See if the sum matches the digits. If so, add the sum.
                if numLength==digits:
                    # Check match.
                    testNum=''
                    for i in range(0,10):
                        for j in range(0,numDigits[i]):
                            testNum+=str(i)
                    if ''.join(sorted(str(testSum)))==testNum:
                        sum+=testSum
                elif numLength>digits:
                    break
                if numDigits[9]==digits:
                    break
            # Look down.
            numDigits=deepcopy(holdMyDigits)
            while True:
                testSum=0
                for i in range(1,10):
                    if numDigits[i]!=0:
                        numDigits[i-1]=1+numDigits[0]
                        if i!=1:
                            numDigits[0]=0
                        numDigits[i]-=1
                        break
                for i in range(0,10):
                    testSum+=numDigits[i]*factorials[i]
                numLength=len(str(testSum))
                # See if the sum matches the digits. If so, add the sum.
                if numLength==digits:
                    # Check match.
                    testNum=''
                    for i in range(0,10):
                        for j in range(0,numDigits[i]):
                            testNum+=str(i)
                    if ''.join(sorted(str(testSum)))==testNum:
                        sum+=testSum
                elif numLength<digits:
                    break
                if numDigits[0]==digits:
                    break
            break
print 'sum='+str(sum)
