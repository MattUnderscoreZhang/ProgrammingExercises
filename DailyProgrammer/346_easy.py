import collections
import itertools

##############################################################
# You will be given a cryptarithm in string form. Your task is to output the letters and corresponding numbers which make up a valid solution to the puzzle.
# For the purposes of this challenge, all equations will consist only of addition.
# Leading zeroes (in a multi-digit number) are not allowed in a valid solution.
# The input is guaranteed to be a valid cryptarithm.
##############################################################

# get the sum for digits in a specific place-value column
def get_place_values_sum(number_mapping, input_indices, place):
    sum_ = 0
    for word in input_indices:
        if len(word) >= place:
            sum_ += number_mapping[word[-place]]
    return sum_

# test out a specific number mapping
def test_number_mapping(number_mapping, input_indices, output_indices, first_letter_indices):
    if 0 in number_mapping:
        if number_mapping.index(0) in first_letter_indices: # test if 0 is a leading digit (except for on a 1-digit number)
            return False
    # check the sum
    overflow = 0
    max_places = len(output_indices)
    for place in range(1, max_places+1):
        sum_ = get_place_values_sum(number_mapping, input_indices, place)
        if (sum_+overflow) % 10 != number_mapping[output_indices[-place]]:
            return False
        else:
            overflow = (sum_+overflow)//10
    if overflow != 0:
        return False
    return True

# test all number mappings
def test_all_number_mappings(unique_letters, input_indices, output_indices, first_letter_indices):
    for number_mapping in itertools.permutations(range(10), len(unique_letters)):
        solved = test_number_mapping(number_mapping, input_indices, output_indices, first_letter_indices)
        if solved:
            print "Found solution"
            print zip(unique_letters, number_mapping)
            return
    print "Did not find solution"

# parse cryptarithm
def solve_cryptarithm(cryptarithm):

    left, output = cryptarithm.split(" == ")
    inputs = left.split(" + ")
    unique_letters = ''.join(set(''.join(inputs) + output))
    first_letters = [word[0] for word in (inputs + [output]) if len(word)>1] # ignoring words of length 1

    input_indices = [[unique_letters.index(letter) for letter in word] for word in inputs]
    output_indices = [unique_letters.index(letter) for letter in output]
    first_letter_indices = [unique_letters.index(letter) for letter in first_letters]

    test_all_number_mappings(unique_letters, input_indices, output_indices, first_letter_indices)

# main
if __name__ == "__main__":
    cryptarithms = [
        "WHAT + WAS + THY == CAUSE",
        "HIS + HORSE + IS == SLAIN",
        "HERE + SHE == COMES",
        "FOR + LACK + OF == TREAD",
        "I + WILL + PAY + THE == THEFT",
        "TEN + HERONS + REST + NEAR + NORTH + SEA + SHORE + AS + TAN + TERNS + SOAR + TO + ENTER + THERE + AS + HERONS + NEST + ON + STONES + AT + SHORE + THREE + STARS + ARE + SEEN + TERN + SNORES + ARE + NEAR == SEVVOTH",
        "SO + MANY + MORE + MEN + SEEM + TO + SAY + THAT + THEY + MAY + SOON + TRY + TO + STAY + AT + HOME + SO + AS + TO + SEE + OR + HEAR + THE + SAME + ONE + MAN + TRY + TO + MEET + THE + TEAM + ON + THE + MOON + AS + HE + HAS + AT + THE + OTHER + TEN == TESTS",
        "THIS + A + FIRE + THEREFORE + FOR + ALL + HISTORIES + I + TELL + A + TALE + THAT + FALSIFIES + ITS + TITLE + TIS + A + LIE + THE + TALE + OF + THE + LAST + FIRE + HORSES + LATE + AFTER + THE + FIRST + FATHERS + FORESEE + THE + HORRORS + THE + LAST + FREE + TROLL + TERRIFIES + THE + HORSES + OF + FIRE + THE + TROLL + RESTS + AT + THE + HOLE + OF + LOSSES + IT + IS + THERE + THAT + SHE + STORES + ROLES + OF + LEATHERS + AFTER + SHE + SATISFIES + HER + HATE + OFF + THOSE + FEARS + A + TASTE + RISES + AS + SHE + HEARS + THE + LEAST + FAR + HORSE + THOSE + FAST + HORSES + THAT + FIRST + HEAR + THE + TROLL + FLEE + OFF + TO + THE + FOREST + THE + HORSES + THAT + ALERTS + RAISE + THE + STARES + OF + THE + OTHERS + AS + THE + TROLL + ASSAILS + AT + THE + TOTAL + SHIFT + HER + TEETH + TEAR + HOOF + OFF + TORSO + AS + THE + LAST + HORSE + FORFEITS + ITS + LIFE + THE + FIRST + FATHERS + HEAR + OF + THE + HORRORS + THEIR + FEARS + THAT + THE + FIRES + FOR + THEIR + FEASTS + ARREST + AS + THE + FIRST + FATHERS + RESETTLE + THE + LAST + OF + THE + FIRE + HORSES + THE + LAST + TROLL + HARASSES + THE + FOREST + HEART + FREE + AT + LAST + OF + THE + LAST + TROLL + ALL + OFFER + THEIR + FIRE + HEAT + TO + THE + ASSISTERS + FAR + OFF + THE + TROLL + FASTS + ITS + LIFE + SHORTER + AS + STARS + RISE + THE + HORSES + REST + SAFE + AFTER + ALL + SHARE + HOT + FISH + AS + THEIR + AFFILIATES + TAILOR + A + ROOFS + FOR + THEIR + SAFE == FORTRESSES"
    ]
    for cryptarithm in cryptarithms:
        solve_cryptarithm(cryptarithm)
