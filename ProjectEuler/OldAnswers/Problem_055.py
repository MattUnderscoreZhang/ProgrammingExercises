LychrelNums=9999
for n in range(1,10000):
    for i in range(50):
        n=n+int(''.join(reversed(str(n))))
        if n==int(''.join(reversed(str(n)))):
            LychrelNums-=1
            break
print LychrelNums
