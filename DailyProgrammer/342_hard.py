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
        self.bin_state = bin(state)[2:].zfill(pow(2, self.dimensions)) # a box with n dimensions has 2^n locations a snake can go, so a complete state is 2^n bits long
        self.dimensions = dimensions

    # check state
    def check(self):
        n_snake_pieces = gmpy.popcount(self.state) # number of 1's in state
        n_neighbors = 0
        states_w_neighbors = [0] * self.dimensions
        for d in range(self.dimensions):
            n = pow(2, d+1) # number of bits to shift before checking
            states_w_neighbors[d] = self.state & ((self.state >> n) | (self.state << n)) # these states have neighbors in the given direction
        states_w_neighbors = [list(swn.zfill(pow(2, self.dimensions))) for swn in states_w_neighbors]
        n_neighbors = np.sum(states_w_neighbors, axis=0)
        n_endpoints = len(n_neighbors[n_neighbors == 1])
        n_middles = len(n_neighbors[n_neighbors == 2])
        n_crowded = len(n_neighbors[n_neighbors > 2])
        return n_endpoints, n_middles, n_crowded

    # all locations neighboring a given location
    def neighbors(self, location):
        neighbors = []
        for i in range(self.dimensions):
            neighbors.append(location ^ pow(2, i))
        return neighbors

# prints the longest path for the snake-in-the-box problem
def snake_in_the_box(dimensions):

    possible_states = np.ones(pow(2, dimensions))
    current_state = 0
    possible_states[0] = 0
    history = [0]

# entry point
if __name__ == "__main__":

    dimensions = 7

    # snake_in_the_box(dimensions)
    for neighbor in neighbors(8, dimensions):
        print padded_bin(neighbor, dimensions)
