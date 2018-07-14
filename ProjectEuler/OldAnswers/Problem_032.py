# The smallest possible candidate has 4 digits, while the largest possible
# candidate also has 4 digits. It can be either a product of a 4-digit number
# with a 1-digits number or of a 2-digit number with a 3-digit number.

import time

sum=0
# Remember that the upper bound of range() is non-inclusive (annoying).
for num in range(1234,9877):
    for i in range(1,99):
        # Remember that python floors integer division! At least until 3.0.
        total=str(num)+str(i)+str(num/i)
        if num%i==0 and ''.join(sorted(total))=='123456789':
            sum+=num
            print total
            # After finding the first one, go on to the next number.
            break
print sum

time.sleep(60)
