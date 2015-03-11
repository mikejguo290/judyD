import cPickle as pickle
import gzip
import StringIO
import os
from datetime import datetime
import xlrd
import xlwt
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
    def keyUKBroker(self):
        forbiddenList =["aon", "gallagher",'lockton','jlt','jardine lloyd thompson','towers watson']
        compBrokers = [self.Broker1,self.Broker2,self.Broker3,self.Broker4,self.UnumCustomer,self.UnumVBBroker,self.UnumGrpBroker,self.UnumIDIBroker,self.UnumILTCBroker,self.UnumGLTCBroker]
    
        flag = False     
        for forbiddenBroker in forbiddenList:
            for broker in compBrokers:
                if forbiddenBroker in (broker.lower()):
                    flag = True
        return flag
                
    

GUOs ={}

for key,item in s.items():
    if item.GUODuns not in GUOs:
        GUOs[str(item.GUODuns)] = set()
print GUOs
#quick lookup in dicc for GUOs

for compDuns, comp in s.items():
    if str(comp.GUODuns) in GUOs:
        comp.unumPortfolio()
        comp.judyPortfolio()
        comp.allPortfolio()
        comp.recombineWords()
        
        if len(comp.AllProds)>0 and (not(comp.keyUKBroker())): 
            print comp.Duns, comp.GUODuns, sorted(comp.AllProds)
            #print "the brokers are %s, %s, %s and %s." % (comp.Broker1, comp.Broker2, comp.Broker3, comp.Broker4)
            #print "the brokers are %s, %s, %s, %s and %s." % (comp.UnumVBBroker, comp.UnumGrpBroker, comp.UnumIDIBroker, comp.UnumILTCBroker, comp.UnumGLTCBroker)
            
        #print list(comp.AllProds)[0], type( list(comp.AllProds)[0])
        #print comp.AllProds
        #print comp.AllProds
        #GUOs[str(comp.GUODuns)].update(comp.AllProds)
def GUOProducts(s):
    GUOProd ={}
    for compDuns, comp in s.items():
        comp.unumPortfolio()
        comp.judyPortfolio()
        comp.allPortfolio()
        comp.recombineWords()
        
        if len(comp.AllProds)>0 and not(comp.keyUKBroker()):
            
            GUOProd[str(comp.GUODuns)] = GUOProd.get(str(comp.GUODuns),[])+(comp.AllProds)

    NewGUOProd ={}
    for key, item in GUOProd.items():
        NewGUOProd[key]=", ".join( sorted(list(set(item)),reverse=True) ) #have to convert the list to string, can't print it out otherwise. 
    return NewGUOProd

def UnumProducts(s):
    Prod ={}
    for compDuns, comp in s.items():
        comp.unumPortfolio()
        UnumProds=[value.encode('utf-8') for value in comp.UnumProds if ( not (isinstance(value, float)) and value != '')]
        if len(UnumProds)>0 and not(comp.keyUKBroker()):
            
            Prod[str(comp.GUODuns)] = Prod.get(str(comp.GUODuns),[])+ list(UnumProds)

    NewProd ={}
    for key, item in Prod.items():
        NewProd[key]=", ".join(  sorted(list(set(item)),reverse=True) ) #have to convert the list to string, can't print it out otherwise. 
    return NewProd

def BrokerProducts(s):
    Prod ={}
    for compDuns, comp in s.items():
        comp.unumPortfolio()
        UnumProds=[value.encode('utf-8') for value in comp.UnumProds if ( not (isinstance(value, float)) and value != '')]
        if len(UnumProds)>0 and not(comp.keyUKBroker()):
            
            Prod[str(comp.GUODuns)] = Prod.get(str(comp.GUODuns),[])+ list(UnumProds)

    NewProd ={}
    for key, item in Prod.items():
        NewProd[key]=", ".join(  sorted(list(set(item)),reverse=True) ) #have to convert the list to string, can't print it out otherwise. 
    return NewProd

def prodInGroup(s, product):
    """
    Shows how many subs hold a certain product in a particular group.
    """
    prodDist = {}
    for key,item in s.items():
        
        if product in item.AllProds and not item.keyUKBroker():
            prodDist[str(item.GUODuns)]=prodDist.get(str(item.GUODuns),0) + 1
    return prodDist

def compInGroup(s):
    """
    Shows how many subs exist under a GUO.
    """
    compDist = {}
    for key,item in s.items():
        compDist[str(item.GUODuns)]=compDist.get(str(item.GUODuns),0)  + 1
        #compDist[str(item.GUODuns)]=compDist.get(str(item.GUODuns),[])  + [item]
    return compDist


#print "GIP in GUOS", prodInGroup(s, "LTD")
#print "Life in GUOS",prodInGroup(s, "Life")

#print compInGroup(s)

def outputToExcel(array,filename):
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('data',cell_overwrite_ok=True)
    row = 0
    sheet.write(row,0,'GUO')
    sheet.write(row,1,'Products')
    row = 1
    for key, val in array.items():
        sheet.write(row,0,key)#names.decode('utf-8')
        sheet.write(row,1,val)#matched name
        row+=1
        
    workbook.save('%s.xls'% filename)
    print "OUTPUT CREATED!"

#outputToExcel(prodInGroup(s, 'Life'),"subsidiaries with GLIF")
#outputToExcel(prodInGroup(s, 'LTD'),"subsidiaries with GIP")
#outputToExcel(GUOProducts(s),"Products in Group")
outputToExcel(UnumProducts(s),"Unum Products in Group")
s.close()

"""
for key, item in GUOs.items():
    
    print key, item
"""
