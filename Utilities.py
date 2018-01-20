#-----------
# CONSTANTS
#-----------

PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]

#------
# SUMS
#------

# sum of numbers in series (i, i+s, i+2s... i+ns), where first=i, step=s, last=i+ns
def discrete_series_sum(first, last, step):
    n_items = (last-first)/step + 1
    return (last+first)*n_items/2
