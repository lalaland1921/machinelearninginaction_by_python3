from numpy import *
def loadDataSet(filename):
    fr=open(filename)
    featnum=len(fr.readline().strip().split('\t'))-1
    dataMat=[];labelMat=[]
    for line in fr.readlines():
        linearr=[]
        curline=line.strip().split('\t')
        for i in range(featnum):
            linearr.append(float(curline[i]))
        dataMat.append(linearr)
        labelMat.append(float(curline[-1]))
    return dataMat,labelMat
def stansRegres(xArr,yArr):
    xMat=mat(xArr);yMat=mat(yArr).T
    xTx=xMat.T*xMat
    if linalg.det(xTx)==0.0:
        print("this matrix is singular,cannot do inverse")
        return
    ws=xTx.I*(xMat.T*yMat)
    return ws
def lwlr(testPoint,xArr,yArr,k=1.0):
    xMat=mat(xArr);yMat=mat(yArr)
    m=shape(xMat)[0]
    weights=mat(eye((m)))
    for i in range(m):
        print(testPoint)
        diffMat=testPoint-xMat[i,:]
        print(diffMat)
        weights[i,i]=exp(diffMat*diffMat.T/(-2.0*k**2))
    xTx=xMat.T*weights*xMat
    if linalg.det(xTx)==0.0:
        print("this matrix is singular,can not do inverse")
        return
    ws=xTx.I*xMat.T*weights*yMat
    return testPoint*ws
def lwlrTest(testArr,xArr,yArr,k=1.0):
    testArr=mat(testArr)
    m=shape(testArr)[0]
    yHat=zeros(m)
    for i in range(m):
        yHat[i]=lwlr(testArr[i],xArr,yArr)
    return yHat
'''if __name__=='__main__':
    xArr,yArr=loadDataSet('ex0.txt')
    prey=lwlr(xArr[0],xArr,yArr)
    print(prey)'''
def rssError(yArr,yHatArr):
    return ((yArr-yHatArr)**2).sum()
def ridgeRegres(xMat,yMat,lam=0.2):
    xTx=xMat.T*xMat
    denom=xTx+lam*eye(shape(xMat)[1])
    if linalg.det(denom)==0.0:
        print("this matrix is singular,can not do inverse")
        return
    ws=denom.I*xMat.T*yMat
    return ws
def ridgeTest(xArr,yArr):
    xMat=mat(xArr);yMat=mat(yArr).T
    yMean=mean(yMat)
    xMean=mean(xMat,0)
    yMat=yMat-yMean
    xVar=var(xMat,0)
    xMat=(xMat-xMean)/xVar
    numtestPts=30
    wMat=zeros((numtestPts,shape(xMat)[1]))
    for i in range(numtestPts):
        ws=ridgeRegres(xMat,yMat,exp(i-10))
        wMat[i,:]=ws.T
    return wMat

def stageWise(xArr,yArr,eps=0.01,numIt=100):
    xMat=mat(xArr);yMat=mat(yArr).T
    yMean=mean(yArr,0)
    xMean=mean(xMat,0)
    xVar=var(xMat,0)
    xMat=(xMat-xMean)/xVar
    m,n=shape(xMat)
    returnMat=zeros((numIt,n))
    ws=zeros((n,1));wsTest=ws.copy();wsMax=ws.copy()
    for i in range(numIt):
        print(ws)
        lowerror=inf
        for j in range(m):
            for sign in [-1,1]:
                wsTest=ws.copy()
                wsTest+=eps*sign
                yHat=xMat*wsTest
                rsse=rssError(yMat.A,yHat.A)
                if rsse<lowerror:
                    wsMax=wsTest
                    lowerror=rsse
        ws=wsMax.copy()
        returnMat[i,:]=ws.T
    return returnMat
'''if __name__=='__main__':
    xArr, yArr = loadDataSet('abalone.txt')
    returnmat = stageWise(xArr, yArr, 0.01, 10)
    print(returnmat)'''
from time import sleep
import json
import urllib2
def searchForSet(ret)
