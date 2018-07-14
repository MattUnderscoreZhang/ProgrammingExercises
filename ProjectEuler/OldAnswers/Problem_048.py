# (A*B)%100=(A%100)*(B%100) and so on, for any power of 10.

sum=0
digits=1000
for i in range(1,digits+1):
    product=1
    for j in range(i):
        product=(product%(10**10))*i
    sum+=product
    sum=sum%(10**10)
print sum
