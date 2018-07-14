from numpy import loadtxt

data=loadtxt('Problem_013_data.txt')
summation=str(int(sum(data)))
print summation[0:10]
