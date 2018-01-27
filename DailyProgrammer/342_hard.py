from __future__ import division
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
        n_neighbors = np.zeros(pow(2, self.dimensions))
        for n, bit in enumerate(self.bin_state):
            if bit == '1': 
                for d in range(self.dimensions):
                    n_neighbors[n] += (self.bin_state[self.partner_index(n, d)] == '1')
        n_endpoints = len(n_neighbors[n_neighbors == 1])
        n_middles = len(n_neighbors[n_neighbors == 2])
        n_crowded = len(n_neighbors[n_neighbors > 2])
        n_isolated = n_snake_pieces - n_endpoints - n_middles - n_crowded
        return n_snake_pieces, n_endpoints, n_middles, n_crowded, n_isolated

    # return a score for this state
    def score(self):
        n_snake_pieces, n_endpoints, n_middles, n_crowded, n_isolated = self.check()
        return 3*n_middles - abs(2 - n_endpoints) - 5*(n_crowded) - n_isolated

    # all locations neighboring a given location
    def neighbors(self, location):
        neighbors = []
        for i in range(self.dimensions):
            neighbors.append(location ^ pow(2, i))
        return neighbors

# prints the longest path for the snake-in-the-box problem
def snake_in_the_box(dimensions):

    population_size = 500
    n_survivors = 20
    mutation_rate = 0.015
    n_generations = 1000

    snake_population = []
    np.random.seed()
    for _ in range(population_size): # initialize population
        snake_state = np.random.randint(pow(2, dimensions))
        snake_population.append(state(snake_state, dimensions))

    for gen_n in range(n_generations):

        # calculate fitnesses of snakes
        scores = []
        for snake in snake_population:
            scores.append(snake.score())
        snake_fitness = zip(scores, range(population_size))
        snake_fitness.sort(key = lambda s : s[0], reverse = True)

        # choose who survives (natural selection)

        # # truncation selection
        # survivor_scores = [s[0] for s in snake_fitness[:n_survivors]]
        # best_snakes = [s[1] for s in snake_fitness[:n_survivors]]
        # survivors = [snake_population[snake] for snake in best_snakes]

        # roulette (proportional) selection
        truncated_scores = [max(s[0], 1) for s in snake_fitness] # give each snake a chance
        total_score = sum(truncated_scores)
        probabilities = [s/total_score for s in truncated_scores]
        survivor_indices = []
        survivor_scores = []
        survivors = []
        keep_best_n = 3
        best_snakes = [s[1] for s in snake_fitness[:n_survivors]]
        for i in range(keep_best_n): # always keep best snakes
            survivor_indices.append(best_snakes[i])
            survivor_scores.append(truncated_scores[best_snakes[i]])
            survivors.append(snake_population[best_snakes[i]])
        while len(survivors) < n_survivors:
            survivor_index = np.random.choice(population_size, 1, p=probabilities)[0]
            if survivor_index not in survivor_indices:
                survivor_indices.append(survivor_index)
                survivor_scores.append(truncated_scores[survivor_index])
                survivors.append(snake_population[survivor_index])
        survivor_scores.sort(reverse = True)

        snake_population = survivors
        print "Survivor scores, generation", str(gen_n+1)+":", survivor_scores

        # choose who mates (sexual selection)
        for _ in range(population_size - n_survivors):
            parent_1 = np.random.randint(n_survivors)
            parent_2 = np.random.randint(n_survivors-1)
            if parent_2 == parent_1: parent_2 = n_survivors-1
            mutations = [str(int(i < mutation_rate)) for i in np.random.rand(pow(2, dimensions))]
            mutations = "".join(mutations)
            mutations = int(mutations, 2)
            cut_point_a = np.random.randint(pow(2, dimensions))
            cut_point_b = np.random.randint(pow(2, dimensions))
            cut_point_1 = min(cut_point_a, cut_point_b)
            cut_point_2 = max(cut_point_a, cut_point_b)
            child_dna = int(snake_population[parent_1].bin_state[:cut_point_1] + snake_population[parent_2].bin_state[cut_point_1:cut_point_2] + snake_population[parent_1].bin_state[cut_point_2:], 2)
            new_state = child_dna ^ mutations
            new_snake = state(new_state, dimensions)
            snake_population.append(new_snake)

    print "Best snake:", snake_population[0].state
    print "Snake stats (n_pieces, n_endpoints, n_middles, n_crowded, n_isolated):", snake_population[0].check()

# entry point
if __name__ == "__main__":

    # best_snake_length = 96
    # my_best = 65
    dimensions = 8
    snake_in_the_box(dimensions)
