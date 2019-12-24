def loadDataSet(filename):
    datamat=[];labelmat=[]
    fr=open(filename)
    for line in fr.readlines():
        lineArr=line.strip().split('\t')
        datamat.append([float(lineArr[0]),float(lineArr[1])])
        labelmat.append(float(lineArr[2]))
    return datamat,labelmat
def selectJrand(i,m):
    j=i
    while(j==i):
        j=int(random.uniform(0,m))
    return j
def clipalpha(aj,H,L):#clip修剪
    if aj>H:
        aj=H
    if aj<L:
        aj=L
    return aj
def smoSimple(dataMatIn,classLabel,C,toler,maxIter):
    dataMatrix=mat(dataMatIn);labelMat=mat(classLabels).transpose()
    b=0;m,n=shape(dataMatrix)
    alphas=mat(zeros((m,1)))
    iter=0
    while(iter<maxIter):
        alphaPairsChanged=0
        for i in range(m):
            fXi=float(multiply(alphas,labelMat).T*(dataMatrix*dataMatrix[i,:].T))+b