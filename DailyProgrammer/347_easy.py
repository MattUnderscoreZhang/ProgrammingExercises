import pandas as pd
import numpy as np

# There is a light in a room which lights up only when someone is in the room (think motion detector). You are given a set of intervals in entrance and exit times as single integers, and expected to find how long the light has been on. When the times overlap, you need to find the time between the smallest and the biggest numbers in that interval.
# First column of csv is entrance times, and second column is exits.

data = pd.read_csv("347_easy.csv", header=None, delimiter=" ")
data = data.sort_values(by=[0])
data = np.array(data)

time_on = 0
first_entrance = 0
last_exit = 0

for i, row in enumerate(data):
    this_entrance = row[0]
    this_exit = row[1]
    if this_entrance > last_exit:
        time_on += (last_exit - first_entrance)
        first_entrance = this_entrance
        last_exit = this_exit
    else:
        if this_exit > last_exit:
            last_exit = this_exit
        if i == len(data)-1: # last row
            time_on += (last_exit - first_entrance)

print time_on
