def numberUniquePrimeFactors(num):
    factors=[]
    i=1
    while num>1:
        i+=1
        if num%i==0:
            num/=i
            if i not in factors:
                factors.append(i)
            i=1
    return len(factors)

num=0
while True:
    num+=4
    if numberUniquePrimeFactors(num)==4:
        if numberUniquePrimeFactors(num+2)==4:
            if numberUniquePrimeFactors(num+1)==4:
                if numberUniquePrimeFactors(num-1)==4:
                    print num-1
                    break
                elif numberUniquePrimeFactors(num+3)==4:
                    print num
                    break
        elif numberUniquePrimeFactors(num-2)==4:
            if numberUniquePrimeFactors(num-1)==4:
                if numberUniquePrimeFactors(num+1)==4:
                    print num-2
                    break
                elif numberUniquePrimeFactors(num-3)==4:
                    print num-3
                    break

