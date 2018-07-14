# Matt Zhang
# Last Updated 2014-01-11
# Python 3.3.3

import numpy

# Read triangle.
triangleFile=open('067_data.txt')
triangleData=triangleFile.readlines()
triangleFile.close()
triangle=[]
for line in triangleData:
    line=line.strip('\n')
    triangle.append(line.split(' '))
triangle=[[int(value) for value in line] for line in triangle]
# Find largest values on way down.
largestSum=[[triangle[0][0]]]
for line in range(1,len(triangle)):
    sumLine=[]
    for value in range(len(triangle[line])):
        leftBranchSum=rightBranchSum=0
        if value>0:
            leftBranchSum=largestSum[line-1][value-1]
        if value<len(triangle[line])-1:
            rightBranchSum=largestSum[line-1][value]
        sumLine.append(triangle[line][value]+max(leftBranchSum,rightBranchSum))
    largestSum.append(sumLine)
# Answer
print(max(largestSum[len(triangle)-1]))
