# -*- coding: utf-8 -*-
"""
Created on Sat Jul 21 19:31:55 2018

@author: Max Yang
"""

from math import log
import operator

def calcShannonEnt(dataSet):
    """计算数据集的信息熵"""
    numEntries=len(dataSet)
    labelCounts={}
    for featVec in dataSet:
        currentLabel=featVec[-1]
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel]=0
        labelCounts[currentLabel]+=1
    shannonEnt=0.0
    for key in labelCounts:
        prob=float(labelCounts[key])/numEntries
        shannonEnt-=prob*log(prob,2)
    return(shannonEnt)

def splitDataSet(dataSet,axis,value):
    """
    按照给定的特征划分数据集
    输入参数为：待划分的数据集、划分数据集的特征（位置）、该特征的值
    返回的是取该值时其他特征和标签
    """
    retDataSet=[]
    for featVec in dataSet:
        if featVec[axis]==value:
            reducedFeatVec=featVec[:axis]
            reducedFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reducedFeatVec)
    return(retDataSet)

def chooseBestFeatureToSplit(dataSet):
    numFeatures=len(dataSet[0])-1
    baseEntropy=calcShannonEnt(dataSet)
    bestInfoGain=0.0
    bestFeature=-1
    for i in range(numFeatures):
        featList=[example[i] for example in dataSet]
        uniqueVals=set(featList)
        newEntropy=0.0
        for value in uniqueVals:
            subDataSet=splitDataSet(dataSet,i,value)
            prob=len(subDataSet)/float(len(dataSet))
            newEntropy+=prob*calcShannonEnt(subDataSet)
        infoGain=baseEntropy-newEntropy
        if (infoGain>bestInfoGain):
            bestInfoGain=infoGain
            bestFeature=i
    return(bestFeature)

def majorityCnt(classList):
    """多数表决,选择一个节点中次数最多的类别"""
    classCount={}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote]=0
        classCount[vote]+=1
    sortedClassCount=sorted(classCount.iteritems(),key=operator.itemgetter(1),reverse=True)
    return(sortedClassCount[0][0])
        
def createTree(dataSet,labels):
    """输入变量为数据集，和标签列表"""
    #生成标签列表
    classList=[example[-1] for example in dataSet]
    #判定是否所有标签属于同一类，是则停止继续划分
    if classList.count(classList[0])==len(classList):
        return(classList[0])
    #所有特征遍历完了，则停止划分，返回的分类为出现次数最多的分类
    if len(dataSet[0])==1:
        return(majorityCnt(classList))
    
    bestFeat=chooseBestFeatureToSplit(dataSet)
    bestFeatLabel=labels[bestFeat]
    myTree={bestFeatLabel:{}}
    del(labels[bestFeat])
    featValues=[example[bestFeat] for example in dataSet]
    uniqueVals=set(featValues)
    for value in uniqueVals:
        subLabels=labels[:]
        myTree[bestFeatLabel][value]=createTree(splitDataSet(dataSet,bestFeat,value),subLabels)
    return(myTree)
        
        

    
def createDataSet():
    dataSet=[[1,1,'yes'],
             [1,1,'yes'],
             [1,0,'no'],
             [0,1,'no'],
             [0,1,'no']]
    labels=['no surfacing','filippers']
    return(dataSet,labels)
        