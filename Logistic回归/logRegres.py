def loadDataSet():
    dataMat=[];labelMat=[]
    fr=open('D:\\python程序\\Python进行机器学习\\Logistic回归\\testSet.txt')
    for line in fr.readlines():
        lineArr=line.strip().split()
        dataMat.append([1.0,float(lineArr[0]),float(lineArr[1])])
        labelMat.append(int(lineArr[2]))
    return dataMat,labelMat
def sigmoid(inX):
    return 1.0/(1+exp(-inX))
def gradAscent(dataMatIn,classLabels):
    dataMatrix=mat(dataMatIn)
    labelMat=mat(classLabels).transpose()
    m,n=shape(dataMatrix)
    alpha=0.001
    maxCycles=500
    weights=ones((n,1))
    for k in range(maxCycles):
        h=sigmoid(dataMatrix*weights)
        error=labelMat-h
        weights=weights+alpha*dataMatrix.transpose()*error
    return weights
'''if __name__ == "__main__":
    lis=[]
    fr=open('D:\\python程序\\Python进行机器学习\\Logistic回归\\testSet.txt')#注意这里\是转义符，因此需要双\\，否则出错
    for line in fr.readlines():#记住是readlines不是readline要加s
        lineArr=line.strip().split('\t')
        lis.append(lineArr)
    print(lis)'''
'''if __name__=="__main__":
    data,label=loadDataSet()
    print(gradAscent(data,label))'''
def plotBestFit(weights):
    import matplotlib.pyplot as plt
    dataMat,labelMat=loadDataSet()
    dataArr=array(dataMat)
    n=shape(dataArr)[0]
    xcord1=[];ycord1=[]
    xcord2=[];ycord2=[]
    for i in range(n):
        if int(labelMat[i])==1:
            xcord1.append(dataArr[i][1]);ycord1.append(dataArr[i][2])
        else:
            xcord2.append(dataArr[i][1]);ycord2.append(dataArr[i][2])
    fig=plt.figure()
    ax=fig.add_subplot()
    ax.scatter(xcord1,ycord1,s=30,c="red",marker='s')
    ax.scatter(xcord2,ycord2,s=30,c='green')
    x=arange(-3.0,3.0,0.1)
    y=(-weights[0]-weights[1]*x)/weights[2]
    ax.plot(x,y)
    plt.xlabel('X1');plt.ylabel('X2')
    plt.show()
'''if __name__=="__main__":
    data,label=loadDataSet()
    weights=gradAscent(data,label)
    plotBestFit(weights.getA())#注意getA的用法，与mat相反'''
def stocGradAscent0(dataMatrix,classLabels):
    m,n=shape(dataMatrix)
    alpha=0.01
    weights=mat(ones(n))
    for i in range(m):
        h=sigmoid(sum(dataMatrix[i]*weights))
        error=classLabels[i]-h
        weights=weights+alpha*error*dataMatrix[i]
    return weights
if __name__ == "__main__":
    data,label=loadDataSet()
    weights=stocGradAscent0(data,label)
    plotBestFit(weights.getA())
def stocGradAscent1(dataMatrix,classLabels,numIter=150):
    m,n=shape(dataMatrix)
    weights=ones(n)
    for i in range(numIter):
        dataIndex=range(m)
        alpha=4/(1.0+i+j)+0.01
        randIndex=int(random.uniform(0,len(dataIndex)))
        h=sigmoid(sum(dataMatrix[dataIndex[randIndex]]*weights))
        error=classLabels[dataIndex[randIndex]]-h
        weights=weights+alpha*error*dataMatrix[dataIndex[randIndex]]
        del(dataIndex[randIndex])
    return weights
def classifyVector(inX,weights):
    prob=sigmoid(sum(inX*weights))
    if prob>0.5 :
        return 1
    else:
        return 0
def colicTest():
    frTrain=open('horseColicTraining.txt')
    frTest=open('horseColicTest.txt')
    trainingSet=[];trainingLabels=[]
    for line in frTrain.readlines():
        currLine=line.strip().split('\t')
        lineArr=[]
        for i in range(21):
            lineArr.append(float(currLine[i]))
        trainingSet.append(lineArr)
        trainingLabels.append(float(currLine[21]))
    trainingWeights=stocGradAscent(array(trainingSet,trainingLabels,500))
    errorcount=0.0
    numTestVec=0.0
    for line in frTest.readlines():
        numTestVec+=1.0
        currLine=line.strip().split('\t')
        for i in range(21):
            lineArr.append(float(currLine[i]))
        if int(classifyVector(array(lineArr),trainingWeights))!=int(currLine[21]):
            errorcount+=1
    errorRate=float(errorcount)/numTestVec
    print("the error rate of the test is: %f"%errorRate)
    return errorRate
def multiTest():
    numTests=10;errorSum=0.0
    for k in range(numTests):
        errorSum+=colicTest()
    print("after %d iterations the average error rate is: %f"%(numTests,errorSum/float(numTests)))