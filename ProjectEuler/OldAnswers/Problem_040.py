def cutoff(digits):
    return sum([9*(10**(i-1))*i for i in range(1,digits+1)])

def digit(place):
    digits=1
    if place==1:
        return 1
    while True:
        if place>cutoff(digits):
            digits+=1
        else:
            number=sum([9*(10**(i-1)) for i in range(1,digits)])+int((place-cutoff(digits-1))/digits)+1
            return int(str(number)[(place-cutoff(digits-1))%digits-1])

print reduce(lambda x,y:x*y,[digit(10**i) for i in range(1,7)])
