% At each node on the right side of the grid, you only have one option,
% that is to go down. On the bottom you only have the option to go right.
% At any other node, the total choices you have is equal to the sum of the
% options of the node on the right and the options of the node below.
options=zeros(21);
for i=1:21
    options(21,i)=1;
    options(i,21)=1;
end
for i=20:-1:1
    for j=20:-1:1
        options(i,j)=options(i+1,j)+options(i,j+1);
    end
end
% Matlab display is a pain. It can't even go past 17 decimal places!
sprintf('%f',options(1,1))