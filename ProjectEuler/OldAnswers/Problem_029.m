% This problem can probably be done through prime factorization. Yeah, I
% see - two numbers each of the form a^b will not be the same unless a1 and
% a2 are different powers of the same integer (including the first power).
% Thus if we want different values we could just take all the powers of the
% base integer, including all the powers the higher ones could reach.
checked=zeros(1,100);
combinations=0;
for a=2:100
    if checked(a)==0
        power=1;
        while a^power<=100
            checked(a^power)=1;
            power=power+1;
        end
        % Let i=1:power-1, j=2:100. How many different combinations of i*j
        % are there?
        for i=1:power-1
            for j=2:100
                add=true;
                % Make sure it hasn't been counted before.
                for k=1:i-1
                    if mod(i*j,k)==0&&i*j/k<=100
                        add=false;
                    end
                end
                if add
                    combinations=combinations+1;
                end
            end
        end
    end
end
combinations