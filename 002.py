import Utilities as U

# let F_i be the ith Fibonnaci number, where F_1=1 and F_2=2
# F_i = F_(i-1) + F_(i-2)
# F_n = F_(n-1) + F_(n-2) = 2*F_(n-2) + F_(n-3) = 3*F_(n-3) + 2*F_(n-4) = 5*F_(n-4) + 3*F(n-5) = F_i*F_(n-i) + F_(i-1)*F(n-i-1)

# F_2, F_5, and F_(2+3n) are even
# F_n = 3*F_(n-3) + 2*F_(n-4) = 3*F_(n-3) + (F_(n-5) + F_(n-6)) + (F_(n-3) - F_(n-5)) = 4*F_(n-3) + F_(n-6) 
# let K_i be the ith even Fibonnaci number - then K_i = 4*K_(i-1) + K_(i-2)

max_value = 4000000

fibo_a = 2
fibo_b = 8
current_sum = 10

while (fibo_b <= max_value):
    fibo_c = fibo_a + 4*fibo_b
    fibo_a = fibo_b
    fibo_b = fibo_c
    if (fibo_b <= max_value):
        current_sum += fibo_b

print current_sum
