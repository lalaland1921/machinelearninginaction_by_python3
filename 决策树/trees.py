def splitdataset(dataset,axis,value):
    retdataset=[]
    for featvec in dataset:
        if featvec[axis]==value:
            reducedfeatvec=featvec[:axis]
            reducedfeatvec.extend(featvec[axis+1:])
            retdataset.append(reducedfeatvec)
    return retdataset
from math import log
def calshannonent(dataset):
    numentries=len(dataset)
    labelcounts={}
    for featvec in dataset:
        currentlabel=featvec[-1]
        if currentlabel not in labelcounts.keys():
            labelcounts[currentlabel]=0
        labelcounts[currentlabel]+=1
    shannoent=0.0
    for key in labelcounts:
        pro=float(labelcounts[key])/numentries
        shannoent-=pro*log(pro,2)
    return shannoent
def creatdataset():
    dataset=[[1,1,'yes'],[1,1,'yes'],[1,0,'no'],[0,1,'no'],[0,1,'no']]
    labels=['no surfacing','flippers']
    return dataset,labels
def choosebestfeaturetosplit(dataset):
    num=len(dataset)
    numfeatures=len(dataset[0])-1
    baseentropy=calshannonent(dataset)
    bestinfogain=0.0;bestfeature=-1
    for i in range(numfeatures):
        featurelist=[example[i] for example in dataset]
        uniquevals=set(featurelist)
        newentropy=0.0
        for value in uniquevals:
            subdataset=splitdataset(dataset,i,value)
            prob=len(subdataset)/float(num)
            newentropy+=prob*calshannonent(subdataset)
        infogain=baseentropy-newentropy
        if infogain > bestinfogain:
            bestinfogain=infogain
            bestfeature=i
    return bestfeature
import operator
def majoritycnt(classlist):
    classcount={}
    for vote in classlist:
        if vote not in classcount.keys():classcount[vote]=0
        classcount[vote]+=1
    sortedclasscount=sorted(classcount.items(),operator.itemgetter(1),reverse=True)
    return sortedclasscount[0][0]
def creattree(dataset,labels):
    classlist=[example[-1] for example in dataset]
    if classlist.count(classlist[0])==len(classlist):
        return classlist[0]
    if len(dataset[0])==1:
        return majoritycnt(classlist)
    bestfeature=choosebestfeaturetosplit(dataset)
    bestfealabel=labels[bestfeature]
    mytree={bestfealabel:{}}
    del(labels[bestfeature])
    bestfeaturelist=[example[bestfeature] for example in dataset]
    bestfeatureset=set(bestfeaturelist)
    for value in bestfeatureset:
        subdataset=splitdataset(dataset,bestfeature,value)
        sublabels=labels[:]
        mytree[bestfealabel][value]=creattree(subdataset,sublabels)
    return mytree