# Matt Zhang
# 2014-01-03
# Python 3.3.3

# This would go a lot quicker if I had my list of previous problems to look at.

import itertools
from math import floor,ceil

# The following is not actually used in the program, but it's a useful function.
# Returns all unique permutations. Returns ints if input is int. Returns strings otherwise.
def uniquePermutations(string):
    permutations=list(itertools.permutations(str(string)))
    unique=[]
    for i in permutations:
        i=''.join(i)
        if type(string) is int:
            i=int(i)
        if i not in unique:
            unique.append(i)
    unique.sort()
    return unique

# Attempt 1. Took too long.

def checkCubeRootInteger(i):
    if i==floor(i**(1/3))**3 or i==ceil(i**(1/3))**3:
        return True
    else:
        return False

'''def numberOfCubes(string):
    count=0
    permutations=list(itertools.permutations(str(string)))
    unique=[]
    for i in permutations:
        if i[0]!='0':
            i=''.join(i)
            i=int(i)
            if checkCubeRootInteger(i):
                if i not in unique:
                    unique.append(i)
    return len(unique)

found=False
n=4
while not found:
    n+=1
    num=numberOfCubes(n**3)
    print('The cube of',n,'has',num,'permutational cube(s).')
    if num==5:
        print(n**3,'is the smallest cube with exactly five permutational cubes.')
        found=True'''

# Attempt 2. Pre-generate a list of cubes and compare.

'''from collections import Counter

cubes=[]
for i in range(20000):
    cubes.append(''.join(sorted(str(i**3))))

cubes=Counter(sorted(cubes))
for (cube,repeats) in cubes.items():
    if repeats==5:
        print(cube)'''

# This gives me three (sorted by digit) numbers: 012334566789, 012334556789, 0234556677899.
# The third has more digits than the other two, so we just need to check the first two
# and see what the lowest cube is which permutes from one of these. I could have just kept
# the information in dictionary form during the first loop, but eh.

for i in range(20000):
    sortedNum=''.join(sorted(str(i**3)))
    if sortedNum=='012334566789' or sortedNum=='012334556789':
        print(i**3)
        break
