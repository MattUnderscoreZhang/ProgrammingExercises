% The largest possible n-digit candidate is n*9^5, which is a six-digit
% number when n=6 and when n=7. Thus the largest candidate is 6*9^5=354294.
sum=0;
for digits=2:5
    for num=10^(digits-1):10^digits-1
        check=0;
        for digit=1:digits
            check=check+floor(mod(num,10^(digit))/(10^(digit-1)))^5;
        end
        if check==num
            sum=sum+num;
        end
    end
end
digits=6;
for num=10^(5):354294
    check=0;
    for digit=1:digits
        check=check+floor(mod(num,10^(digit))/(10^(digit-1)))^5;
    end
    if check==num
        sum=sum+num;
    end
end
sum