numerator=1;
denominator=1;
for i=1:9
    for num=10*i:10*(i+1)-1
        for den=i+10:10:90+i
            if num/den==mod(num,10)/floor(den/10)
                if num<den
                    numerator=numerator*num;
                    denominator=denominator*den;
                elseif den<num
                    numerator=numerator*den;
                    denominator=denominator*num;
                end
            end
        end
    end
end
% Simplify.
denominator/gcd(numerator,denominator)