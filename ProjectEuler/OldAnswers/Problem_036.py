# Only consider odd numbers.

def isPalindrome(num):
    Num=str(num)
    for i in range(len(Num)):
        if Num[i]!=Num[len(Num)-1-i]:
            return False
    return True

sum=0
# range(start,stop,step)
for num in range(1,10**6,2):
    if isPalindrome(num) and isPalindrome(str(bin(num))[2:]):
        sum+=num

print sum
