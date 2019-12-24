class treeNode:
    def __init__(self,nameValue,numOccur,parentNode):
        self.name=nameValue
        self.count=numOccur
        self.nodeLink=None
        self.parent=parentNode
        self.children={}
    def inc(self,numOccur):
        self.count+=numOccur
    def disp(self,ind=1):
        print(" "*ind,self.name,'',self.count)
        for child in self.children.values():
            child.disp(ind+1)

def createTree(dataSet,minSup=1):
    headerTable={}
    for trans in dataSet:
        for item in trans:
            headerTable[item]=headerTable.get(item,0)+dataSet[trans]
    for k in list(headerTable.keys()):
        if headerTable[k]<minSup:
            del(headerTable[k])
    freqItemSet=set(headerTable.keys())
    if len(freqItemSet)==0:return None,None
    for k in headerTable:
        headerTable[k]=[headerTable[k],None]
    retTree=treeNode('NULL set',1,None)
    for transSet,count in dataSet.items():
        itemList=[item for item in transSet if item in freqItemSet]
        if itemList!=None:
            orderedItems=sorted(itemList,key=lambda p:headerTable[p][0],reverse=True)#改用list.sort()就错了，
            updateTree(orderedItems,retTree,headerTable,count)
    return retTree,headerTable
def updateTree(items,inTree,headerTable,count):#注意逻辑关系和缩进，否则updateHeader会死循环，只对新建的结点进行连接，否则nodelink指向自己
    if items[0] in inTree.children:
        inTree.children[items[0]].inc(count)
    else:
        inTree.children[items[0]]=treeNode(items[0],count,inTree)
        if headerTable[items[0]][1]==None:
            headerTable[items[0]][1]=inTree.children[items[0]]
        else:
            updateHeader(headerTable[items[0]][1],inTree.children[items[0]])
    if len(items)>1:
        updateTree(items[1::],inTree.children[items[0]],headerTable,count)
def updateHeader(nodeToTree,targetNode):
    while(nodeToTree.nodeLink!=None):
        nodeToTree=nodeToTree.nodeLink
    nodeToTree.nodeLink=targetNode
def loadSimpDat():
    simDat=[['r','z','h','j','p'],
            ['z','y','x','w','v','u','t','s'],
            ['z'],
            ['r','x','n','o','s'],
            ['y','r','x','z','q','t','p'],
            ['y','z','x','e','q','s','t','m']]
    return simDat
def createInitSet(dataSet):
    retDict={}
    for trans in dataSet:
        retDict[frozenset(trans)]=1
    return retDict

def acsendTree(leafNode,prefixPath):
    while(leafNode.parent!=None):
        prefixPath.append(leafNode.name)
        leafNode=leafNode.parent
def findPrefixPath(basePat,headerTable):
    conPats={}
    treeNode=headerTable[basePat][1]
    while(treeNode!=None):
        prefixPath=[]
        acsendTree(treeNode,prefixPath)
        if len(prefixPath)>0:
            conPats[frozenset(prefixPath[1:])]=treeNode.count
        treeNode=treeNode.nodeLink
    return conPats
def mineTree(inTree,headerTable,minSup,prefix,freqItemList):
    bigL=[v[0] for v in sorted(headerTable.items(),key=lambda p:p[1][0])]
    for basePat in bigL:
        newFreqSet=prefix.copy()
        newFreqSet.add(basePat)
        freqItemList.append(newFreqSet)
        condPattBases=findPrefixPath(basePat,headerTable)
        myCondTree,myHeaderTable=createTree(condPattBases,minSup)
        if myHeaderTable!=None:
            print("conditional tree for: ", newFreqSet)
            myCondTree.disp(1)
            mineTree(myCondTree,myHeaderTable,minSup,newFreqSet,freqItemList)

if __name__=="__main__":
    simDat=loadSimpDat()
    initSet=createInitSet(simDat)
    myTree,headerTable=createTree(initSet,3)
    myTree.disp(1)
    mineTree(myTree,headerTable,3,set([]),[])



