% Work from the top down. Start with 2 pounds, then successively remove the
% lowest denomiation and replace it with the next lowest. Just like
% counting in binary.
denomination=[1 2 5 10 20 50 100 200];
coins=8;
division=[0 0 0 0 0 0 0 1];
combinations=1;
while division(1)~=200
    % Find the lowest denomination.
    for i=2:coins
        if division(i)~=0
            % Remove that coin.
            division(i)=division(i)-1;
            toDivide=denomination(i);
            % Remove all coins below it.
            for j=i-1:-1:1
                toDivide=toDivide+division(j)*denomination(j);
                division(j)=0;
            end
            % Divide it up.
            for j=i-1:-1:1
                division(j)=division(j)+floor(toDivide/denomination(j));
                toDivide=toDivide-division(j)*denomination(j);
            end
            combinations=combinations+1;
            break;
        end
    end
end
combinations