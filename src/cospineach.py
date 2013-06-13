from operator import itemgetter
from heapq import nlargest
from itertools import repeat, ifilter
import math
import pymysql
import random
from random import randint
import csv
import collections
import numpy as np
from pandas import DataFrame
from csv import DictWriter




def cosine_similarity(vector1,vector2):
  # Calculate numerator of cosine similarity
  dot=sum(p*q for p,q in zip(vector1, vector2))
  #print dot
  
  # Normalize the vectors
  sum_vector1=sum([vector1[i]**2 for i in range(len(vector1))])
  sum_vector2=sum([vector2[i]**2 for i in range(len(vector2))])
  denominator=math.sqrt(sum_vector1) * math.sqrt(sum_vector2)

  if not denominator:
      return 0.0
  else:
      return float(dot) / denominator

def randomboard():
    # Get # of boards crawled
    cur.execute("SELECT COUNT(*) FROM Boards where is_crawled=1")
    allboards=cur.fetchone()[0]
    #print "Boards number: " + str(allboards)

    # Get first random boardid
    board1=randint(1,allboards)
    #print "Random Board1: " + str(board1)

    # Get first board pins
    cur.execute("SELECT COUNT(*) From Board_has_pins where Boards_boardid=\"%i\"" % (board1))
    board1pinnum=cur.fetchone()[0]
    #print "Board1 pins: " + str(board1pinnum)

    #Get first board pin sources
    cur.execute("SELECT Pins_pinid FROM Board_has_pins where Boards_boardid=\"%i\"" % (board1))
    board1pins=cur.fetchall()
    #print len(board1pins)
    board1sources=[]
    for item in board1pins:
        #print str(item[0])
        cur.execute("SELECT Sources_sourceid FROM Pin_has_sources WHERE Pins_pinid=\"%s\"" % str(item[0]))
        source=cur.fetchone()
        if source != None:
            board1sources.append(source[0])
    #print "Board1 sources: " + str(len(board1sources))
    

    return board1,board1sources



if __name__=="__main__":

    conn = pymysql.connect(host='localhost', unix_socket='/tmp/mysql.sock', user='pinarozturk', passwd='', db='pindb')
    cur = conn.cursor()

    cosdict={}
    cossimdict={}
    board1a=[]
    board2a=[]
    cossima=[]
    board1so=[]
    for i in range(0,100):
        print i
        board1,board1s=randomboard()
        board1so.append(board1s)
        board1a.append(board1)

    for a in range(0,len(board1a)):
      for b in range(0,len(board1a)):
        cossim=cosine_similarity(board1so[a],board1so[b])
        cossima.append(cossim)
        #print str(board1a[a]) +'-'+ str(board1a[b]) + '-' +str(cossim)
        key=str(board1a[a]) +'-'+str(board1a[b]) + '-' +str(cossim)
        if key not in cosdict:
            cosdict[key]="%.3f" % cossim

    #print cosdict
                               
    c=board1a
    d=board1a
    e=cossima

    print "Cos sim mat"
    #Cosine similarity matrix
    i=0
    f=0
    for i in range(0,len(c)):
        cossimdict[list(c)[i]]={}
        for y in range(0,len(d)):
            for f in range(0,len(e)):
                key3=str(list(c)[i])+'-'+str(list(d)[y])+'-'+str(list(e)[f])
                if key3 in cosdict:
                    #print key3
                    #print pjdict[key3]
                    cossimdict[list(c)[i]][list(d)[y]]=cosdict[key3]
                    #print pinjac[list(c)[i]][list(d)[y]]
                #else:
                    #pinjac[list(c)[i]][list(d)[y]]=0
    #print cossimdict

    
    print "Dataframe"
    # Write Cosine Sim Matrix
    df = DataFrame(cossimdict)
    #print df
    print "to Csv"
    df.to_csv('cosdicteach100.csv')


    
    
    cur.close()
    conn.close()
