import time

a=1
b=1
i=2
go=True
while go:
    i+=1
    c=a+b
    a=b
    b=c
    if c>=10**999:
        print c
        print i
        go=False
time.sleep(60)
