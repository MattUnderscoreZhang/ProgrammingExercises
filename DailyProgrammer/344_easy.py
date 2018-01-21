# In mathematics, the Baum-Sweet sequence is an infinite automatic sequence of 0s and 1s defined by the rule:
# b_n = 1 if the binary representation of n contains no block of consecutive 0s of odd length;
# b_n = 0 otherwise;
# for n >= 0.
# Your challenge today is to write a program that generates the Baum-Sweet sequence from 0 to some number n.

def baum_sweet(n):
    zeros = bin(n)[2:].split('1')
    even = [len(i)%2 == 0 for i in zeros]
    return str(int(all(even)))

def baum_sweet_sequence(n):
    for i in range(n+1):
        print baum_sweet(i) + ",",

if __name__ == "__main__":
    baum_sweet_sequence(50)
