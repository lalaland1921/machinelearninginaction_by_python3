def loadDataSet():
    return [[1,3,4],[2,3,5],[1,2,3,5],[2,5]]
def createC1(dataSet):
    C1=[]
    for transaction in dataSet:
        for item in transaction:
            if not [item] in C1:
                C1.append([item])
    C1.sort()
    retC1=[]
    for item in C1:
        retC1.append(frozenset(item))
    return retC1
def scanD(D,Ck,minSupport):
    ssCnt={}#字典
    for tid in D:
        for can in Ck:
            if can.issubset(tid):
                if can not in ssCnt:ssCnt[can]=1
                else:ssCnt[can]+=1
    numItem=len(D)
    retList=[]
    supportData={}
    for key in ssCnt.keys():
        support=float(ssCnt[key]/numItem)
        if support>=minSupport:
            retList.insert(0,key)
        supportData[key]=support
    return retList,supportData
def aprioriGen(Lk,k):
    retList=[]
    lenLK=len(Lk)
    for i in range(lenLK):
        for j in range(i+1,lenLK):
            L1=list(Lk[i])[:k-2];L2=list(Lk[j])[:k-2]
            L1.sort();L2.sort()
            if L1==L2:
                retList.append(Lk[i]|Lk[j])
    return retList
def apriori(dataSet,minSupport=0.5):
    C1=createC1(dataSet)
    D=[set(item) for item in dataSet]
    L1,supportData=scanD(D,C1,minSupport)
    L=[L1]
    k=2
    while(len(L[k-2])>0):
        Ck=aprioriGen(L[k-2],k)
        Lk,supK=scanD(D,Ck,minSupport)
        L.append(Lk)
        supportData.update(supK)
        k+=1
    return L,supportData
def generateRule(L,supportData,minConf=0.7):
    bigRuleList=[]
    for i in range(1,len(L)):
        for freqSet in L[i]:
            H1=[frozenset([item]) for item in freqSet]
            if i >1:
                ruleFromConseq(freqSet,H1,supportData,bigRuleList,minConf)
            else:
                calcConf(freqSet,H1,supportData,bigRuleList,minConf)
    return bigRuleList
def calcConf(freqSet,H,supportData,brl,minConf):
    prunedH=[]
    for conseq in H:
        conf=supportData[freqSet]/supportData[freqSet-conseq]
        if conf>minConf:
            prunedH.append(conseq)
            print(freqSet-conseq,"-->",conseq,"conf",conf)
            brl.append((freqSet-conseq,conseq,conf))
    return prunedH
def ruleFromConseq(freqSet,H,supportData,bigRuleList,minConf):
    k=len(H[0])
    while(len(freqSet)>k+1):
        Hmp1=aprioriGen(H,k+1)
        Hmp1=calcConf(freqSet,Hmp1,supportData,bigRuleList,minConf)
        if len(Hmp1)>1:
            ruleFromConseq(freqSet,Hmp1,supportData,bigRuleList,minConf)
if __name__=="__main__":
    dataSet=loadDataSet()
    L,supportData=apriori(dataSet)
    bigrulelist=generateRule(L,supportData)
