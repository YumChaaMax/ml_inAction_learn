# -*- coding: utf-8 -*-
"""
Created on Tue Jan 15 18:52:52 2019

@author: Max Yang
"""

import matplotlib as plt
import numpy as np

import warnings
#忽略warning 警告错误信息
warnings.filterwarnings('ignore')
import pandas as pd
url='https://github.com/tristanga/Data-Analysis/raw/master/Global%20Superstore.xls'
df=pd.read_excel(url)
df=df[(df.Segment=='Consumer')& (df.Country=='United States')]
df.head()

#为每一位消费者创建RFM变量
#注意agg用法，可以对数据框的不同字段用不同的（自定义）函数计算
df_RFM=df.groupby('Customer ID').agg({'Order Date':lambda y:(df['Order Date'].max().date()-y.max().date()).days,
                  'Order ID': lambda y: len(y.unique()),
                  'Sales': lambda y: round(y.sum(),2)})
df_RFM.columns=['Recency','Frequency','Monetary']
df_RFM=df_RFM.sort_values('Monetary',ascending=False)

df_RFM.head()

quantiles=df_RFM.quantile(q=[0.8])

df_RFM['R']= np.wehre(df_RFM['Recency']<=int(quantiles.Recency.values),2,1)