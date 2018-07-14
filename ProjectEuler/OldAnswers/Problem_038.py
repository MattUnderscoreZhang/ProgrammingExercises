from numpy import *

max=0
for n in range(2,10):
    integers=array([i for i in range(1,n+1)])
    for i in range(1,100000):
        concat=''.join([str(j) for j in integers*i])
        if len(concat)>9:
            break
        elif ''.join(sorted(concat))=='123456789' and int(concat)>max:
            max=int(concat)

print max
