% First find all abundant numbers below 28112.
abundant=zeros(1,28111);
for num=1:28111
    tempSum=0;
    for i=floor(num/2):-1:1
        if mod(num,i)==0
            tempSum=tempSum+i;
            if tempSum>num
                abundant(num)=1;
                break;
            end
        end
    end
end
% Check if these numbers are the sum of abundant ones.
sum=0;
for num=1:28123
    notWriteable=true;
    for i=1:num/2
        if abundant(i)==1&&abundant(num-i)==1
            notWriteable=false;
        end
    end
    if notWriteable
        sum=sum+num;
    end
end
sum