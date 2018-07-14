circularNumbers=0

# What? Python doesn't have an isprime() function!?!
def isPrime(n):
    for i in range(2,int(n**0.5)+1):
        if n%i==0:
            return False
    return True

for num in range(2,10**6):
    if isprime(num):
        Num=str(num)
        circular=True
        for i in range(len(Num)-1):
            Num=Num[1:]+Num[0]
            if not isprime(int(Num)):
                circular=False
                break
        if circular:
            print num
            circularNumbers+=1
        
print circularNumbers
