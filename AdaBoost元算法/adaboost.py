from numpy import*
def loadSimpleData():
    datMat=mat([[1.,2.1],[2.,1.1],[1.3,1.],[1.,1.],[2.,1.]])
    classLabels=[1.0,1.0,-1.0,-1.0,1.0]
    return datMat,classLabels
def stumpClassify(dataMatrix,dimen,threshVal,threshInq):
    retArray=ones((shape(dataMatrix)[0],1))
    if threshInq=='lt':
        retArray[dataMatrix[:,dimen]<=threshVal]=-1.0
    else:
        retArray[dataMatrix[:,dimen]>threshVal]=-1.0
    return retArray
def biuldStump(dataArr,classLabels,D):
    dataMtrix=mat(dataArr);labelMat=mat(classLabels).T
    m,n=shape(dataMtrix)
    numsteps=10.0;bestStump={};bestClasEst=mat(zeros((m,1)))
    minError=inf
    for i in range(n):
        rangeMin=dataMtrix[:,i].min();rangeMax=dataMtrix[:,i].max()
        stepsize=(rangeMax-rangeMin)/numsteps
        for j in range(-1,int(numsteps)+1):
            for inequal in ['lt','gt']:
                threshVal=rangeMin+stepsize*int(j)
                predictVals=stumpClassify(dataMtrix,i,threshVal,inequal)
                errArr=mat(ones((m,1)))
                errArr[predictVals==labelMat]=0
                weightedError=D.T*errArr
                #print("split:dim %d,thresh %.2f,thresh ineqal: %s,the weighted error is %.3f"%(i,threshVal,inequal,weightedError))
                if weightedError<minError:
                    minError=weightedError
                    bestClassEst=predictVals.copy()
                    bestStump['dim']=i
                    bestStump['thresh']=threshVal
                    bestStump['ineq']=inequal
    return bestStump,minError,bestClassEst
def adaBoostTrainDS(dataArr,classLabels,numIt=40):
    weakclassArr=[];m=shape(dataArr)[0];D=mat(ones((m,1))/m);aggClassEst=mat(zeros((m,1)))
    for i in range(numIt):
        bestStump,error,classEst=biuldStump(dataArr,classLabels,D)
        #print("D:",D)
        print(bestStump)
        alpha=float(0.5*log((1-error)/error))
        bestStump["alpha"]=alpha
        weakclassArr.append(bestStump)
        expon=multiply(-1,multiply(mat(classLabels).T,classEst))
        D=multiply(D,exp(expon))
        D=D/D.sum()
        aggClassEst=aggClassEst+alpha*classEst
        #print("aggClassEst:",aggClassEst)
        aggError=multiply(sign(aggClassEst)!=mat(classLabels).T,ones((m,1)))
        errorRate=aggError.sum()/m
        print("total error",errorRate)
        if errorRate==0.0:
            break
    return weakclassArr
def classifydata(datToclass,classifierArr):
    datamatrix=mat(datToclass)
    m=shape(datamatrix)[0]
    weakclassArr=adaBoostTrainDS(datamatrix,classifierArr)
    classest=mat(zeros((m,1)))
    for beststump in weakclassArr:
        classiarr=stumpClassify(datamatrix,beststump['dim'],beststump['thresh'],beststump['ineq'])
        classest+=beststump['alpha']*classiarr
        print(classest)
    return sign(classest)
def loadDataset(file):
    dataArr=[];classLabel=[]
    fr=open(file)
    numfeat=len(fr.readline().strip().split('\t'))
    for line in fr.readlines():
        linearr=[]
        curline=line.strip().split('\t')
        for i in range(numfeat-1):
            linearr.append(float(curline[i]))
        dataArr.append(linearr)
        classLabel.append(float(curline[numfeat-1]))
    return dataArr,classLabel