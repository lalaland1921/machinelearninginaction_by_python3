import matplotlib.pyplot as plt 
decisionnode=dict(boxstyle="sawtooth",fc="0.8")
leafnode=dict(boxstyle="round4",fc="0.8")
arrow_args=dict(arrowstyle="<-")
def plotnode(nodetxt,centerpt,parentpt,nodetype):
    creatPlot.ax1.annotate(nodetxt,xy=parentpt,xycoords='axes fraction',xytext=centerpt,textcoords='axes fraction',va='center',ha="center",bbox=nodetype,arrowprops=arrow_args)
def creatPlot():
    fig=plt.figure(1,facecolor='white')
    fig.clf()
    creatPlot.ax1=plt.subplot(111,frameon=False)
    plotnode('决策节点',(0.5,0.1),(0.1,0.5),decisionnode)
    plotnode('叶节点',(0.8,0.1),(0.3,0.8),leafnode)
    plt.show()