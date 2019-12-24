from numpy import*
def loadDataSet(filename):
    dataMat=[]
    fr=open(filename)
    for line in fr.readlines():
        fltline=[]
        curline=line.strip().split("\t")
        for num in curline:
            fltline.append(float(num))
        dataMat.append(fltline)
    return dataMat
def distEclud(vecA,vecB):
    return sqrt(sum(power(vecA-vecB,2)))
def randCent(dataSet,k):
    n=shape(dataSet)[1]
    centriods=mat(zeros((k,n)))
    for i in range(n):
        minI=min(dataSet[:,i])
        maxI=max(dataSet[:,i])
        rangeI=float(maxI-minI)
        centriods[:,i]=minI+rangeI*random.rand(k,1)
    return centriods
def kMeans(dataSet,k,distMeas=distEclud,createCent=randCent):
    m=shape(dataSet)[0]
    clusterAssment=mat(zeros((m,2)))
    centroid=createCent(dataSet,k)
    clusterChange=True
    while(clusterChange):
        clusterChange=False
        for i in range(m):
            minDist = float("+inf")
            minIndex = -1
            for j in range(k):
                distJI = distMeas(centroid[j, :], dataSet[i, :])
                if distJI < minDist:
                    minDist = distJI
                    minIndex = j
            if minIndex!=clusterAssment[i,0]:
                clusterChange=True
            clusterAssment[i,:]=minIndex,minDist**2
        print(centroid)
        for cent in range(k):
            ptsInCluster=dataSet[(clusterAssment[:,0]==cent).nonzero()[0]]
            centroid[cent,:]=mean(ptsInCluster,axis=0)
    return centroid,clusterAssment
'''if __name__=="__main__":
    mydat=mat(loadDataSet("testSet.txt"))
    kMeans(mydat,4)'''
def biKmeans(dataSet,k,distMeas=distEclud):
    m=shape(dataSet)[0]
    clusterAssment=mat(zeros((m,2)))
    centroid0=mean(dataSet,axis=0).A[0]
    centList=[centroid0]
    while(len(centList)<k):
        lowestSSE=float("+inf")
        for i in range(len(centList)):
            ptsInCurrCluster=dataSet[(clusterAssment[:,0].A==i).nonzero()[0],:]
            centroidMat,splitClustAss=kMeans(ptsInCurrCluster,2,distMeas)
            splitSSE=sum(splitClustAss[:,1])
            nonsplitSSE=sum(clusterAssment[(clusterAssment[:,0].A!=i).nonzero()[0],1])
            print("the splitSSE and nonsplitSSE is ",splitSSE,nonsplitSSE)
            if splitSSE+nonsplitSSE<lowestSSE:
                lowestSSE=splitSSE+nonsplitSSE
                bestCentToSplit=i
                bestClustAss=splitClustAss.copy()
                bestNewCents=centroidMat
        bestClustAss[(bestClustAss[:,0].A==1).nonzero()[0],0]=len(centList)
        bestClustAss[(bestClustAss[:,0].A==0).nonzero()[0],0]=bestCentToSplit
        print("the best cent to split is ",bestCentToSplit)
        print("the len of the bestClustAss is ",len(bestClustAss))
        clusterAssment[(clusterAssment[:,0].A==bestCentToSplit).nonzero()[0],:]=bestClustAss
        centList[bestCentToSplit]=bestNewCents[0,:].A[0]
        centList.append(bestNewCents[1,:].A[0])
    return mat(centList),clusterAssment