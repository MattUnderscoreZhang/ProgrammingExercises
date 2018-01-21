import sys

# You'll be given a LFSR input on one line specifying the tap positions (0-indexed), the feedback function (XOR or XNOR), the initial value with leading 0s as needed to show you the bit width, and the number of clock steps to output.
# The feedback function is used on the bits in the tap positions, indicating the next input bit.

class LFSR(object):

    registers = []
    tap_positions = []
    feedback_function = "XOR"

    def __init__(self, initial_registers, tap_positions, feedback_function):
        self.registers = initial_registers
        self.tap_positions = tap_positions
        self.feedback_function = feedback_function

    def step(self):
        new_bit = 0
        if feedback_function == "AND":
            new_bit = all([self.registers[i] for i in tap_positions])
        elif feedback_function == "OR":
            new_bit = any([self.registers[i] for i in tap_positions])
        elif feedback_function == "XOR":
            new_bit = reduce(lambda i, j: i != j, [self.registers[i] for i in tap_positions])
        elif feedback_function == "XNOR":
            new_bit = reduce(lambda i, j: i == j, [self.registers[i] for i in tap_positions])
        else:
            print "Unrecognized feedback function"
            sys.exit(0)
        self.registers.insert(0, int(new_bit))
        self.registers.pop()

    def display(self):
        print self.registers

if __name__ == "__main__":

    # initial_registers = [0, 0, 1]
    # tap_positions = [0, 2]
    # feedback_function = "XNOR"
    # steps = 7

    initial_registers = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
    tap_positions = [1, 5, 6, 31]
    feedback_function = "XOR"
    steps = 16

    my_LFSR = LFSR(initial_registers, tap_positions, feedback_function)
    my_LFSR.display()

    for step in range(steps):
        my_LFSR.step()
        my_LFSR.display()
