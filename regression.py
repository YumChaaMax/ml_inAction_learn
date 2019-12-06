# -*- coding: utf-8 -*-
"""
Created on Sun Aug 19 21:20:55 2018

@author: Max Yang
"""

import numpy as np
from numpy import linalg
from time import sleep
import json
import urllib2

def loadDataSet(filename):
    numFeat=len(open(filename).readline().split('\t'))-1
    dataMat=[];labelMat=[]
    fr=open(filename)
    for line in fr.readlines():
        lineArr=[]
        curLine=line.strip().split('\t')
        for i in range(numFeat):
            lineArr.append(float(curLine[i]))
        dataMat.append(lineArr)
        labelMat.append(float(curLine[-1]))
    return(dataMat,labelMat)
    
def standRegres(xArr,yArr):
    """计算最佳拟合直线,
    input 是x,y列表
    输出w;
    标准回归
    """
    xMat=np.mat(xArr);yMat=np.mat(yArr).T
    xTx=xMat.T*xMat
    if linalg.det(xTx)==0.0:
        print("this matrix is singular,cannot do inverse")
        return
    #求w,这里也可以用linalg.solve(xTx,xMat.T*yMatT)
    ws=xTx.I*(xMat.T*yMat)
    
    return(ws)
   
def lwlr(testPoint,xArr,yArr,k=1.0):
    """局部加权线性回归，针对感兴趣的点加权
       testPoint 为待预测的点，
       xArr,yArr用于建模型，
       k高斯核系数，k越小所有的值权重，仅有较少的值用于考虑回归
     """
    xMat=np.mat(xArr);yMat=np.mat(yArr).T
    m=np.shape(xMat)[0]
    #创建对角矩阵，np.eye创建一个所有元素都是0除了第k个对角线等于1的array
    weights=np.mat(np.eye((m)))
    for j in range(m):
        diffMat=testPoint-xMat[j,:]
        #高斯核来对附近的点赋予更高的权重
        weights[j,j]=np.exp(diffMat*diffMat.T/(-2.0*k**2))
    xTx=xMat.T*(weights*xMat)
    if linalg.det(xTx)==0.0:
        print("this matrix is singular,cannot do inverse")
        return
    ws=xTx.I* (xMat.T*(weights*yMat))
    return(testPoint*ws)
    
def lwlrTest(testArr,xArr,yArr,k=1.0):
    """为数据集的每个点调用lwlr()"""
    m=np.shape(testArr)[0]
    yHat=np.zeros(m)
    for i in range(m):
        yHat[i]=lwlr(testArr[i],xArr,yArr,k)
    return(yHat)
    
def rssError(yArr,yHatArr):
    return(((yArr-yHatArr)**2).sum())
    
def ridgeRegres(xMat,yMat,lam=0.2):
    xTx=xMat.T*xMat
    #np.eye 用于生成单位矩阵（对角线是1，其余为0）
    denom=xTx+np.eye(np.shape(xMat)[1])*lam
    if linalg.det(denom)==0.0:
        print("this matrix is singular,cannot do inverse")
        return
    #matrix.I表示求逆
    ws=denom.I*(xMat.T*yMat)
    return(ws)
    
def ridgeTest(xArr,yArr):
    """目的：数据标准化，多个lambda取值"""
    xMat=np.mat(xArr);yMat=np.mat(yArr).T
    yMean=np.mean(yMat,0)
    yMat=yMat-yMean
    xMeans=np.mean(xMat,0)
    #return the variance of the array elements
    xVar=np.var(xMat,0)
    xMat=(xMat-xMeans)/xVar
    numTestPts=30
    wMat=np.zeros((numTestPts,np.shape(xMat)[1]))
    for i in range(numTestPts):
        ws=ridgeRegres(xMat,yMat,np.exp(i-10))
        wMat[i,:]=ws.T
    return(wMat)
    
def stagewise(xArr,yArr,eps=0.01,numIt=100):
    xMat=np.mat(xArr);yMat=np.mat(yArr).T
    yMean=np.mean(yMat,0)
    yMat=yMat-yMean
    xMeans=np.mean(xMat,0)
    xVar=np.var(xMat,0)
    xMat=(xMat-xMeans)/xVar
    m,n=np.shape(xMat)
    returnMat=np.zeros((numIt,n))
    ws=np.zeros((n,1))
    wsTest=ws.copy()
    wsMax=ws.copy()
    for i in range(numIt):
        print(ws.T)
        lowestError=np.inf
        for j in range(n):
            for sign in [-1,1]:
                wsTest=ws.copy()
                wsTest[j]+=eps*sign
                yTest=xMat*wsTest
                rssE=rssError(yMat.A,yTest.A)
                if rssE<lowestError:
                    lowestError=rssE
                    wsMax=wsTest
        ws=wsMax.copy()
        returnMat[i,:]=ws.T
    return(returnMat)
                
def searchForSet(retX, retY, setNum, yr, numPce,origPrc):
    sleep(10)
    myAPIstr='get from code.google.com'
    searchURL='https://www.googleapis.com/shopping/search/v1/public/products?\
    key=%s&country=US&q=lego+%d&alt=json' % (myAPIstr,setNum)
    pg=urllib2.urlopen(searchURL)
    retDict=json.loads(pg.read())
    for i in range(len(retDict['items'])):
        try:
            currItem=retDict['items'][i]
            if currItem['product']['condition']=='new':
                newFlag=1
            else:
                newFlag=0
            listOfInv=currItem['product']['inventories']
            for item in listOfInv:
                sellingPrice=item['price']
                if sellingPrice>origPrc*0.5:
                    print("%d\t%d\t%d\t%f\t%f") %\
                    (yr,numPce,newFlag,origPrc,sellingPrice)
                    retX.append([yr,numPce,newFlag,origPrc])
                    retY.append(sellingPrice)
        except:print('problem with item %d' % i)

def crossValidation(xArr,yArr, numVal=10):
    """输入x,y以及交叉验证的次数"""
    m=len(yArr)
    indexList=range(m)
    errorMat=np.zeros((numVal,30))
    for i in range(numVal):
        trainX=[];trainY=[]
        testX=[];testY=[]
        np.random.shuffle(indexList)
        for j in range(m):
            if j < m*0.9:
                trainX.append(xArr[indexList[j]])
                trainY.append(yArr[indexList[j]])
            else:
                testX.append(xArr[indexList[j]])
                testY.append(yArr[indexList[j]])
        wMat=ridgeTest(trainX,trainY)
        for k in range(30):
            matTestX=np.mat(testX); matTrainX=np.mat(trainX)
            meanTrain=np.mean(matTrainX,0)
            varTrain=np.var(matTrainX,0)
            #用与训练数据相同的参数标准化，在ridgeTest中训练数据已经标准化
            matTestX=(matTestX-meanTrain)/varTrain
            yEst=matTestX*np.mat(wMat[k,:]).T+np.mean(trainY)
            errorMat[i,k]=rssError(yEst.T.A,np.array(testY))
            
    meanErrors=np.mean(errorMat,0)
    minMean=float(min(meanErrors))
    bestWeights=wMat[np.nonzero(meanErrors==minMean)]
    xMat=np.mat(xArr);yMat=np.mat(yArr).T
    meanX=np.mean(xMat,0); varX=np.var(xMat,0)
    unReg=bestWeights/varX
    print("the best model from Ridge Regression is :\n",unReg)
    print("with constant term: ",-1*sum(np.multiply(meanX,unReg))+np.mean(yMat))
                        
    
    
        