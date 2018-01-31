#include <iostream>
#include <vector>
#include <cmath>
#include <random>

using namespace std;

// Fermat's little theorem states:
// If p is a prime number, then for any integer a, the number a**p − a is an integer multiple of p.
// This can also be stated as (a**p) % p = a
// If n is not prime, then, in general, most of the numbers a < n will not satisfy the above relation. This leads to the following algorithm for testing primality: Given a number n, pick a random number a < n and compute the remainder of a**n modulo n. If the result is not equal to a, then n is certainly not prime. If it is a, then chances are good that n is prime. Now pick another random number a and test it with the same method. If it also satisfies the equation, then we can be even more confident that n is prime. By trying more and more values of a, we can increase our confidence in the result. This algorithm is known as the Fermat test.

int myPow(int x, int p)
{
  if (p == 0) return 1;
  if (p == 1) return x;

  int tmp = myPow(x, p/2);
  if (p%2 == 0) return tmp * tmp;
  else return x * tmp * tmp;
}

int power_modulus(int a, long p) {
    // returns (a ** p) % p
    // let b = a % p -> then (a ** p) % p = (b ** p) % p
    long base_component = a;
    long power_component = p;
    long multiplicative_component = 1;
    while (power_component > 1) {
        //cout << base_component << ", " << power_component << ", " << multiplicative_component << endl;
        long power_series = 1;
        for (int n = 1; n <= power_component; n++) {
            power_series *= base_component;
            if (power_series >= p) {
                multiplicative_component *= myPow(base_component, power_component % n);
                base_component = power_series % p;
                if (base_component == 0) return 0;
                power_component = floor(power_component / n);
                multiplicative_component %= p;
                break;
            }
            if (n == power_component) {
                base_component = power_series;
                power_component = 1;
            }
        }
    }
    return (myPow(base_component, power_component) * multiplicative_component) % p;
}

int main(int argn, char* args[]) {
    long p = stol(args[1]);
    int n_to_try = 7;
    random_device rd; // only used once to initialise (seed) engine
    mt19937 rng(rd()); // random-number engine used (Mersenne-Twister in this case)
    uniform_int_distribution<int> uni(2, 100); // guaranteed unbiased

    for (int i = 0; i < n_to_try; i++) {
        int a = uni(rng);
        //int a = 26;
        if (power_modulus(a, p) != a) {
            cout << "Not a prime" << endl;
            return 0;
        }
    }
    cout << "Tested " << n_to_try << " values - probability of prime better than 1 in " << pow(2, n_to_try) << endl;
    return 0;
}
