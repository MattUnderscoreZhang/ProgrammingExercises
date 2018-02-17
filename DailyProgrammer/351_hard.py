import numpy as np
import string
import itertools as it

# Star Battle is a grid-based logic puzzle. You are given a SxS square grid divided into S connected regions, and a number N. You must find the unique way to place N*S stars into the grid such that:
# Every row has exactly N stars.
# Every column has exactly N stars.
# Every region has exactly N stars.
# No two stars are horizontally, vertically, or diagonally adjacent.

# import data
file_name = "351_hard.txt"
with open(file_name) as f:
    input_data = f.readlines()
input_data = [line.strip('\n') for line in input_data]

# prepare data
N = int(input_data[0])
input_data.pop(0)
S = int(input_data[0])
input_data.pop(0)

# find regions
region_labels = string.ascii_uppercase[:S]
regions = []
for label in region_labels:
    region = []
    for i, row in enumerate(input_data):
        region.append([(i, j) for j, char in enumerate(row) if char == label])
    region = [item for sublist in region for item in sublist]
    regions.append(region)

# function to check if a solution is correct
def check_solution(solution):
    cols = [star[0] for star in solution]
    rows = [star[1] for star in solution]
    for i in range(S):
        if cols.count(i) != N or rows.count(i) != N: return False
    for i in range(len(solution)):
        for j in range(len(solution)):
            star1 = solution[i]
            star2 = solution[j]
            if abs(star1[0] - star2[0]) == 1 or abs(star1[1] - star2[1]) == 1:
                if abs(star1[0] - star2[0]) == 1 and abs(star1[1] - star2[1]) == 1: return False
    return True

# function to draw what solution looks like
def print_solution(solution):
    for i in range(S):
        for j in range(S):
            if solution.count((i,j)) == 0:
                print("-", end="")
            else:
                print("*", end="")
        print()

# iterate over all possible solutions, starting with S stars in each region
region_stars = [list(it.chain.from_iterable(it.combinations(region, N))) for region in regions]
for solution in it.product(*region_stars):
    if(check_solution(solution)):
        print_solution(solution)
        break
