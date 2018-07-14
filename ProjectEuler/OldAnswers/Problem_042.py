def numericate(word):
    value=0
    for i in word:
        value+=ord(i.upper())-64
    return value

words=0
data=open('Problem_042_data.txt')
data=data.read().strip('"').split('","')
for i in range(len(data)):
    num=numericate(data[i])*2
    if num==int(num**.5)*(int(num**.5)+1):
        words+=1

print words
