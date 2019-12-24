def loadExData():
    return [[1,1,1,0,0],[2,2,2,0,0],[1,1,1,0,0],[5,5,5,0,0],[1,1,0,2,2],[0,0,0,3,3],[0,0,0,1,1]]
def loadExData2():
    return[[0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 5],
           [0, 0, 0, 3, 0, 4, 0, 0, 0, 0, 3],
           [0, 0, 0, 0, 4, 0, 0, 1, 0, 4, 0],
           [3, 3, 4, 0, 0, 0, 0, 2, 2, 0, 0],
           [5, 4, 5, 0, 0, 0, 0, 5, 5, 0, 0],
           [0, 0, 0, 0, 5, 0, 1, 0, 0, 5, 0],
           [4, 3, 4, 0, 0, 0, 0, 5, 5, 0, 1],
           [0, 0, 0, 4, 0, 4, 0, 0, 0, 0, 4],
           [0, 0, 0, 2, 0, 2, 5, 0, 0, 1, 2],
           [0, 0, 0, 0, 5, 0, 0, 0, 0, 4, 0],
           [1, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0]]
import numpy as np
from numpy import linalg as la

def euclidSim(inA,inB):
    return 1.0/(1.0+la.norm(inA-inB))

def pearsSim(inA,inB):
    if len(inA)<3:return 1.0
    return 0.5+0.5*la.corrcoef(inA,inB)

def cosSim(inA,inB):
    num=float(inA.T*inB)
    denom=la.norm(inA)*la.norm(inB)
    return 0.5+0.5*num/denom

def standEst(dataMat,user,simMeas,item):
    n=np.shape(dataMat)[1]
    simTotal=0.0;rateSimTotal=0.0
    for j in range(n):
        userRating=dataMat[user,j]
        if userRating==0:
            continue
        overlap=np.nonzero(np.logical_and(dataMat[:,j],dataMat[:,item]))[0]
        if overlap==None:similarity=0
        else:
            similarity=simMeas(dataMat[:,j],dataMat[:,item])
        print("the %d and %d similarity is: %f".format(item,j,similarity))
        simTotal+=similarity
        rateSimTotal+=similarity*userRating
    if simTotal==0.0:return 0
    return rateSimTotal/simTotal

def recommend(dataMat,user,N=3,simMeas=cosSim,estMethod=standEst):
    unratedItem=np.nonzero(dataMat[user,:]==0)[1]
    if len(unratedItem)==0:
        return 'you rated everything!'
    itemScores=[]
    for item in unratedItem:
        estimatedScore=estMethod(dataMat,user,simMeas,item)
        itemScores.append((item,estimatedScore))
    return sorted(itemScores,key=lambda x:x[1],reverse=True)[:N]

def svdEst(dataMat,user,simMeas,item):
    n=np.shape(dataMat)[1]
    U,sigma,VT=la.svd(dataMat)
    Sig4=np.mat(np.eye(4)*sigma[:4])
    xformedItems=dataMat.T*U[:,:4]*Sig4.I
    for j in range(n):
        userRating=dataMat[user,j]
        simTotal=0.0;rateSimTotal=0.0
        if userRating==0 or j== item:continue
        similarity=simMeas(xformedItems[j,:].T,xformedItems[item,:].T)
        print("the",j,"and",item,"similarity is ",similarity)
        simTotal+=similarity
        rateSimTotal+=similarity*userRating
    if simTotal==0.0:return 0
    return rateSimTotal/simTotal

def printMat(inMat,threshold=0.8):
    for i in range(32):
        for j in range(32):
            if float(inMat[i,j])>threshold:
                print(1)
            else:print(0)
        print(' ')


def imgCompress(numSV=3,threshold=0.8):
    myl=[]
    fr=open('0_5.txt')
    for line in fr.readlines():
        newrow=[int(num) for num in line.strip()]
        myl.append(newrow)
    myMat=np.mat(myl)
    print("the original image is *********")
    printMat(myMat)
    U,sigma,VT=la.svd(myMat)
    SigRecon=np.mat(np.eye(numSV)*sigma[:numSV])
    reconMat=U[:,:numSV]*SigRecon*VT[:numSV,:]
    print("the reconstruted image is ********")
    #printMat(reconMat)

if __name__=="__main__":
    imgCompress()
