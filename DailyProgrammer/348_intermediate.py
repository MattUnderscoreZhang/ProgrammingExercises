# Today's challenge will be a variation on a popular introductory programming task, scoring a game of bowling. However, in this challenge, we won't even actually have to calculate the score. Today's challenge is to produce the display for the individual frames, given a list of the number of pins knocked down on each frame.

def display_pin_score(pins_hit):
    display_string = ""
    on_second_roll = False
    first_roll_value = 0
    on_round = 1
    for roll in range(len(pins_hit)):
        if on_round < 11:
            if not on_second_roll:
                if pins_hit[roll] < 10: 
                    on_second_roll = True
                    first_roll_value = pins_hit[roll]
                else:
                    display_string += "X\t"
                    on_round += 1
            else:
                on_second_roll = False
                if first_roll_value + pins_hit[roll] < 10: 
                    display_string += ((str(first_roll_value) if first_roll_value > 0 else "-") + (str(pins_hit[roll]) if pins_hit[roll] > 0 else "-") + "\t")
                else:
                    display_string += ((str(first_roll_value) if first_roll_value > 0 else "-") + "/\t")
                on_round += 1
        else:
            display_string = display_string[:-1] # strip final tab
            if on_second_roll:
                display_string += (str(first_roll_value) if first_roll_value > 0 else "-")
                on_second_roll = False
            if pins_hit[roll] < 10:
                display_string += (str(pins_hit[roll]) if pins_hit[roll] > 0 else "-")
            else:
                display_string += "X\t"
    print display_string

pins_hit = [[6, 4, 5, 3, 10, 10, 8, 1, 8, 0, 10, 6, 3, 7, 3, 5, 3],
[9, 0, 9, 0, 9, 0, 9, 0, 9, 0, 9, 0, 9, 0, 9, 0, 9, 0, 9, 0],
[10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
[5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
[10, 3, 7, 6, 1, 10, 10, 10, 2, 8, 9, 0, 7, 3, 10, 10, 10],
[9, 0, 3, 7, 6, 1, 3, 7, 8, 1, 5, 5, 0, 10, 8, 0, 7, 3, 8, 2, 8]]
for hits in pins_hit:
    display_pin_score(hits)
