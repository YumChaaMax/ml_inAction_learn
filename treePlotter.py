# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 21:14:42 2018

@author: Max Yang
"""

import matplotlib.pyplot as plt

decisionNode=dict(boxstyle="sawtooth",fc="0.8")
leafNode=dict(boxstyle="round4",fc="0.8")
arrow_args=dict(arrowstyle="<-")

def plotNode(nodeTxt, centerPt,parentPt,nodeType):
    createPlot.ax1.annotate(nodeTxt,xy=parentPt,xycoords='axes fraction',\
                            xytext=centerPt,textcoords='axes fraction',\
                            va="center",ha="center",bbox=nodeType, arrowprops=arrow_args)
    
def createPlot():
    #to greate a new figure, 1 represents id, facecolor 是表示背景图
    fig=plt.figure(1,facecolor='white')
    #clear it
    fig.clf()
    createPlot.ax1=plt.subplot(111,frameon=False)
    plotNode('a decision Node',(0.5,0.1),(0.1,0.5),decisionNode)
    plotNode("a leaf node",(0.8,0.1),(0.3,0.8),leafNode)
    plt.show()
    
def getNumLeafs(myTree):
    numLeafs=0
    firstStr=list(myTree.keys())[0]
    secondDict=myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=='dict':
            numLeafs+=getNumLeafs(secondDict[key])
        else:
            numLeafs+=1
    return(numLeafs)
    
def getTreeDepth(myTree):
    maxDepth=0
    #获取第一个key
    firstStr=list(myTree.keys())[0]
    secondDict=myTree[firstStr]
    for key in secondDict.keys():
        #判定对象类型的一种用法，见下方if条件
        if type(secondDict[key]).__name__=='dict':
            thisDepth=1+getTreeDepth(secondDict[key])
        else:
            thisDepth=1
        if thisDepth>maxDepth:
            maxDepth=thisDepth
    return(maxDepth)
    
def retrieveTree(i):
    listOfTrees=[{'no surfacing':{0:'no',1:{'flippers':\
                                            {0:'no',1:'yes'}}}},\
    {'no surfacing':{0:'no',1:{'flippers':\
                               {0:{'head':{0:'no',1:'yes'}},1:'no'}}}}]
    return(listOfTrees[i])

def plotMidText(cntrPt, parentPt, txtString):
    xMid=(parentPt[0]-cntrPt[0])/2.0+cntrPt[0]
    yMid=(parentPt[1]-cntrPt[1])/2.0+cntrPt[1]
    createPlot.ax1.text(xMid,yMid,txtString)

def plotTree(myTree,parentPt,nodeText):
    numLeafs=getNumLeafs(myTree)
    depth=getTreeDepth(myTree)
    firstStr=list(myTree.keys())[0]
    cntrPt=(plotTree.xOff+(1.0+float(numLeafs))/2.0/plotTree.totalW,plotTree.yOff)
    plotMidText(cntrPt,parentPt,nodeTxt)
    plotNode(firstStr,cntrPt,parentPt,decisionNode)
    secondDict=myTree[firstStr]
    plotTree.yOff=plotTree.yOff-1.0/plotTree.totalD
    for key in secondDict.keys():
        if type(secondDict[key]).__name__='dict':
            plotTree(secondDict[key],cntrPt,str(key))
        else:
            plotTree.xoff=plotTree.xOff+1.0/plotTree.totalW
    


    