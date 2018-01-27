import itertools as it
import numpy as np
import gmpy

# The snake-in-the-box problem in graph theory and computer science deals with finding a certain kind of path along the edges of a hypercube. This path starts at one corner and travels along the edges to as many corners as it can reach. After it gets to a new corner, the previous corner and all of its neighbors must be marked as unusable. The path should never travel to a corner after it has been marked unusable.

# A game state, with 1's representing all locations where the snake is, and 0's representing where it isn't
class state(object):

    state = 0
    bin_state = '0'
    dimensions = 1

    # initialize state
    def __init__(self, state, dimensions):
        self.state = state
        self.bin_state = bin(state)[2:].zfill(pow(2, dimensions)) # a box with n dimensions has 2^n locations a snake can go, so a complete state is 2^n bits long
        self.dimensions = dimensions

    # find corresponding index in a dimension - for instance, index 8 (1000) along dimension 1 will correspond to index 9 (1010)
    def partner_index(self, index, dimension):
        if index < pow(2, dimension):
            bit = 0
        else:
            bit = bin(index)[-(dimension+1)]
        if (bit == '1'):
            return index - pow(2, dimension)
        else:
            return index + pow(2, dimension)

    # check state
    def check(self):
        n_snake_pieces = gmpy.popcount(self.state) # number of 1's in state
        n_neighbors = [0] * pow(2, self.dimensions)
        for n, bit in enumerate(self.bin_state):
            if bit == '1': 
                for d in range(self.dimensions):
                    n_neighbors[n] += (self.bin_state[self.partner_index(n, d)] == '1')
        n_neighbors = np.array(n_neighbors)
        n_endpoints = len(n_neighbors[n_neighbors == 1])
        n_middles = len(n_neighbors[n_neighbors == 2])
        n_crowded = len(n_neighbors[n_neighbors > 2])
        n_isolated = n_snake_pieces - n_endpoints - n_middles - n_crowded
        return n_snake_pieces, n_endpoints, n_middles, n_crowded, n_isolated

    # all locations neighboring a given location
    def neighbors(self, location):
        neighbors = []
        for i in range(self.dimensions):
            neighbors.append(location ^ pow(2, i))
        return neighbors

# prints the longest path for the snake-in-the-box problem
def snake_in_the_box(dimensions):

    my_state = state(30, dimensions)
    print my_state.bin_state
    print my_state.check()

# entry point
if __name__ == "__main__":

    dimensions = 7
    snake_in_the_box(dimensions)
