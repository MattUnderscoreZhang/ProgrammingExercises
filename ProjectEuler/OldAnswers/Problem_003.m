% This is a pretty straightforward method, but I can't think of any better
% one. You just start from the middle and decrease until you find a prime
% divisor.
N=600851475143;
largestPrime=1;
% Note that the indices of a for loop are fixed at the time the loop is
% initiated. To have changing bounds you need a while loop.
i=floor(sqrt(N));
while i>1
    divisible=mod(N,i)==0;
    if divisible
        if isprime(N/i)
            largestPrime=N/i;
            i=1;
        elseif isprime(i)
            largestPrime=i;
            i=1;
        end
    end
    i=i-1;
end
largestPrime