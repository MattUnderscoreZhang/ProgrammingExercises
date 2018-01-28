import itertools as it
import numpy as np

# For this challenge your task is, given a number N, rearrange the numbers 1 to N so that all adjacent pairs of numbers sum up to square numbers.
# There might not actually be a solution. There also might be multiple solution. You are only required to find one, if possible.

# generator for all squares less than or equal to max_n
def possible_squares(max_n):
    n = 1
    while n*n <= max_n:
        yield n*n
        n += 1

# main square chain code
def square_chain(max_n):

    possible_neighbors = [[] for i in range(max_n)]
    for square in possible_squares(2*max_n - 1):
        for i in range(1, max_n+1):
            if square > i and square != 2*i and (square-i <= max_n): possible_neighbors[i-1].append(square - (i+1))

    path = [[0, 0]] # starting on the first index, going towards the first neighbor
    backtrack = False
    while True:
        if backtrack:
            if len(path) > 1:
                path.pop()
                path[-1][1] += 1 # backtrack and try the next neighbor
            elif path[0][0] < max_n-1:
                path[0][0] += 1 # if we've backtracked all the way, try a different starting location
                path[0][1] = 0
            else:
                print "Not possible"
                break # tried everything
            backtrack = False
        index = path[-1][0]
        neighbor = path[-1][1]
        if neighbor >= len(possible_neighbors[index]):
            backtrack = True # keep backtracking
            continue
        if possible_neighbors[index][neighbor] not in [i[0] for i in path]:
            path.append([possible_neighbors[index][neighbor], 0]) # go to the neighbor if it hasn't been visited yet
            if len(path) == max_n:
                print [i[0]+1 for i in path]
                break
        elif neighbor < len(possible_neighbors[index]) - 1:
            path[-1][1] += 1 # else, if there's more neighbors, try the next neighbor
        else:
            backtrack = True # if there's no more neighbors, backtrack

# main
if __name__ == "__main__":
    square_chain(64)
