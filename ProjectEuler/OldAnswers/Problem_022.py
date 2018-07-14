from numpy import loadtxt, zeros

def score(name):
    score=0
    for letter in name:
        score+=ord(letter)-64
    return score

data=open('Problem_022_data.txt')
names=data.read().strip('"').split('","')
names.sort()
scores=zeros(len(names))
for i in range(len(names)):
    scores[i]=(i+1)*score(names[i])
print int(sum(scores))
