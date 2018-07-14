% Simple. All the ones starting 0 go first. There are 9! of them. Then etc.
digit=zeros(1,10);
locked=0;
for i=1:10
    digit(i)=floor(((10^6-1)-locked)/factorial(10-i));
    locked=locked+digit(i)*factorial(10-i);
end
digit
% Note this program doesn't output the actual number. It tells you which
% digit to take at each place, out of the ones that are left. The actual
% number is 2783915460.