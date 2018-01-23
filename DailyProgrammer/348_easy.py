import numpy as np

# Rabbits are known for their fast breeding, but how soon will they dominate the earth?
# Every month a fertile female will have 14 offspring (5 males and 9 females).
# A female rabbit is fertile when it has reached the age of 4 months, they never stop being fertile.
# Rabbits die at the age of 8 years (96 months).

initial_male_rabbits, initial_female_rabbits, target_rabbits = (2, 4, 15000000000)
female_rabbits = np.zeros(96) # sorted by age in months
male_rabbits = np.zeros(96)
female_rabbits[2] = initial_female_rabbits
male_rabbits[2] = initial_male_rabbits
total_rabbits = initial_female_rabbits + initial_male_rabbits
months = 0

def propagate():
    global months, female_rabbits, male_rabbits, total_rabbits
    months += 1
    fertile_rabbits = np.sum(female_rabbits[4:])
    new_male_rabbits = 5*fertile_rabbits
    new_female_rabbits = 9*fertile_rabbits
    female_rabbits = np.roll(female_rabbits, 1)
    female_rabbits[0] = new_female_rabbits
    male_rabbits = np.roll(male_rabbits, 1)
    male_rabbits[0] = new_male_rabbits
    total_rabbits += (new_male_rabbits + new_female_rabbits)

if __name__ == "__main__":
    while (total_rabbits < target_rabbits):
        propagate()
    print months
