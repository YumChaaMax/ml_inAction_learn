# -*- coding: utf-8 -*-
"""
Created on Tue Jul 17 23:20:46 2018

@author: Max Yang
"""

import numpy as np
import operator

def createDataSet():
    group = np.array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels = ['A','A','B','B']
    return(group,labels)

def classify0(inX, dataSet, labels, k):
    """inX 用于分类变量的输入向量
       dataSet 训练样本集
       labels 标签向量，元素个数与dataSet的行数一致
    """
    dataSetSize = dataSet.shape[0]
    #将输入向量按照与训练集一致的形状复制，与训练集各向量相减
    diffMat = np.tile(inX, (dataSetSize,1)) – dataSet
    #平方
    sqDiffMat = diffMat**2
    sqDistances = sqDiffMat.sum(axis=1)
    distances = sqDistances**0.5
    #值排序，返回索引
    sortedDistIndicies = distances.argsort()
    classCount={}
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1
        #排序，对元组中的第二个元素operator.itemgetter(1)进行逆向排序reverse
    sortedClassCount = sorted(classCount.items(),
    key=operator.itemgetter(1), reverse=True)
    return(sortedClassCount[0][0])
    
def file2matirx(filename):
    fr=open(filename)
    arrayOlines=fr.readlines()
    nmuberOflines=len(arrayOlines)
    #创建（x,3)形状的array,array上的所有值都是0
    returnMatt=np.zeros((numberOflines,3))
    ClassLabelVector=[]
    index=0
    for line in arrayOlines:
        #去掉每一行首尾空格
        line=line.strip()
        listFromline=line.split('\t')
        returnMat[index,:]=listFromline[0:3]
        classLabelVector.append(listFromline[-1])
        index+=1
    return(returnMat,classLabelVector)
    
def autoNorm(dataSet):
    """多个特征值由于取值范围不同，
    导致计算距离时有的取值偏大的元素影响更深，此处用于归一化
    """
    #参数为0时表示取列上的最大/最小值，参数为1时表示取行上的最大最小值
    minVals=dataSets.min(0)
    maxVals=dataset.max(0)
    ranges=maxVals-minVals
    #总是要初始化一个值为0的np.array
    normDataSet=np.zeros(np.shape(dataSet))
    m=dataSet.shape[0]
    normDataSet=dataSet-np.tile(minVals,(m,1))
    normDataSet=normDataSet/tile(ranges,(m,1))
    return(normDataSet,ranges,minVals)
    
def datingClassTest():
    #测试集比例
    hoRatio=0.10
    datingDataMat,datingLabels=file2matrix（'datingTestSet.txt')
    normMat,ranges,minVals=autoNorm(datingDataMat)
    m=normMat.shape[0]
    numTestVecs=int(m*hoRatio)
    errorCount=0.0
    for i in range(numTestVecs):
        classifierResult=classiy0(normMat[i,:],normMat[numTestVecs:m,:],\
                                  datingLabels[numTestVecs:m],3)
        print("the classifier came back with :%d, the real anwser is :%d"\
              %(classiferResult, datingLabels[i]))
        if (classifierResult!=datingLabels[i]):errorcount+=1.0
    print("the total error rate is %f"%(errorcunt/float(numTestVecs)))

def classifyPerson()：:
    resultList=['not at all','in small doses','in large doses']
    percentTats=float(raw_input(\
                                "percentage  of time spent plaing video games?"))
    ffMiles=float(raw_input("frequent flier miles earned per year?"))
    iceCream=float(raw_input("liters of ice cream consumed per year?"))
    datingDataMat,datingLabels=file2matrix("dat.txt")
    normMat,ranges,minVals=autoNorm(datingDataMat)
    inArr=array([ffMiles,percentTats,iceCream])
    classifierResult=classify0((inArr-minVals)/ranges,normMat,datingLabels,3)
    print("you will probably like this person:," resultList[classifierResult-1])
        