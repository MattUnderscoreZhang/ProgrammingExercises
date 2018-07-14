% Simple problem, no need to complicate it. Just search two terms back,
% and if a number isn't part of a longer chain that starts under a million,
% then investigate it.
chainRecord=1;
recordHolder=1;
for i=(10^6)/2-1:10^6-1
    % First term back.
    a=2*i;
    b=(i-1)/3;
    if a<10^6||(isinteger(b)&&b<10^6)
    else
        % Second term back.
        aa=2*a;
        ba=2*b;
        ab=(a-1)/3;
        bb=(b-1)/3;
        if aa<10^6||(isinteger(ba)&&ba<10^6)||(isinteger(ab)&&ab<10^6)||(isinteger(bb)&&bb<10^6)
        else
            % See how far the chain goes.
            n=i;
            chain=1;
            while n~=1
                if mod(n,2)==0
                    n=n/2;
                else
                    n=3*n+1;
                end
                chain=chain+1;
            end
            if chain>chainRecord
                chainRecord=chain;
                recordHolder=i;
            end
        end
    end
end
chainRecord
recordHolder