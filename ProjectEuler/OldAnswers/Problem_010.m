sum=2;
for i=1:2:2*10^6
    if isprime(i)
        sum=sum+i;
    end
end
sum