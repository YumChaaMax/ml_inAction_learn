# -*- coding: utf-8 -*-
"""
Created on Sat Jul 21 07:01:02 2018

@author: Max Yang
"""
import numpy as np
from os import listdir
import kNN


def img2Vector(filename):
    """将二进制图像转换为向量"""
    returnVect=np.zeros((1,1024))
    fr=open(filename)
    for i in range(32):
        lineStr=fr.readline()
        for j in range(32):
            returnVect[0,32*i+j]=int(lineStr[j])
    return(returnVect)
    
def handwritingClassTest():
    hwLabels=[]
    trainingFileList=listdir('trainingDigits')
    m=len(trainingFileList)
    trainingMat=np.zeros((m,1024))
    for i in range(m):
        fileNameStr=trainingFileList[i]
        fileStr=fileNameStr.split('.')[0]
        classNumStr=int(fileStr.split('_')[0])
        hwLabels.append(classNumStr)
        trainingMat[i,:]=img2Vector('trainingDigits/%s'%fileNameStr)
    testFileList=listdir('testDigits')
    errorCount=0.0
    mTest=len(testFileList)
    for i in range(mTest):
        fileNameStr=testFileList[i]
        fileStr=fileNameStr.split('.')[0]
        classNumStr=int(fileStr.split('_')[0])
        vectorUnderTest=img2Vector('testDigits/%s'%fileNameStr)
        classifierResult=kNN.classify0(vectorUnderTest,trainingMat,hwLabels,3)
        print( "the classifier came back with : %d, the real anwser is: %d"\
        %(classifierResult,classNumStr))
        if (classifierResult!=classNumStr):errorCount+=1.0
        print("\nthe total number of errors is %d"%errorCount)
        print("\nthe total error rate is: %f" % (errorCount/float(mTest)))
        
        