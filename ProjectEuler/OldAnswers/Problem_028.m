% Starting from 1, add 2 to get to the next number, then 2 again. The
% pattern goes like 2(x4), 4(x4), 6(x4), etc. We want to go until 1000(x4).
% There's probably a closed-form solution to this, but meh.
sum=1;
num=1;
for step=2:2:1000
    sum=sum+num*4+step*10;
    num=num+step*4;
end
sum