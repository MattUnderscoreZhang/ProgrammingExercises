import Utilities as U

sum_threes = U.discrete_series_sum(3, 999, 3) 
sum_fives = U.discrete_series_sum(5, 995, 5) 
sum_fifteens = U.discrete_series_sum(15, 990, 15) 

sum_multiples = sum_threes + sum_fives - sum_fifteens

print sum_multiples
