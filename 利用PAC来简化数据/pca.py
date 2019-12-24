import numpy as np
def loadDataSet(filename,delim='\t'):
    fr=open(filename)
    retMat=[]
    for curline in fr.readlines():
        dataline=[]
        for data in curline.strip().split(delim):
            dataline.append(float(data))
        retMat.append(dataline)
    return np.mat(retMat)
def pca(dataMat,topNfeat=99999):
    meanVals=np.mean(dataMat,axis=0)
    meanRemoved=dataMat-meanVals
    covMat=np.cov(meanRemoved,rowvar=0)
    eigVals,eigVector=np.linalg.eig(np.mat(covMat))
    eigValInd=np.argsort(-eigVals)
    redEigVects=eigVector[:,eigValInd[0:topNfeat]]
    lowDDataMat=meanRemoved*redEigVects
    reconMat=lowDDataMat*redEigVects.T+meanVals
    return lowDDataMat,reconMat

def replaceNanwithMean(datMat):
    featNum=np.shape(datMat)[1]
    for i in range(featNum):
        meanVal=np.mean(datMat[np.nonzero(~np.isnan(datMat[:,i]))[0]])
        datMat[np.nonzero(np.isnan(datMat[:, i]))[0],i]=meanVal
    return datMat

if __name__=="__main__":
    dataMat = loadDataSet('testSet.txt')
    replaceNanwithMean(dataMat)
    lowDDataMat, reconMat = pca(dataMat,1)