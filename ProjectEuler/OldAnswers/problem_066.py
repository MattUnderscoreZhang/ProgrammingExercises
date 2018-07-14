# Matt Zhang
# Last Updated 2014-01-11
# Python 3.3.3

from gmpy import is_square

'''DCandidates=range(2,1001)
DCandidates=[i for i in DCandidates if not is_square(i)]
highestSquare=0
highestD=0
y=0
while len(DCandidates)>0:    
    y+=1
    for D in DCandidates:
        num=D*y**2+1
        if is_square(num):
            if num>highestSquare:
                highestSquare=num
                highestD=D
            print('Eliminated',D,'-',len(DCandidates),'candidates remaining. y is at',y)
            DCandidates.remove(D)
print('D =',highestD)'''

# This problem can not be brute forced. After looking online, it seems to be of the
# form of something called Pell's equation.
