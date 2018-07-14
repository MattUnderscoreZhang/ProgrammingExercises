from fractions import gcd

protoNumer=[5]*1000
protoDenom=[2]*1000
for i in range(1,1000):
    numer=protoNumer[i-1]
    denom=protoDenom[i-1]
    temp=numer
    protoNumer[i]=denom
    protoDenom[i]=temp
    protoNumer[i]+=2*protoDenom[i]
protoNumer=[protoNumer[i]-protoDenom[i] for i in range(1000)]
numer=[protoNumer[i]/gcd(protoNumer[i],protoDenom[i]) for i in range(1000)]
denom=[protoDenom[i]/gcd(protoNumer[i],protoDenom[i]) for i in range(1000)]
total=0
for i in range(1000):
    if len(str(numer[i]))>len(str(denom[i])):
        total+=1

print total
