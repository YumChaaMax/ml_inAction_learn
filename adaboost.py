# -*- coding: utf-8 -*-
"""
Created on Fri Jan 11 20:00:52 2019

@author: Max Yang
"""
import numpy as np

def loadSimpData():
    datMat=np.matrix([[1.,2.1],[2.0,1.1],[1.3,1.0],[1.0,1.0],[2.0,1.0]])
    classLabels=[1.0,1.0,-1.0,-1.0,1.0]
    return datMat, classLabels
    
def stumpClassify(dataMatrix,dimen,threshVal,threshIneq):
    """通过对阈值比较对数据进行分类,
    dimen 表示维度
    """
    retArray=np.ones((np.shape(dataMatrix)[0],1))
    if threshIneq == 'lt':
        retArray[dataMatrix[:,dimen]<=threshVal]=-1.0
    else:
        retArray[dataMatrix[:,dimen]>threshVal]=-1.0
    return retArray

def buildStump(dataArr,classLabels,D):
    """单层决策树生成函数（弱分类器),
    D=np.mat(np.ones((5,1))/5)
    样本的权重之和为1"""
    dataMatrix= np.mat(dataArr)
    labelMat=np.mat(classLabels).T
    m,n=np.shape(dataMatrix)
    numSteps=10.0;bestStump={}
    bestClasEst=np.mat(np.zeros((m,1)))
    #首先设定最小误差为无限
    minError=np.inf
    for i in range(n):
        #获取一列上的最大最小值，来确定步长
        rangeMin = dataMatrix[:,i].min()
        rangeMax = dataMatrix[:,i].max()
        stepSize = (rangeMax-rangeMin)/numSteps
        for j in range(-1,int(numSteps+1)):
            for inequal in ['lt','gt']:
                #数据分类（不断尝试不同的分类值的结果，找到错误率较低）
                threshVal = (rangeMin+float(j)*stepSize)
                predictedVals= \
                stumpClassify(dataMatrix,i,threshVal,inequal)
                errArr=np.mat(np.ones((m,1)))
                #分类结果与实际值比较，这里用法特别注意array(5,1)与matirx（5，1）元素级比较
                #如果是两个matrix,回整体比较
                errArr[predictedVals==labelMat] = 0
                #计算错误率
                weightedError=D.T*errArr
                
                print("split: dim %d, thresh %.2f, thresh \
                      inequal: %s, the weighted error is %.3f"\
                      % (i,threshVal,inequal,weightedError))
                
                if weightedError < minError:
                    minError = weightedError
                    bestClasEst = predictedVals.copy()
                    bestStump['dim'] = i
                    bestStump ['thresh'] = threshVal
                    bestStump['ineq'] = inequal
    return bestStump, minError, bestClasEst
    
def adaBoostTrainDS(dataArr,classLabels,numIt=40):
    weakClassArr=[]
    m=np.shape(dataArr)[0]
    #D存储所有样本的权重，样本的权重之和为1，初始权重都一样
    #随着学习，增加错误分类的样本的权重，降低正确分类的样本权重
    D=np.mat(np.ones((m,1))/m)
    aggClassEst=np.mat(np.zeros((m,1)))
    for i in range(numIt):
        bestStump,error,classEst=buildStump(dataArr,classLabels,D)
        print("D:", D.T)
        #max(error,1e-16)确保下面的公式不会因为除0的情况报错，1e-16 就是10的-16次方
        alpha=float(0.5*np.log((1.0-error)/max(error,1e-16)))
        bestStump['alpha']=alpha
        weakClassArr.append(bestStump)
        print("classEst:",classEst.T)
        #迭代计算D
        expon=np.multiply(-1*alpha*np.mat(classLabels).T,classEst)
        D=np.multiply(D,np.exp(expon))
        D=D/D.sum()
        #aggClassEst 用来记录每个数据点的类别估计累计值
        aggClassEst+=alpha*classEst
        print("aggClassEst: ",aggClassEst)
        aggErrors=np.multiply(np.sign(aggClassEst))\
        !=np.mat(classLabels).T,np.ones((m,1)))
        errorRate=aggErrors.sum()/m
        print("total error: ",errorRate, "\n")
        if errorRate==0.0:
            break
    return(weakClassArr)
    
def adaClassify(datToClass,classifierArr):
    """预测新样本的分类"""
    dataMatrix=np.mat(datToClass)
    m=np.shape(dataMatrix)[0]
    aggClassEst=np.mat(np.zeros((m,1)))
    for i in range(len(classifierArr)):
        classEst=stumpClassify(dataMatrix,classifierArr[i]['dim'],\
                               classifierArr[i]['thresh'],\
                               classifierArr[i]['ineq'])
        aggClasEst += classifierArr[i]['alpha']*classEst
        print(aggClassEst)
    return(np.sign(aggClassEst))
    
                    
        
        
    

    