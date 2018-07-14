% I could do something complicated involving prime factorization, but I
% won't. Either way, this problem doesn't run so fast but it's okay. To
% make it faster easily I could stop checking amicability once the number
% is obviously too large.
% EDIT: Changed it. Runs much faster now.
sumDivisors=zeros(1,9999);
amicableSum=0;
for i=2:9999
    % Find sum of proper divisors if it hasn't been found before.
    if sumDivisors(i)==0
        for j=1:i/2
            if mod(i,j)==0
                sumDivisors(i)=sumDivisors(i)+j;
            end
        end
    end
    % Check for amicability.
    k=sumDivisors(i);
    tempSum=0;
    if k<10000
        if sumDivisors(k)==0
            for j=1:k/2
                if mod(k,j)==0
                    sumDivisors(k)=sumDivisors(k)+j;
                end
            end
        end
        tempSum=sumDivisors(k);
    else
        for j=floor(k/2):-1:1
            if mod(k,j)==0
                tempSum=tempSum+j;
                if tempSum>i
                    break;
                end
            end
        end
    end
    % Add only the original number if it's amicable.
    if (tempSum==i)&&(i~=k)
        amicableSum=amicableSum+i;
    end
end
amicableSum