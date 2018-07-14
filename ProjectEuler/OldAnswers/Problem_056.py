def digitSum(num):
    return sum([int(i) for i in str(num)])

maxSum=0
for a in range(100):
    for b in range(100):
        newSum=digitSum(a**b)
        if newSum>maxSum:
            maxSum=newSum
print maxSum
