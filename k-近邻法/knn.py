from numpy import *
import operator
def creatdataset():
    group=array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels=['A','A','B','B']
    return group,labels
def classify0(inx,dataset,labels,k):
    dimension=dataset.shape[0]
    distance=tile(inx,(dimension,1))-dataset
    distance=distance**2
    distance=distance.sum(axis=1)
    distance=distance**0.5
    sort_indices=distance.argsort()
    class_count={}
    for i in range(k):
        label=labels[sort_indices[i]]
        class_count[label]=class_count.get(label,0)+1
    sortedclass=sorted(class_count.items(),key=operator.itemgetter(1),reverse=True)
    return sortedclass[0][0]

def file2matrix(filename):
    fr=open(filename)
    arrayolines=fr.readlines()
    numolines=len(arrayolines)
    returnmat=zeros((numolines,3))
    classlabelvector=[]
    index=0
    for line in arrayolines:
        line=line.strip()#去除首尾空格
        listfromline=line.split('\t')#以tab分隔的字符串变为列表
        returnmat[index,:]=listfromline[:3]
        classlabelvector.append(int(listfromline[-1]))
        index +=1
    return returnmat,classlabelvector
def autonorm(dataset):
    minvals=dataset.min(0)
    maxvals=dataset.max(0)
    ranges=maxvals-minvals
    m=dataset.shape[0]
    result=dataset-tile(minvals,(m,1))
    result=result/tile(ranges,(m,1))
    return result,ranges,minvals
def datingClassTest(filename):
    horatio=0.1
    datingdatamat,datinglabels=file2matrix(filename)
    normMat,ranges,minvals=autonorm(datingdatamat)
    m=normMat.shape[0]
    numtestvecs=int(horatio*m)
    erronum=0
    for i in range(numtestvecs):
        classifierresult=classify0(normMat[i,:],normMat[numtestvecs:m,:],datinglabels[numtestvecs:m],3)
        print("the classifier came back with: {:d},the real answer is {:d}".format(classifierresult,datinglabels[i]))
        if classifierresult!=datinglabels[i]:
            erronum+=1
    print("the error rate is {:.2f} ".format(float(erronum/numtestvecs)))
def img2vector(filename):
    returnvector=zeros((1,1024))
    fr=open(filename)
    for i in range(32):
        line=fr.readline()
        for j in range(32):
            returnvector[0][i*32+j]=int(line[j])
    return returnvector
from os import listdir
def handwritingclasstest():
    hwlabel=[]
    trainingfilelist=listdir('trainingDigits')
    m=len(trainingfilelist)
    trainingMat=zeros((m,1024))
    for i in range(m):
        filenamestr=trainingfilelist[i]
        filestr=filenamestr.split('.')[0]
        digit=int(filestr.split('_')[0])
        hwlabel.append(digit)
        trainingMat[i,:]=img2vector('trainingDigits\%s'%filenamestr)
    testfilelist=listdir('testDigits')
    m=len(testfilelist)
    errorcount=0.0
    for i in range(m):
        filenamestr=testfilelist[i]
        filestr=filenamestr.split('.')[0]
        digit=int(filestr.split('_')[0])
        testvector=img2vector('testDigits\%s'%filenamestr)
        testresult=classify0(testvector,trainingMat,hwlabel,3)
        print("the classifier came back with %d,the real answer is %d" %(testresult,digit))
        if testresult!=digit:
            errorcount+=1
    print("the error rate is %.2f"%(float(1.0*errorcount/m)))     