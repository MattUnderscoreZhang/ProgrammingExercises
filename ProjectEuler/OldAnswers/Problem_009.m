for c=335:997
    for b=2:999-c
        a=1000-b-c;
        if a^2+b^2==c^2
            a*b*c
        end
    end
end