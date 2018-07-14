from numpy import *
data=loadtxt('Problem_011_data.txt')
greatestProduct=0;
for i in range(0,20):
    for j in range(0,20):
        newProductR=0
        newProductD=0
        newProductDD=0
        newProductDU=0
        # Right multiply.
        if j<=16:
            newProductR=data[i][j]*data[i][j+1]*data[i][j+2]*data[i][j+3]
        # Down multiply.
        if i<=16:
            newProductD=data[i][j]*data[i+1][j]*data[i+2][j]*data[i+3][j]
        # Diagonal down multiply.
        if i<=16 and j<=16:
            newProductDD=data[i][j]*data[i+1][j+1]*data[i+2][j+2]*data[i+3][j+3]
        # Diagonal up multiply.
        if i>=3 and j<=16:
            newProductDU=data[i][j]*data[i-1][j+1]*data[i-2][j+2]*data[i-3][j+3]
        if max(newProductR,newProductD,newProductDD,newProductDU)>greatestProduct:
            greatestProduct=max(newProductR,newProductD,newProductDD,newProductDU)
print int(greatestProduct)
