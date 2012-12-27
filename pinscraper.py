import urllib
import re
from bs4 import BeautifulSoup
import math
import time
import pprint
from unicoderw import UnicodeWriter

searchword="fashion"
pinurl = "http://pinterest.com"
boardpgurl = "http://pinterest.com/search/boards/?q="+searchword+"&page="


# initialize arrays
boardlist=[]
userlist = []
newboardlist=[]
crawledboards=[]
pinids=[]

pindict = {}


# Get initial boards from search
def getinitial():
    nboardpages=1
    for bpage in range(1,nboardpages+1):
        print "opening board list " + str(bpage)
        boardpg = urllib.urlopen(boardpgurl+str(bpage))
        # test whether more than 0.5 second has passed
        start=time.time()
        elapsed = time.time() - start
        if elapsed > 0.5:
            time.sleep(0.5)
        start = time.time()

        boardread = boardpg.read()
        soup = BeautifulSoup(boardread)
        for board_div in soup.find_all("div","pin pinBoard"):
            for userid_a in board_div.find_all("a","colorless"):
                userid = userid_a["href"]
                userlist.append(userid)
            for h3_name in board_div("h3","serif"):
                for a_name in h3_name("a"):
                    board_name=a_name['href']
                    boardlist.append(board_name)

    print "Number of boards: "+str(len(boardlist))
	return boardlist

# get pins from boards
def getpins(boardlist, crawledboards):
    for a in range(0,len(boardlist)):
	firstpg = urllib.urlopen(pinurl + "/" + boardlist[a])
        # test whether more than 0.1 second has passed
        start = time.time()
        elapsed = time.time() - start
        if elapsed > 0.1:
            time.sleep(0.1)
        start = time.time()

	pageread = firstpg.read()
	count = re.compile(ur'<strong>(.*?)</strong> pins', re.UNICODE)
        pincount_group = count.search(pageread)
        if not pincount_group:
            a = a - 1
            continue
	pincount = pincount_group.group(1)
	npages = math.ceil(int(re.sub(r'[^\d-]+','',pincount))/50)
	print "Pin pages in board "+str(a)+": "+str(npages)
        crawledboards.append(boardlist[a])
	npage=int(npages)
   	for i in range(1,npage+2):
    		pages=urllib.urlopen(pinurl+"/"+boardlist[a]+"?page="+str(i))
                # test whether more than 0.1 second has passed
                elapsed = time.time() - start
                if elapsed > 0.1:
                    time.sleep(0.1)
                start = time.time()
                page=pages.read()
    		soup = BeautifulSoup(page)
    		for pin in soup.find_all("div","pin"):
    	   		pinid = "None"
    	   		board = "None"
    	  	 	source = "None"
                        userid = "None"
           		for pinid_a in pin.find_all("a","PinImage ImgLink"):
               			pinid = pinid_a['href']
               			#userid=userlist[a]
                                userid = boardlist[a].split('/')[1]
               			board=boardlist[a]
           		for clearfix in pin.find_all("div","convo attribution clearfix"):
                   		for link in clearfix.find_all("a"):
                                    source = link['href']
                        # remove sources that are None or Empty
                        if source != "None" and source != '':
                            key = userid+'-'+source
                            if key not in pindict:
                                pindict[key] = (pinid,board,userid,source)
                                pinids.append(pinid)
    #How to return pindict to use in Main??
    #Returning pinids, couldn't extract pinids from dict to use in getboards
    print "Number of Pinids: " + str(len(pinids))
    return pinids


# get boards from pins - it takes a while!
def getboards(pinids, crawledboards):
        #Only using first 50 instead of len(pinids) - for now.
    	for k in range(0,50):
		pinpages=urllib.urlopen(pinurl+pinids[k])
		# test whether more than 0.1 second has passed
        	start=time.time()
		elapsed = time.time() - start
        	if elapsed > 0.1:
                	time.sleep(0.1)
        	start = time.time()
		pinpage=pinpages.read()
		soup=BeautifulSoup(pinpage)
		for spin in soup.find_all("span","repin_post_attr"):
			newuserid=spin.a.next_sibling.next_sibling['href'].split('/')[3]
			newboard=spin.a.next_sibling.next_sibling['href'].split('/')[4]
			newboardname="/"+newuserid+"/"+newboard+"/"
			#check if newboard is in crawledboards
			s="\n".join(crawledboards)
			if not newboardname in s:
				newboardlist.append(newboardname)
        print "Number of NewBoards: " + str(len(newboardlist))
   	return newboardlist


if __name__=="__main__":
    boardlist = getinitial()
    pinids=getpins(boardlist,crawledboards)
    newboardlist=getboards(pinids,crawledboards)

    # loop N times between getpins and getboards
    pindict = getpins(boardlist, crawledboards, pindict)
    # extract pins from dictionary


    allpins = pindict.values()
    allpins.sort(key=lambda tup: tup[3])

    f = open("allpins.csv","w")
    writer = UnicodeWriter(f)
    writer.writerows(allpins)
    f.close()
