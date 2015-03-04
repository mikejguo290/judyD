import cPickle as pickle
import gzip
import StringIO
import os
from datetime import datetime
import xlrd
import pandas as pd
from pandas import DataFrame, read_excel
import shelve

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
        self.UnumProds = None
        self.JudyProds =None
        self.AllProds =None
    def unumPortfolio(self):
        unumProdsList = [self.VB, self.GRP, self.LTD, self.STD, self.Life, self.ADD, self.IDI, self.ILTC, self.GLTC]
        self.UnumProds = unumProdsList
        
    def judyPortfolio(self):
        def delimit(word):
            return word.split(' ')
        a = delimit(self.Prod1)
        b = delimit(self.Prod2)
        c = delimit(self.Prod3)
        d = delimit(self.Prod4)
        e = a + b + c + d
        judyProdsList = set(e)
        self.JudyProds = judyProdsList
        
    def allPortfolio(self):
        self.AllProds = self.JudyProds.union(self.UnumProds)
        #self.AllProds = set(self.AllProds)
        a = self.AllProds#[logical_not(isnan(self.AllProds))]
        #a = [value for value in a if isinstance(value, str)]
        a = [value for value in a if ( not (isinstance(value, float)) and value != '')]
        self.AllProds = a
        
def readAllComp(tabName):
    filLocation = r"E:\Marketing Insight And Analysis\Analysis - Internal\Broker Packs\Mercer\20150109 -US owned startups in UK\Archive\Mercer GUOs List input 2.xlsx"
    data_df =read_excel(filLocation,tabName)
    return data_df

#print readAllComp('Test Tab').describe

companies= {}

for index, row in readAllComp('Test Tab').iterrows():#
    a = businessRecord()
    a.Duns = row ['Duns_No']
    a.GUODuns= row['Duns_No_Global_Parent']
    a.VB = row['VB']
    a.GRP = row['GRP']#
    a.LTD = row['LTD']#
    a.STD = row['STD']
    a.Life = row['Life']
    a.ADD = row['ADD']
    a.IDI= row['IDI']
    a.ILTC = row['ILTC']
    a.GLTC= row['GLTC']
    a.Prod1 = row ['Products#1']
    a.Prod2 = row ['Products#2']
    a.Prod3 = row ['Products#3']
    a.Prod4 = row ['Products#4']

    a.unumPortfolio()
    a.judyPortfolio()
    a.allPortfolio()
    
    companies[a.Duns] = a 
    """
    unumProdsList = [a.VB, a.GRP,a.LTD, a.STD, a.Life, a.ADD, a.IDI, a.ILTC, a.GLTC]
    a.UnumProds = dict(zip(unumProdsList,unumProdsList))

    judyProdsList = [a.Prod1,a.Prod2,a.Prod3,a.Prod4]
    a.JudyProds = dict(zip(judyProdsList,judyProdsList))

    a.AllProds = dict(a.UnumProds.items() + a.JudyProds.items())
    companies[a.Duns] = a 
    """
s = shelve.open('JudyD analysis.db')#
try:
    for key,item in companies.items():
        s[str(key)]=item
finally:
    print len(companies.keys())
    s.close()
    print "output produced"

