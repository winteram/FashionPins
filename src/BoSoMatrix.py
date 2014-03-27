import time
import pymysql
from itertools import chain


def getboards():
   
    cur.execute("Select Boardid from Boards;")
    boardids=cur.fetchall()
    allboards=[]
    for boardid in boardids:
        boards=[]
        # Get Sources from Pins table
        cur.execute("select sources_sourceid from Pins where sources_sourceid<>0 and Boards_boardid=\"%s\"" % (boardid))
        pinboards=cur.fetchall()
        #print pinboards
        
        # Get Sources from Repins table
        cur.execute("select sources_sourceid from Pins join Pin_has_repinboards on Pins.pinid=Pin_has_repinboards.pins_pinid where Pin_has_repinboards.BOards_boardid=\"%s\"" % (boardid))
        repinboards=cur.fetchall()
        #print repinboards
        boards=pinboards+repinboards
        boards=set(list(chain.from_iterable(boards)))
        allboards.append(list(boards))
    
   
    return allboards

if __name__=="__main__":
    time1=time.time()
    conn = pymysql.connect(host='localhost', unix_socket='/tmp/mysql.sock', user='pinarozturk', passwd='W1nter0zturk', db='newpindb')
    cur = conn.cursor()
    boards1= getboards()
    
    boards={}
    for i in range(0,len(boards1)):
        key=i
        if key in boards:
            boards[i].append(boards1[i])
        else:
            boards[i]=boards1[i]
    print "Initial Boards " + "  :length " +str(len(boards))
    #print boards
 #
 #       
    K=5
    board_done=False
    source_done=False
    
    while not board_done and not source_done: 
        board_done=False
        source_done=False 
        
        #Update Boards     
        newboards={}    
        for key,board in boards.iteritems():
            if len(board) >=K:
                newboards[key]=board
        if len(newboards)==len(board):
            board_done=True
            print "board done true"
        else:
            boards=newboards 
        print "boards updated " + ">= " + str(K) +"  :length " +str(len(boards))    
        #print boards
        
        # Create sources from BOards
        sources={}
        i=0
        for key,board in boards.iteritems():
            for source in board:
                if source in sources:
                    sources[source].append(key)
                else:
                    sources[source]=[key]
            i+=1
        print "sources created"  +"  :length " +str(len(sources))
        #print sources
        
        #Update Sources
        newsources={}
        for key,source in sources.iteritems():
            if len(source) >=K:
                newsources[key]=source 
        if len(newsources)==len(sources):
            source_done=True
            print "source done true"
        else:
            sources=newsources
        print "sources updated" + ">= " + str(K) +"  :length " +str(len(sources))
        #print sources
        
        #Create Boards from Sources
        boards={}
        i=0
        for key,source in sources.iteritems():
            for board in source:
                if board in boards:
                    boards[board].append(key)
                else:
                    boards[board]=[key]
            i+=1
        print "boards created" + "  :length " +str(len(boards))  
        #print boards
    
    print "Final Boards" +"  :length " +str(len(boards))
    #print boards
    print "Final Sources"+"  :length " +str(len(sources))
    #print sources
    time2=time.time() 
    print "time elapsed: " + str(time2-time1)    
