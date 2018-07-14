# No need to check lower right corners.

from myFunctions import isprime

primes=3
layers=2
while 1.0*primes/(4*layers-3)>.1:
    if isprime((2*layers-1)**2+(2*layers)):
        primes+=1
    if isprime((2*layers-1)**2+2*(2*layers)):
        primes+=1
    if isprime((2*layers-1)**2+3*(2*layers)):
        primes+=1
    layers+=1

print 2*layers-1
