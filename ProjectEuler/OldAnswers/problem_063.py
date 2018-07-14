# Matt Zhang
# 2014-01-06
# Python 3.3.3

# Everything below 10, when raised to the nth power, will not be able to keep up with n.
# Anything above 10 would have more than n digits. Therefore, we're only looking for
# numbers between 1-9, raised to some powers.

count=0
for n in range(1,10):
    for power in range(1,100):
        raised=n**power
        if raised>10**(power-1)-1 and raised<10**power:
            count+=1
            print(raised)
        elif raised>10**power:
            break
print('There are',count,'such numbers.')
