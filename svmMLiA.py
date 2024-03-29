# -*- coding: utf-8 -*-
"""
Created on Sun Nov  4 18:10:36 2018

@author: Max Yang
"""
import numpy as np

def loadDataSet(fileName):
    dataMat=[];labelMat=[]
    fr=open(fileName)
    for line in fr.readlines():
        lineArr=line.strip().split('\t')
        dataMat.append([float(lineArr[0]),float(lineArr[1])])
        labelMat.append(float(lineArr[2]))
    return(dataMat,labelMat)
    
def selectJrand(i,m):
    """i 为第一个alpha的下标，m为所有alpha的数目"""
    j=i
    while(j==i):
        j=int(np.random.uniform(0,m))
        
    return(j)

def clipAlpha(aj,H,L):
    if aj>H:
        aj=H
    if L>aj:
        aj=L
    return(aj)
    
def smoSimple(dataMatIn,classLabels,C,toler,maxIter):
    dataMatrix=np.mat(dataMatIn);labelMat=np.mat(classLabels).transpose()
    b=0; m,n=np.shape(dataMatIn) 
    alphas=np.zeros((m,1))
    iter=0
    while(iter<maxIter):
        #用于记录alpha是否已经优化
        alphaPairsChanged=0
        for i in range(m):
            fXi=float(np.multply(alphas,labelMat).T*\
                      (dataMatrix*dataMatrix[i,:].T))+b
            Ei=fXi-float(labelMat[i])
            if ((labelMat[i]*Ei<-toler) and (alphas[i]<C) or \
                (labelMat[i]*Ei>toler) and (alphas[i]>0)):
                j=selectJrand(i,m)
                fXj=float(np.multiply(alphas,labelMat).T*\
                          (dataMatrix*dataMatrix[j,:].T))+b
                Ej=fXj-float(labelMat[j])
                alphaIold=alphas[i].copy()
                alphaJold=alphas[j].copy()
                if (labelMat[i] != labelMat[j]):
                    L=max(0,alphas[j]-alphas[i])
                    H=min(C,C+alphas[j]-alphas[i])
                else:
                    L=max(0,alphas[j]+alphas[i]-C)
                    H=min(C,alphas[j]+alphas[i])
                if L==H: print("L=H") ;continue
                #eta是alphas[j]的最优修改量
                eta=2.0*dataMatrix[i,:]*dataMatrix[j,:].T-\
                dataMatrix[i,:]*dataMatrix[i,:].T-\
                dataMatrix[j,:]*dataMatrix[j,:].T
                alphas[j]-=labelMat[j]*(Ei-Ej)/eta
                alphas[j]=clipAlpha(alphas[j],H,L)
                if abs(alphas[j]-alphaJold)<0.00001:
                    print("j not moving enough");continue
                alphas[i]+=labelMat[j]*labelMat[i]*\
                (alphaJold-alphas[j])
                b1=b-Ei-labelMat[i]*(alphas[i]-alphaIold)*\
                dataMatrix[i,:]*dataMatrix[i,:].T-\
                labelMat[j]*(alphas[j]-alphaJold)*\
                dataMatrix[j,:]*dataMatrix[j,:].T
                
                b2=b-Ej-labelMat[i]*(alphas[i]-alphaIold)*\
                dataMatrix[i,:]*dataMatrix[j,:].T-\
                labelMat[j]*(alphas[j]-alphaJold)*\
                dataMatrix[i,:]*dataMatrix[j,:].T
                
                if (0<alphas[i]) and (C>alphas[i]): b=b1
                elif (0<alphas[j]) and (C>alphas[j]):b=b2
                else: b=(b1+b2)/2.0
                alphaPairsChanged+=1
                print("iter: %d i:%d , pairs changed %d" % \
                      (iter,i, alphaPairsChanged))
        if alphaPairsChanged==0:
            iter+=1
        else:
            iter=0
        print("iteration number: %d" % iter)
    return(b,alphas)
                    
                    