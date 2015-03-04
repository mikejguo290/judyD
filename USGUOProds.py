import cPickle as pickle
import gzip
import StringIO
import os
from datetime import datetime
import xlrd
import pandas as pd
from pandas import DataFrame, read_excel
import shelve
import math

s = shelve.open('JudyD analysis.db')#

class businessRecord(object):
    def __init__(self):
        self.Duns = None
        self.GUODuns = None
        self.VB = None
        self.GRP =None
        self.LTD = None
        self.STD = None
        self.Life = None
        self.ADD = None
        self.IDI = None
        self.ILTC = None
        self.GLTC = None
        self.Prod1 = None
        self.Prod2 = None
        self.Prod3 = None
        self.Prod4 = None
        self.Broker1= None
        self.Broker2= None
        self.Broker3= None
        self.Broker4= None
        self.UnumCustomer = None
        self.UnumVBBroker = None
        self.UnumGrpBroker = None
        self.UnumIDIBroker = None	
        self.UnumILTCBroker = None
        self.UnumGLTCBroker = None
        
        self.UnumProds = None
        self.JudyProds =None
        self.AllProds =None
  
    def unumPortfolio(self):
        #no duplicates, everything should be in the same order, though not alphabetic.
        unumProdsList = set([self.VB, self.GRP, self.LTD, self.STD, self.Life, self.ADD, self.IDI, self.ILTC, self.GLTC])
        self.UnumProds = unumProdsList
    def judyPortfolio(self):
        # this is the troublesome when combined with unumPortfolio,  duplications, "All Other Products" etc.
        def delimit(word):
            return word.split(' ')
        a = delimit(self.Prod1)
        b = delimit(self.Prod2)
        c = delimit(self.Prod3)
        d = delimit(self.Prod4)
        judyProdsList = a + b + c + d
        self.JudyProds = set(judyProdsList)
    
        
    
    def allPortfolio(self):
        self.AllProds = self.JudyProds. union(self.UnumProds)
        self.AllProds = [value.encode('utf-8') for value in self.AllProds if ( not (isinstance(value, float)) and value != '')]
      
    def recombineWords(self):
        wordsList = self.AllProds
        newWordsList =[]
        i= 0
        while i <len(wordsList):
            
            if wordsList[i] != "All":
                newWordsList.append(wordsList[i])
                i+=1
            else:
                newWordsList.append("All Other Products")
                i+=3
        self.AllProds = sorted( newWordsList )
        # terrible bodge. if i add sorted on allPortfolio, then call recombineWords, weird stuff happens
                

GUOs ={}

for key,item in s.items():
    if item.GUODuns not in GUOs:
        GUOs[str(item.GUODuns)] = set()
print GUOs


for compDuns, comp in s.items():
    if str(comp.GUODuns) in GUOs:
        comp.unumPortfolio()
        comp.judyPortfolio()
        comp.allPortfolio()
        comp.recombineWords()
        
        if len(comp.AllProds)>0:
            print comp.AllProds
            #print "the brokers are %s, %s, %s and %s." % (comp.Broker1, comp.Broker2, comp.Broker3, comp.Broker4)
            #print "the brokers are %s, %s, %s, %s and %s." % (comp.UnumVBBroker, comp.UnumGrpBroker, comp.UnumIDIBroker, comp.UnumILTCBroker, comp.UnumGLTCBroker)
            
        #print list(comp.AllProds)[0], type( list(comp.AllProds)[0])
        #print comp.AllProds
        #print comp.AllProds
        #GUOs[str(comp.GUODuns)].update(comp.AllProds)

        
s.close()

"""
for key, item in GUOs.items():
    
    print key, item
"""
