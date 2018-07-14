% Kinda slow.
longestPrimeStreak=0;
product=0;
for a=-999:999
    for b=-999:999
        n=1;
        streak=0;
        while true
            testSubject=n^2+a*n+b;
            if (testSubject)<0
                break;
            elseif isprime(testSubject)
                n=n+1;
                streak=streak+1;
            else
                if streak>longestPrimeStreak
                    longestPrimeStreak=streak;
                    product=a*b;
                end
                break;
            end
        end
    end
end
product