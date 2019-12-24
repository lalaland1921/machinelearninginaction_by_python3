from numpy import *
def loaddataset():
    postinglist=[['my','dog','has','flea','problems','help','please'],['maybe','not','take','him','to','dog','park','sutpid'],['my','dalmation','is','so','cute','i','love','him'],['stop','posting','stupid','worthless','garbage'],['mr','licks','ate','my','steak','how','to','stop','him'],['quit','buying','worthless','dog','food','stupid']]
    classvec=[0,1,0,1,0,1]
    return postinglist,classvec
def creatvocablist(dataset):
    vocabset=set([])
    for document in dataset:
        vocabset=vocabset|set(document)
    return list(vocabset)
def setofwords2vec(vocabset,inputset):
    returnvec=[0]*len(vocabset)
    for word in inputset:
        if word in vocabset:
            returnvec[vocabset.index(word)]=1
        else: 
            print("the word %s is not in my vocabulary"%word)
    return returnvec
def trainNB0(trainmatrix,traincategory):
    numtraindocs=len(trainmatrix)
    numwords=len(trainmatrix[0])
    pAbusive=sum(traincategory)/float(numtraindocs)
    p0num=ones(numwords);p1num=ones(numwords)
    p0denom=2.0;p1denom=2.0
    for i in range(numtraindocs):
        if traincategory[i]==1:
            p1num+=trainmatrix[i]
            p1denom+=sum(trainmatrix[i])
        else:
            p0num+=trainmatrix[i]
            p0denom+=sum(trainmatrix[i])
    p1vec=log(p1num/float(p1denom))
    p0vec=log(p0num/float(p0denom))
    return p0vec,p1vec,pAbusive
def classifyNB(vec2Classify,p0vec,p1vec,pclass1):
    p1=sum(vec2Classify*p1vec)+log(pclass1)
    p0=sum(vec2Classify*p0vec)+log(1-pclass1)
    if p1>p0:
        return 1
    else:
        return 0
def testingNB():
    listposts,listclasses=loaddataset()
    myvocablist=creatvocablist(listposts)
    trainmat=[]
    for words in listposts:
        trainmat.append(setofwords2vec(myvocablist,words))
    p0vec,p1vec,pab=trainNB0(array(trainmat),array(listclasses))
    testentry=['love','my','dalmation']
    vec2Classify=array(setofwords2vec(myvocablist,testentry))
    print(testentry,"is classified as: ",classifyNB(vec2Classify,p0vec,p1vec,pab))
    testentry=['stupid','garbage']
    vec2Classify=array(setofwords2vec(myvocablist,testentry))
    print(testentry,"is classified as: ",classifyNB(vec2Classify,p0vec,p1vec,pab))
def bagofword2vecmn(vocablist,inputset):    
    result=zeros(len(vocablist))
    for word in inputset:
        if word in vocablist:
            vocablist[vocablist.index(word)]+=1
    return result
def textparse(bigstring):
    import re
    listoftokens=re.split(r'\W+',bigstring)#记得W大写，与书上方法不同，书上可能是python2的写法，这是Python3的写法
    return [token.lower() for token in listoftokens if len(token)>2]
def spamtest():
    doclist=[];classlist=[];fulltext=[]
    for i in range(1,26):
        wordlist=textparse(open('D:\python程序\Python进行机器学习\朴素贝叶斯\email\email\spam\%d.txt'%i).read())
        doclist.append(wordlist)
        fulltext.extend(wordlist)
        classlist.append(1)
        wordlist=textparse(open('D:\python程序\Python进行机器学习\朴素贝叶斯\email\email\ham\%d.txt'%i).read())
        doclist.append(wordlist)
        fulltext.extend(wordlist)
        classlist.append(0)
    vocablist=creatvocablist(doclist)
    trainingset=list(range(50));testset=[]
    for i in range(10):
        randindex=int(random.uniform(0,len(trainingset)))
        testset.append(trainingset[randindex])
        del(trainingset[randindex])
    trainmat=[];trainclasses=[]
    for docindex in trainingset:
        trainmat.append(setofwords2vec(vocablist,doclist[docindex]))
        trainclasses.append(classlist[docindex])
    pv0,pv1,pspam=trainNB0(trainmat,trainclasses)
    errorcount=0
    for docindex in testset:
        wordvector =setofwords2vec(vocablist,doclist[docindex])
        if classifyNB(array(wordvector),pv0,pv1,pspam)!=classlist[docindex]:
            errorcount+=1
    print("the error rate is:",float(errorcount)/len(testset))
