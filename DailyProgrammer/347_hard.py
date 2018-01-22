import pandas as pd
import numpy as np
import subprocess
import itertools

# The puzzle opens with a group of tiles of six random colors. The tile in the upper left remains wild for you to change. Tile colors change by flooding from the start tile to directly connected tiles in the four cardinal directions (not diagonals). Directly connected tiles convert to the new color, allowing you to extend the size of the block. The puzzle challenges you to sequentially change the color of the root tile until you grow the block of tiles to the target color in 25 moves or fewer.
# Today's challenge is to read a board tiled with six random colors (R O Y G B V), starting from the wild (W) tile in the upper left corner and to produce a sequence of color changes.

class game(object):

    height = 1
    width = 1
    colors = ['R', 'O', 'Y', 'G', 'B', 'V'] # could also parse from input map
    game_map = [['W']]
    initial_map = [['W']]
    target_color = 'R'

    def __init__(self, input_map_file):
        first_line = subprocess.check_output(['head', '-n 1', input_map_file])[:-1]
        self.game_map = pd.read_csv(input_map_file, header=None, delimiter=' ', engine='python', skiprows=1, skipfooter=1).values
        self.initial_map = np.array(self.game_map)
        last_line = subprocess.check_output(['tail', '-1', input_map_file])[:-1]
        game_size = first_line.split(' ')
        self.width = int(game_size[0])
        self.height = int(game_size[1])
        self.target_color = last_line[0]

    # not a great implementation - the recursion is pretty bad
    def flood(self, color, i=0, j=0, match_color=None):
        if (i>=0 and j>=0 and i<self.height and j<self.width and color!=match_color):
            if match_color == None:
                match_color = self.game_map[i][j]
            if self.game_map[i][j] == match_color:
                self.game_map[i][j] = color
                self.flood(color, i-1, j, match_color)
                self.flood(color, i+1, j, match_color)
                self.flood(color, i, j-1, match_color)
                self.flood(color, i, j+1, match_color)
                return True
            else:
                return False
        else:
            return False

    def display(self):
        print self.game_map
        print ""

    def display_history(self, history):
        print "Displaying move history -", history, "\n"
        self.display()
        for color in history:
            self.flood(color)
            self.display()

    # not a good solution right now - we brute-force all movement chains, without pruning the search tree
    def brute_force(self):
        saved_map = np.array(self.game_map)
        max_moves = 25
        fewest_moves = 25
        for moveset_backwards in itertools.product(self.colors, repeat=max_moves):
            moveset = moveset_backwards[::-1]
            print "Examining moveset", moveset
            if any(moveset[i]==moveset[i+1] for i in range(len(moveset)-1)): # check for repeated values
                continue
            for n, move in enumerate(moveset):
                if n+1 >= fewest_moves:
                    self.game_map = np.array(saved_map)
                    break
                if not self.flood(move):
                    self.game_map = np.array(saved_map)
                    break
            if all([all([i == self.target_color for i in row]) for row in self.game_map]):
                best_moveset = moveset
                fewest_moves = len(moveset)
        self.game_map = np.array(self.initial_map)
        return best_moveset

    def greedy(self):
        saved_map = np.array(self.game_map)
        max_moves = 500
        move_number = 1
        last_move = 'W'
        most_flooded = 0
        best_move = 'W'
        history = []
        while move_number <= max_moves:
            for color in self.colors:
                if color == last_move:
                    continue
                else:
                    self.flood(color)
                    if all([all([i == self.target_color for i in row]) for row in self.game_map]):
                        best_move = color
                        move_number = max_moves
                        break
                    self.flood('W')
                    n_flooded = np.count_nonzero(saved_map != self.game_map)
                    if n_flooded > most_flooded:
                        most_flooded = n_flooded
                        best_move = color
                self.game_map = np.array(saved_map)
            history.append(best_move)
            self.flood(best_move)
            saved_map = np.array(self.game_map)
            move_number += 1
        self.game_map = np.array(self.initial_map)
        return history

    def find_best_moves(self):
        best_moveset = self.greedy()
        return best_moveset

if __name__ == "__main__":

    input_map_file = "347_hard_map2.csv"
    game = game(input_map_file)
    history = game.find_best_moves()
    print history
    # game.display_history(history)
