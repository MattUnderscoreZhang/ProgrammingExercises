% a and b are the first two Fibonacci numbers.
a=1;
b=2;
c=2;
sum=0;
% We use this loop to calculate the even Fibonacci numbers c. Then we
% continue the process by setting b equal to the new c and a equal to the
% Fibonacci number before c. We can do this because every third F. number
% is even.
while c<=4*10^6
    sum=sum+c;
    c=2*a+3*b;
    a=a+2*b;
    b=c;
end
sum