from numpy import*
def loadDataSet(filename):
    fr=open(filename)
    dataMat=[]
    for line in fr.readlines():
        curline=line.strip().split('\t')
        fltline=[]
        for tmp in curline:
            fltline.append(float(tmp))
        dataMat.append(fltline)
    return dataMat
def binSplitDataSet(dataSet,feature,value):
    mat0=dataSet[nonzero(dataSet[:,feature]>value)[0],:]
    mat1 = dataSet[nonzero(dataSet[:, feature] <= value)[0], :]
    return mat0,mat1
def regLeaf(dataSet):
    return mean(dataSet[:,-1])
def regErr(dataSet):
    return var(dataSet[:,-1])*shape(dataSet)[0]
def createTree(dataSet,leafType=regLeaf,errType=regErr,ops=(1,4)):
    feat,val=chooseBestSplit(dataSet,leafType,errType,ops)
    if feat==None:
        return val
    retTree={}
    retTree['spInd']=feat
    retTree['spVal']=val
    lSet,rSet=binSplitDataSet(dataSet,feat,val)
    retTree['left']=createTree(lSet,leafType,errType,ops)
    retTree['right']=createTree(rSet,leafType,errType,ops)
    return retTree
def chooseBestSplit(dataSet,leafType=regLeaf,errType=regErr,ops=(1,4)):
    tolS=ops[0];tolN=ops[1]
    if len(set(dataSet[:,-1].T.tolist()[0]))==1:
        return None,leafType(dataSet)
    m,n=shape(dataSet)
    S=errType(dataSet)
    bestS=inf;bestIndex=0;bestValue=0
    for featIndex in range(n-1):
        for splitVal in set(dataSet[:,featIndex].T.A.tolist()[0]):#这里进行了改动，否则map is not hashable
            mat0,mat1=binSplitDataSet(dataSet,featIndex,splitVal)
            if shape(mat0)[0]<tolN or shape(mat1)[0]<tolN:
                continue
            newS=errType(mat0)+errType(mat1)
            if newS<bestS:
                bestS=newS;bestIndex=featIndex;bestValue=splitVal
    if S-bestS<tolS:
            return None,leafType(dataSet)
    mat0,mat1=binSplitDataSet(dataSet,bestIndex,bestValue)
    if shape(mat0)[0]<tolN or shape(mat1)[0]<tolN:
        return None,leafType(dataSet)
    return bestIndex,bestValue
'''if __name__=='__main__':
    myDat=loadDataSet("ex00.txt")
    myMat=mat(myDat)
    rettree=createTree(myMat)
    print((rettree))'''
def isTree(obj):
    return (type(obj).__name__=="dict")
def getMean(tree):
    if isTree(tree['left']):tree['left']=getMean(tree['left'])
    if isTree(tree['right']):tree['right']=getMean(tree['right'])
    return (tree['left']+tree['right'])/2.0
def prune(tree,testData):
    if shape(testData[:,-1])==0:return getMean(tree)
    lSet,rSet=binSplitDataSet(testData,tree["spInd"],tree['spVal'])
    if isTree(tree['left']):
        tree['left']=prune(tree['left'],lSet)
    if isTree(tree['right']):
        tree['right']=prune(tree['right'],rSet)
    if not isTree(tree['left']) and not isTree(tree['right']):
        errornomerge=sum(power(lSet[:,-1]-tree['left'],2))+sum(power(rSet[:,-1]-tree['right'],2))
        treeMean = (tree['left']+tree['right'])/2.0
        errormerge=sum(power(lSet[:,-1]-treeMean,2))+sum(power(rSet[:,-1]-treeMean,2))
        if errormerge<errornomerge:
            print("merge")
            return treeMean
    return tree
'''if __name__=="__main__":
    myDat2=loadDataSet("ex2.txt")
    myMat2=mat(myDat2)
    mytree=createTree(myMat2,ops=(0,1))
    myDat2test=loadDataSet("ex2test.txt")
    myMat2test=mat(myDat2test)
    newtree=prune(mytree,myMat2test)
    print(newtree)'''
def linearSolve(dataset):
    m,n=shape(dataset)
    X=mat(ones((m,n)))
    X[:,1:n]=dataset[:,0:n-1]
    Y=dataset[:,n-1]
    xTx=X.T*X
    if linalg.det(xTx)==0:
        raise NameError('this matrix is singular, can not do inverse,\n try increasing the second value of ops')
    ws=xTx.I*X.T*Y
    return ws,X,Y
def modelLeaf(dataset):
    ws,X,Y=linearSolve(dataset)
    return ws
def modelError(dataset):
    ws,X,Y=linearSolve(dataset)
    yHat=X*ws
    return sum(power(Y-yHat,2))
def regTreeEval(model,inData):
    return float(model)
def modelTreeEval(model,inData):
    n=shape(inData)[1]
    X=mat(ones((1,n)))
    X[:,1:n]=inData[:,0:n-1]
    return float(X*model)
def treeForeCast(tree,inData,modelEval=regTreeEval):
    if not isTree(tree):
        return modelEval(tree,inData)
    if inData[0,tree["spInd"]]>tree["spVal"]:
        return treeForeCast(tree["left"],inData,modelEval)
    else:
        return treeForeCast(tree["right"],inData,modelEval)
def createForeCast(tree,testData,modelEval=regTreeEval):
    n=len(testData)
    yHat=mat(zeros((n,1)))
    for i in range(n):
        yHat[i,0]=treeForeCast(tree,mat(testData[i,:]),modelEval)
    return yHat
