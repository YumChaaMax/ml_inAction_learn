# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 15:09:43 2018
regTrees
@author: Max Yang
"""
import numpy as np

def loadDataSet(fileName):
    dataMat=[]
    fr=open(fileName)
    for line in fr.readlines():
        curLine=line.strip().split('\t')
        fltLine=list(map(float,curLine))
        dataMat.append(fltLine)
    return(dataMat)

def binSplitDataSet(dataSet,feature, value):
    mat0=dataSet[np.nonzero(dataSet[:,feature]>value)[0],:]
    mat1=dataSet[np.nonzero(dataSet[:,feature]<=value)[0],:]
    return(mat0,mat1)
    

    
def regLeaf(dataSet):
    return(np.mean(dataSet[:,-1]))
    
def regErr(dataSet):
    return(np.var(dataSet[:,-1])*np.shape(dataSet)[0])
    
def createTree(dataSet,leafType=regLeaf,errType=regErr,ops=(1,4)):
    feat,val=chooseBestSplit(dataSet,leafType,errType, ops)
    if feat==None:
        return(val)
    retTree={}
    retTree['spInd']=feat
    retTree['spVal']=val
    lSet,rSet=binSplitDataSet(dataSet,feat,val)
    retTree['left']=createTree(lSet,leafType,errType,ops)
    retTree['right']=createTree(rSet,leafType,errType,ops)
    return(retTree)
    
def chooseBestSplit(dataSet,leafType=regLeaf, errType=regErr,ops=(1,4)):
    #tolS is a tolerance on error reduction，tolN is a minimum data instances, 
    #which are user-defined settings
    tolS=ops[0]; tolN=ops[1]
    #此处len(set())==1用于判定是否所有值取值相同
    if len(set(dataSet[:,-1].T.tolist()[0]))==1:
        return(None,leafType(dataSet))
    m,n=np.shape(dataSet)
    S=errType(dataSet)
    bestS=np.inf;bestIndex=0;bestValue=0
    #循环计算每一个值，找出最佳切分
    for featIndex in range(n-1):
        for splitVal in set((dataSet[:,featIndex].T.tolist())[0]):
            mat0,mat1=binSplitDataSet(dataSet,featIndex,splitVal)
            #if continue 用于跳出本次循环， break 用于跳出整个循环
            if (np.shape(mat0)[0]<tolN) or (np.shape(mat1)[0]<tolN):
                continue
            newS=errType(mat0)+errType(mat1)
            if newS<bestS:
                bestIndex=featIndex
                bestValue=splitVal
                bestS=newS
    if (S-bestS) <tolS:
        return(None,leafType(dataSet))
    mat0,mat1=binSplitDataSet(dataSet,bestIndex,bestValue)
    if (np.shape(mat0)[0]<tolN) or (np.shape(mat1)[0]<tolN):
        return(None,leafType(dataSet))
    return(bestIndex,bestValue)
        
def isTree(obj):
    return(type(obj).__name__=='dict')

def getMean(tree):
    if isTree(tree['right']):
        tree['right']=getMean(tree['right'])
    if isTree(tree['left']):
        tree['left']=getMean(tree['left'])
    return((tree['left']+tree['right'])/2)
    
def prune(tree,testData):
    """输入参数是训练出的树，和测试集"""
    if np.shape(testData)[0]==0:
        return(getMean(tree))
    if (isTree(tree['right']) or isTree(tree['left'])):
        lSet,rSet=binSplitDataSet(testData,tree['spInd'],tree['spVal'])
    if isTree(tree['left']):
        tree['left']=prune(tree['left'],lSet)
    if isTree(tree['right']):
        tree['right']=prune(tree['right'],rSet)
    if not isTree(tree['left']) and not isTree(tree['right']):
        lSet,rSet=binSplitDataSet(testData,tree['spInd'],tree['spVal'])
        errorNoMerge=np.sum(np.power(lSet[:,-1]-tree['left'],2))+\
        np.sum(np.power(rSet[:-1]-tree['right'],2))
        treeMean=(tree['left']+tree['right'])/2.0
        errorMerge=np.sum(np.power(testData[:-1]-treeMean,2))
        if errorMerge<errorNoMerge:
            print('merging')
            return(treeMean)
        else:
            return(tree)
    else:
        return(tree)
        
def linearSolve(dataSet):
    m,n=np.shape(dataSet)
    X=np.mat(np.ones((m,n)));Y=np.mat(np.ones((m,1)))
    X[:,1:n]=dataSet[:,0:n-1]; Y=dataSet[:,-1]
    xTx=X.T*X
    if np.linalg.det(xTx)==0.0:
        raise NameError ('This matrix is singular, cannot do inverse, \
                         try increase second value of ops')
    ws=xTx.I*(X.T*Y)
    return(ws,X,Y)
    
def modelleaf(dataSet):
    ws,X,Y=linearSolve(dataSet)
    return(ws)
    
def modelErr(dataSet):
    ws,X,Y=linearSolve(dataSet)
    yHat=X*ws
    return(np.sum(np.power(Y-yHat,2)))
    
def regTreeEval(model,inDat):
    return(float(model))
    
def modelTreeEval(model,inDat):
    n=np.shape(inDat)[1]
    X=np.mat(np.ones((1,n+1)))
    X[:,1:n+1]=inDat
    return(float(X*model))
    
def treeForeCast(tree,inData,modelEval=regTreeEval):
    """给定单个数据点或行向量，返回预测值"""
    if not isTree(tree):
        return(modelEval(tree,inData))
    if inData[tree['spInd']]>tree['spVal']:
        if isTree(tree['left']):
            return(treeForeCast(tree['left'],inData,modelEval))
        else:
            return(modelEval(tree['left'],inData))
    else:
        if isTree(tree['right']):
            return(treeForeCast(tree['right'],inData,modelEval))
        else:
            return(modelEval(tree['right'],inData))
            
def createForeCast(tree,testData,modelEval=regTreeEval):
    m=len(testDat)
    yHat=np.mat(np.ones((m,1)))
    for i in range(m):
        yHat[i,0]=treeForeCast(tree,np.mat(testData[i]),modelEval)
        return(yHat)
        
        