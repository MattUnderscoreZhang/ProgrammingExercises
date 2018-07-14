# Brute force all the way!

arr=[]
with open('Problem_018_data.txt') as data:
    for line in data:
        arr.append(line.rstrip('\n').split(' '))
arr=[[int(j) for j in i] for i in arr]
maxTotal=0
for i in range(2**14):
    total=0
    d=0
    for j in range(15):
        total+=arr[j][d]
        if int((i%(2**(j+1)))/(2**j))==1:
            d+=1
    if total>maxTotal:
        maxTotal=total
print maxTotal
