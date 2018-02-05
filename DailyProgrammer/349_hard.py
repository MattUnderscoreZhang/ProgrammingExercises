# INCOMPLETE
# Can't figure out a good formula to do this problem, especially since I don't think TF takes variable-sized inputs (for unknown number of sub-polygons each with an unknown number of vertices).

import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf

# You are given a number of points, forming the hull of a convex polygon. You are also given a number N.
# Your goal is to partition the original polygon into N smaller polygons, all containing equal amount of space (surface, volume, ...), by adding at most one node, and as many edges as required.
# If it is impossible to find a valid solution by adding the single node, you may give a result for the max number < N, for which a equitable partitioning is possible.

# If I were more concerned about performance, I'd write this using TensorFlow

#############
# FUNCTIONS #
#############

class node(object):
    x = 0
    y = 0
    moveable = False
    def __init__(self, x, y, moveable=False):
        self.x = x
        self.y = y
        self.moveable = moveable
    def position(self):
        return [self.x, self.y]

class line(object):
    node_0 = 0
    node_1 = 1
    def __init__(self, node_0, node_1):
        self.node_0 = node_0
        self.node_1 = node_1
    def nodes(self):
        return [self.node_0, self.node_1]

# class internode(object):
    # my_nodes = [0, 1]
    # internode_fraction = 0.5
    # x = 0
    # y = 0
    # def set(self, my_nodes, internode_fraction):
        # self.my_nodes = my_nodes
        # self.internode_fraction = internode_fraction
        # nodes_diff = [a-b for a,b in zip(nodes[my_nodes[1]], nodes[my_nodes[0]])]
        # [self.x, self.y] = [a + b * internode_fraction for a,b in zip(nodes[my_nodes[0]], nodes_diff)]
    # def get_node(self):
        # return [self.x, self.y]
    # def __init__(self, nodes, internode_fraction):
        # self.set(nodes, internode_fraction)

def draw_polygon(nodes, lines):
    node_positions = [node.position() for node in nodes]
    line_nodes = [line.nodes() for line in lines]
    for x in node_positions:
        plt.plot(x[0], x[1], "o")
    for node in line_nodes:
        [x1, y1] = node_positions[node[0]]
        [x2, y2] = node_positions[node[1]]
        plt.plot([x1, x2], [y1, y2], 'k-')
    x_min = min([x[0] for x in node_positions])
    x_max = max([x[0] for x in node_positions])
    y_min = min([x[1] for x in node_positions])
    y_max = max([x[1] for x in node_positions])
    plt.xlim(x_min - (x_max-x_min)*0.25, x_max + (x_max-x_min)*0.25)
    plt.ylim(y_min - (y_max-y_min)*0.25, y_max + (y_max-y_min)*0.25)
    plt.show()

# shoelace formula
def poly_area(nodes):
    x_in = [x[0] for x in [node.position() for node in nodes]]
    y_in = [x[1] for x in [node.position() for node in nodes]]
    x = tf.placeholder(tf.float32)
    y = tf.placeholder(tf.float32)
    x_roll_1 = tf.concat(values=[x[len(nodes)-1:], x[:len(nodes)-1]], concat_dim=0)
    y_roll_1 = tf.concat(values=[y[len(nodes)-1:], y[:len(nodes)-1]], concat_dim=0)
    shoelace_x = tf.reduce_sum(tf.multiply(x, y_roll_1))
    shoelace_y = tf.reduce_sum(tf.multiply(y, x_roll_1))
    area = tf.constant(0.5) * tf.abs(shoelace_x - shoelace_y)
    with tf.Session() as sess:
        return sess.run(area, feed_dict={x: x_in, y: y_in})

#############
# MAIN CODE #
#############

input_filename = "349_hard.txt"
input_file = open(input_filename)

# parse input
N = int(input_file.readline().strip("\n"))
node_data = input_file.readline().strip("\n").replace("(", "").split(")")[:-1]
nodes = [node(float(data[0]), float(data[1])) for data in [data.split(" ") for data in node_data]]
line_data = node_data = input_file.readline().strip("\n").replace("(", "").split(")")[:-1]
lines = [line(int(data[0])-1, int(data[1])-1) for data in [data.split(" ") for data in line_data]]

print("Split into", N, "polygons")
print("Nodes at:", [node.position() for node in nodes])
print("Lines between nodes:", [line.nodes() for line in lines])
print("Area:", poly_area(nodes))
# print("Drawing polygon")
# draw_polygon(nodes, lines)
print()
input_file.close()

# n_new_internodes = N - len(nodes)
# if (n_new_internodes != 0):
    # print("Sorry, code can't deal with this yet")

x_nodes = [x[0] for x in [node.position() for node in nodes]]
y_nodes = [x[1] for x in [node.position() for node in nodes]]
new_node = node(np.mean(x_nodes), np.mean(y_nodes))
for node in range(len(nodes)):
    lines.append(line(node, len(nodes)))
nodes.append(new_node)
# print("Drawing polygon")
# draw_polygon(nodes, lines)
# print()

# # new_internode = internode([0, 2], 0.3)
# # nodes.append(new_internode.get_node())
# # print(new_internode.get_node())

# print("Drawing polygon")
# draw_polygon()
