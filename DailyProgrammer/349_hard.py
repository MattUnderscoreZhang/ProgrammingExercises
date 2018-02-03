import matplotlib.pyplot as plt
import numpy as np

# You are given a number of points, forming the hull of a convex polygon. You are also given a number N.
# Your goal is to partition the original polygon into N smaller polygons, all containing equal amount of space (surface, volume, ...), by adding at most one node, and as many edges as required.
# If it is impossible to find a valid solution by adding the single node, you may give a result for the max number < N, for which a equitable partitioning is possible.

# If I were more concerned about performance, I'd write this using TensorFlow

###############
# PARSE INPUT #
###############

input_filename = "349_hard.txt"
input_file = open(input_filename)

# parse input
N = int(input_file.readline().strip("\n"))
nodes = [[float(node[0]), float(node[1])] for node in [node.split(" ") for node in input_file.readline().strip("\n").replace("(", "").split(")")[:-1]]]
lines = [[int(line[0])-1, int(line[1])-1] for line in [line.split(" ") for line in input_file.readline().strip("\n").replace("(", "").split(")")[:-1]]]

def draw_polygon():
    for node in nodes:
        plt.plot(node[0], node[1], "o")
    for line in lines:
        [x1, y1] = nodes[line[0]]
        [x2, y2] = nodes[line[1]]
        plt.plot([x1, x2], [y1, y2], 'k-')
    x_min = min([x[0] for x in nodes])
    x_max = max([x[0] for x in nodes])
    y_min = min([x[1] for x in nodes])
    y_max = max([x[1] for x in nodes])
    plt.xlim(x_min - (x_max-x_min)*0.25, x_max + (x_max-x_min)*0.25)
    plt.ylim(y_min - (y_max-y_min)*0.25, y_max + (y_max-y_min)*0.25)
    plt.show()

class internode(object):
    my_nodes = [0, 1]
    internode_fraction = 0.5
    node = nodes[0]
    def set(self, my_nodes, internode_fraction):
        self.my_nodes = my_nodes
        self.internode_fraction = internode_fraction
        nodes_diff = [a-b for a,b in zip(nodes[my_nodes[1]], nodes[my_nodes[0]])]
        self.node = [a + b * internode_fraction for a,b in zip(nodes[my_nodes[0]], nodes_diff)]
    def get_node(self):
        return self.node
    def __init__(self, nodes, internode_fraction):
        self.set(nodes, internode_fraction)

# shoelace formula, stolen from Stack Overflow
def poly_area(x,y):
    return 0.5 * np.abs(np.dot(x, np.roll(y,1)) - np.dot(y, np.roll(x,1)))

#############
# MAIN CODE #
#############

print("Split into", N, "polygons")
print("Nodes at:", nodes)
print("Lines between nodes:", lines)
print("Area:", poly_area([x[0] for x in nodes], [x[1] for x in nodes]))
# print("Drawing polygon")
# draw_polygon()
print()
input_file.close()

new_internode = internode([0, 2], 0.3)
nodes.append(new_internode.get_node())
print(new_internode.get_node())
print("Drawing polygon")
draw_polygon()
