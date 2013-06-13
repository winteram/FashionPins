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



unionsource=[]
intersectsource=[]
jaccardsource=[]



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
        cur.execute("SELECT Sources_sourceid FROM Pin_has_sources WHERE Pins_pinid=\"%s\"" % str(item[0]))
        board1sources.append(cur.fetchall())
    #print "Board1 sources: " + str(len(board1sources))



    # Get second random board
    board2=randint(1,allboards)
    #print "Random Board2: " + str(board2)

    # Get second board pins
    cur.execute("SELECT COUNT(*) From Board_has_pins where Boards_boardid=\"%i\"" % (board2))
    board2pinnum=cur.fetchone()[0]
    #print "Board2 pins: " + str(board2pinnum)

    # Get second board pin sources
    cur.execute("SELECT Pins_pinid FROM Board_has_pins where Boards_boardid=\"%i\"" % (board2))
    board2pins=cur.fetchall()
    board2sources=[]
    for item in board2pins:
        cur.execute("SELECT Sources_sourceid FROM Pin_has_sources WHERE Pins_pinid=\"%s\"" % str(item[0]))
        board2sources.append(cur.fetchall())
    #print "Board2 sources: " + str(len(board2sources))

   
    # Find intersection of first board sources & second board sources
    a,b=set(board1sources), set(board2sources)
    intersect= len(a.intersection(b))
    intersectsource.append(intersect)
    union=len(board1sources)+len(board2sources)-intersect
    unionsource.append(union)

    if union != 0:
        jaccard_index="%.3f" % (float(intersect)/float(union))
    else:
        jaccard_index=0
    #jaccard_index=round((float(intersect)/float(union)),4)
    #print jaccard_index
    #print "Intersect: " + str(intersect) +"-" + "Union: " + str(union) + '-'+ "Jaccard: " + str(jaccard_index)
    jaccardsource.append(jaccard_index)
    

    return True

class Counter(dict):
    

    def __init__(self, iterable=None, **kwds):
        '''Create a new, empty Counter object.  And if given, count elements
        from an input iterable.  Or, initialize the count from another mapping
        of elements to their counts.

        >>> c = Counter()                           # a new, empty counter
        >>> c = Counter('gallahad')                 # a new counter from an iterable
        >>> c = Counter({'a': 4, 'b': 2})           # a new counter from a mapping
        >>> c = Counter(a=4, b=2)                   # a new counter from keyword args

        '''        
        self.update(iterable, **kwds)

    def __missing__(self, key):
        return 0

    def most_common(self, n=None):
        '''List the n most common elements and their counts from the most
        common to the least.  If n is None, then list all element counts.

        >>> Counter('abracadabra').most_common(3)
        [('a', 5), ('r', 2), ('b', 2)]

        '''        
        if n is None:
            return sorted(self.iteritems(), key=itemgetter(1), reverse=True)
        return nlargest(n, self.iteritems(), key=itemgetter(1))

    def elements(self):
        '''Iterator over elements repeating each as many times as its count.

        >>> c = Counter('ABCABC')
        >>> sorted(c.elements())
        ['A', 'A', 'B', 'B', 'C', 'C']

        If an element's count has been set to zero or is a negative number,
        elements() will ignore it.

        '''
        for elem, count in self.iteritems():
            for _ in repeat(None, count):
                yield elem

    # Override dict methods where the meaning changes for Counter objects.

    @classmethod
    def fromkeys(cls, iterable, v=None):
        raise NotImplementedError(
            'Counter.fromkeys() is undefined.  Use Counter(iterable) instead.')

    def update(self, iterable=None, **kwds):
        
        if iterable is not None:
            if hasattr(iterable, 'iteritems'):
                if self:
                    self_get = self.get
                    for elem, count in iterable.iteritems():
                        self[elem] = self_get(elem, 0) + count
                else:
                    dict.update(self, iterable) # fast path when counter is empty
            else:
                self_get = self.get
                for elem in iterable:
                    self[elem] = self_get(elem, 0) + 1
        if kwds:
            self.update(kwds)

    def copy(self):
        'Like dict.copy() but returns a Counter instance instead of a dict.'
        return Counter(self)

    def __delitem__(self, elem):
        'Like dict.__delitem__() but does not raise KeyError for missing values.'
        if elem in self:
            dict.__delitem__(self, elem)

    def __repr__(self):
        if not self:
            return '%s()' % self.__class__.__name__
        items = ', '.join(map('%r: %r'.__mod__, self.most_common()))
        return '%s({%s})' % (self.__class__.__name__, items)



    def __add__(self, other):
        '''Add counts from two counters.

        >>> Counter('abbb') + Counter('bcc')
        Counter({'b': 4, 'c': 2, 'a': 1})


        '''
        if not isinstance(other, Counter):
            return NotImplemented
        result = Counter()
        for elem in set(self) | set(other):
            newcount = self[elem] + other[elem]
            if newcount > 0:
                result[elem] = newcount
        return result

    def __sub__(self, other):
        ''' Subtract count, but keep only results with positive counts.

        >>> Counter('abbbc') - Counter('bccd')
        Counter({'b': 2, 'a': 1})

        '''
        if not isinstance(other, Counter):
            return NotImplemented
        result = Counter()
        for elem in set(self) | set(other):
            newcount = self[elem] - other[elem]
            if newcount > 0:
                result[elem] = newcount
        return result

    def __or__(self, other):
        '''Union is the maximum of value in either of the input counters.

        >>> Counter('abbb') | Counter('bcc')
        Counter({'b': 3, 'c': 2, 'a': 1})

        '''
        if not isinstance(other, Counter):
            return NotImplemented
        _max = max
        result = Counter()
        for elem in set(self) | set(other):
            newcount = _max(self[elem], other[elem])
            if newcount > 0:
                result[elem] = newcount
        return result

    def __and__(self, other):
        ''' Intersection is the minimum of corresponding counts.

        >>> Counter('abbb') & Counter('bcc')
        Counter({'b': 1})

        '''
        if not isinstance(other, Counter):
            return NotImplemented
        _min = min
        result = Counter()
        if len(self) < len(other):
            self, other = other, self
        for elem in ifilter(self.__contains__, other):
            newcount = _min(self[elem], other[elem])
            if newcount > 0:
                result[elem] = newcount
        return result

if __name__=="__main__":

    conn = pymysql.connect(host='localhost', unix_socket='/tmp/mysql.sock', user='pinarozturk', passwd='', db='pindb')
    cur = conn.cursor()

    for i in range(0,10000):
        print i
        randomboard()

    
    pin={}
    pdict={}
    pinjac={}
    pjdict={}


    c=Counter(unionsource)
    d=Counter(intersectsource)
    e=Counter(jaccardsource)
##    print len(c)
##    print len(d)
##    print e


            
    #Intersect - Union - Jaccard library
    for a in range(len(unionsource)):
        key=str(unionsource[a])+'-'+str(intersectsource[a])+'-'+str(jaccardsource[a])
        #print key
        if key not in pjdict:
            pjdict[key]=jaccardsource[a]
        #else:
            #pdict[key]+=1
            
    #print '-'
    #print pjdict

    #Jaccard index matrix
    i=0
    f=0
    for i in range(0,len(c)):
        pinjac[list(c)[i]]={}
        for y in range(0,len(d)):
            for f in range(0,len(e)):
                key3=str(list(c)[i])+'-'+str(list(d)[y])+'-'+str(list(e)[f])
                if key3 in pjdict:
                    #print key3
                    #print pjdict[key3]
                    pinjac[list(c)[i]][list(d)[y]]=pjdict[key3]
                    #print pinjac[list(c)[i]][list(d)[y]]
                #else:
                    #pinjac[list(c)[i]][list(d)[y]]=0
                    

    #print '-'
    #print pinjac
    

##    print "c: " + str(len(c))
##    print "d: " + str(len(d))
##
##    a=np.zeros((len(c),len(d)))
##
##    keys=[]
##    keys2=[]
##
##    for key,values in pin.iteritems():
##        keys.append(key)
##        for key2, value in values.iteritems():
##            if key2 not in keys2:
##                keys2.append(key2)
##
##    for key, values in pin.iteritems():
##        index=keys.index(key)
##        for key2, value in values.iteritems():
##            index2=keys2.index(key2)
##            a[index][index2]=values.get(key2,0)
##            
##    np.savetxt("pinmat.csv", a, delimiter=",",fmt='%2i')
            


    # Write Jaccard index Matrix
    print "Dataframe"
    df2 = DataFrame(pinjac)
    print "transpose"
    df2t=df2.transpose()
    print "to csv"
    df2t.to_csv('pinsJac.csv')

    
    
    cur.close()
    conn.close()
