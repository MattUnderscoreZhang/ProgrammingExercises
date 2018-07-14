from math import factorial

total=0
for n in range(1,101):
    for r in range(int(n/2)+1):
        if factorial(n)/(factorial(r)*factorial(n-r))>10**6:
            total+=(n+1)-2*r
            break
print total
