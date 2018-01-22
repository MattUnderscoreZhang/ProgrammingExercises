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
    control_map = [[1]]
    initial_map = [['W']]
    initial_control_map = [[1]]
    target_color = 'R'

    def __init__(self, input_map_file):
        first_line = subprocess.check_output(['head', '-n 1', input_map_file])[:-1]
        self.game_map = pd.read_csv(input_map_file, header=None, delimiter=' ', engine='python', skiprows=1, skipfooter=1).values
        self.initial_map = np.array(self.game_map)
        last_line = subprocess.check_output(['tail', '-1', input_map_file])[:-1]
        game_size = first_line.split(' ')
        self.width = int(game_size[0])
        self.height = int(game_size[1])
        self.control_map = np.zeros((self.height, self.width))
        self.control_map[0][0] = 1
        self.initial_control_map = np.array(self.control_map)
        self.target_color = last_line[0]

    # returns number of newly flooded squares
    # I did this in a dumb way - I could have just had a single map, instead of game_map and control_map. Color control region a unique color, and recolor it according to step when displaying history.
    def flood(self, color):
        new_squares = 0
        for i in range(self.height):
            for j in range(self.width):
                control_self = self.control_map[i][j]
                control_above = i>0 and self.control_map[abs(i-1)][j]
                control_left = j>0 and self.control_map[i][abs(j-1)]
                control_below = i<self.height-1 and self.control_map[abs(i+1)][j]
                control_right = j<self.width-1 and self.control_map[i][abs(j+1)]
                if self.game_map[i][j]==color and (control_above or control_left or control_below or control_right) and not control_self:
                    self.control_map[i][j] = 1
                    new_squares += 1
        self.game_map[self.control_map == 1] = color
        return new_squares

    def display(self):
        print self.game_map
        print self.control_map
        print ""

    def display_history(self, history):
        print "Displaying move history -", history, "\n"
        self.display()
        for color in history:
            self.flood(color)
            self.display()

    def greedy(self):
        saved_map = np.array(self.game_map)
        saved_control_map = np.array(self.control_map)
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
                    n_flooded = self.flood(color)
                    if np.count_nonzero(self.control_map) == self.height*self.width and color == self.target_color: # check win
                        best_move = color
                        move_number = max_moves
                        break
                    if n_flooded > most_flooded:
                        most_flooded = n_flooded
                        best_move = color
                self.game_map = np.array(saved_map) # reset to try another color
                self.control_map = np.array(saved_control_map)
            history.append(best_move)
            self.flood(best_move)
            saved_map = np.array(self.game_map)
            saved_control_map = np.array(self.control_map)
            most_flooded = 0
            move_number += 1
        self.game_map = np.array(self.initial_map)
        self.control_map = np.array(self.initial_control_map)
        return history

    def find_best_moves(self):
        best_moveset = self.greedy()
        return best_moveset

if __name__ == "__main__":

    input_map_file = "347_hard_map3.csv"
    game = game(input_map_file)
    # game.display_history(['Y', 'O', 'R', 'R'])
    history = game.find_best_moves()
    print history
    # game.display_history(history)
