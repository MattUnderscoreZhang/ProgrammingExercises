% A palindrome number with six digits is divisible by 11. I'll only check
% 6 digit numbers, and if nothing comes up then I'll check the 5 digits.
% EDIT: This was a dumb way of checking for being a palindrome. I should
% have converted into a string and reversed.
largestPalindrome=0;
i=1001;
j=1000;
while i>=100
    j=1000;
    i=i-11;
    while j>=100
        j=j-1;
        N=i*j;
        d1=mod(N,10);
        d6=floor(N/100000);
        if d1~=0&&d1==d6
            d2=floor(mod(N,100)/10);
            d5=floor(mod(N,100000)/10000);
            if d2==d5
                d3=floor(mod(N,1000)/100);
                d4=floor(mod(N,10000)/1000);
                if d3==d4
                    if N>largestPalindrome
                        largestPalindrome=N;
                    end
                    j=100;
                end
            end
        end
    end
end
largestPalindrome