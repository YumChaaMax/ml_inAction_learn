# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 19:48:16 2018

@author: Max Yang
"""

import numpy as np
import tkinter as tkt
import regTrees as rt
import matplotlib as plt
plt.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

def reDraw(tolS,tolN):
    #清空之前的图像
    reDraw.f.clf()
    reDraw.a=reDraw.f.add_subplot(111)
    if chkBtnVar.get():
        if tolN<2: tolN=2
        myTree=rt.createTree(reDraw.rawDat,rt.modelleaf,rt.modelErr,(tolS,tolN))
        yHat=rt.createForeCast(myTree,reDraw.testDat,rt.modelTreeEval)
    else:
        myTree=rt.createTree(reDraw.rawDat,ops=(tolS,tolN))
        yHat=rt.createForeCast(myTree,reDraw.testDat)
    reDraw.a.scatter(reDraw.rawDat[:,0],reDraw.rawDat[:,1],s=5)
    reDraw.a.plot(reDraw.testDat,yHat,linewidth=2.0)
    reDraw.canvas.show()        
    
    
def getInputs():
    try: tolN=int(tolNentry.get())
    except:
        tolN=10
        print("enter Integer for tolN")
        tolNentry.delete(0)
        tolNentry.insert(0,'10')
    try: tolS=int(toSentry.get())
    except:
        tolN=1.0
        print("enter Float for tolS")
        tolSentry.delete(0)
        tolSentry.insert(0,'1.0')
    return(tolN,tolS)
    

def drawNewTree():
    tolN,tolS=getInputs()
    reDraw(tolS,tolN)

root=tkt.Tk()

#tkt.Label(root,text="Plot Place Holder").grid(row=0,columnspan=3)
reDraw.f=Figure(figsize=(5,4),dpi=100)
reDraw.canvas=FigureCanvasTkAgg(reDraw.f,master=root)
reDraw.canvas.show()
reDraw.canvas.get_tk_widget().grid(row=0,columnspan=3)

tkt.Label(root,text="tolN").grid(row=1,column=0)

tolNentry=tkt.Entry(root)
tolNentry.grid(row=1,column=1)
tolNentry.insert(0,'10')

tkt.Label(root,text="tolS").grid(row=2,column=0)

tolSentry=tkt.Entry(root)
tolSentry.grid(row=2,column=1)
tolSentry.insert(0,'1.0')

tkt.Button(root,text="ReDraw",command=drawNewTree).grid(row=2,column=2,rowspan=3)

chkBtnVar=tkt.IntVar()
chkBtn=tkt.Checkbutton(root,text="Model Tree",variable=chkBtnVar)
chkBtn.grid(row=3,column=0,columnspan=2)

reDraw.rawDat=np.mat(rt.loadDataSet(r'./dataset/sine.txt'))
reDraw.testDat=np.arange(np.min(reDraw.rawDat[:,0]),np.max(reDraw.rawDat[:,0]),0.01)
reDraw(1.0,10)

root.mainloop()
