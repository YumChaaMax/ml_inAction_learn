# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 21:56:24 2018

@author: Max Yang
"""
import numpy as np

def loadDataSet():
    dataMat=[]
    labelMat=[]
    fr=open(r'D:\python_code\ML_AL_ACT\dataset\testSet.txt')
    for line in fr.readlines():
        lineArr=line.strip().split()
        dataMat.append([1.0,float(lineArr[0]),float(lineArr[1])])
        labelMat.append(int(lineArr[2]))
    return(dataMat,labelMat)
    
def sigmoid(inX):
    return(1.0/(1.0+np.exp(-inX)))
    
def gradAscent(dataMatIn,classLabels):
    dataMatrix=np.mat(dataMatIn)
    labelMat=np.mat(classLabels).transpose()
    m,n=np.shape(dataMatrix)
    alpha=0.001
    maxCycles=500
    weights=np.ones((n,1))
    for k in range(maxCycles):
        h=sigmoid(dataMatrix*weights)
        error=(labelMat-h)
        weights=weights+alpha*dataMatrix.transpose()*error
    return(weights)

def plotBestFit(weights):
    import matplotlib.pyplot as plt
    dataMat,labelMat=loadDataSet()
    dataArr=np.array(dataMat)
    n=np.shape(dataArr)[0]
    xcord1=[]; ycord1=[]
    xcord2=[]; ycord2=[]
    for i in range(n):
        if int(labelMat[i])==1:
            xcord1.append(dataArr[i,1]);ycord1.append(dataArr[i,2])
        else:
            xcord2.append(dataArr[i,1]);ycord2.append(dataArr[i,2])
    fig=plt.figure()
    ax=fig.add_subplot(111)
    ax.scatter(xcord1,ycord1,s=30,c='red',marker='s')
    ax.scatter(xcord2,ycord2,s=30,c='green')
    x=np.arange(-3.0,3.0,0.1)
    y=(-weights[0]-weights[1]*x)/weights[2]
    ax.plot(x,y)
    plt.xlabel('x1')
    plt.ylabel('X2')
    plt.show()

def stocGradAscent0(dataMatrix,classLabels):
    m,n=np.shape(dataMatrix)
    alpha=0.01
    weights=np.ones(n)
    for i in range(m):
        h=sigmoid(sum(dataMatrix[i]*weights))
        error=classLabels[i]-h
        weights=weights+alpha*error*dataMatrix[i]
    return(weights)