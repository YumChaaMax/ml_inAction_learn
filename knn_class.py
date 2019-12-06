
# coding: utf-8

# In[2]:


import numpy as np
import operator


# In[3]:


def createDataSet():
    group = np.array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels = ['A','A','B','B']
    return(group,labels)


# In[1]:


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


# In[8]:


dataset,labels=createDataSet()


# In[12]:


diffMat=np.tile([0,0],(4,1))-dataset
print(diffMat)


# In[13]:


sqDiffMat = diffMat**2
sqDistances = sqDiffMat.sum(axis=1)
distances = sqDistances**0.5


# In[14]:


sortedDistIndicies = distances.argsort()


# In[17]:


classCount={}
for i in range(3):
    voteIlabel = labels[sortedDistIndicies[i]]
    print(voteIlabel)
    classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1
    print(classCount)
    #排序，对元组中的第二个元素operator.itemgetter(1)进行逆向排序reverse
    sortedClassCount = sorted(classCount.items(),
    key=operator.itemgetter(1), reverse=True)
    print(sortedClassCount)

