import urllib
import re
from bs4 import BeautifulSoup
import math
import time

user = "calistoddard"
pinurl = "http://pinterest.com"

firstpg = urllib.urlopen(pinurl + "/" + user + "/pins/")
page = firstpg.read()
fh = open("calliepins.html","w")
fh.write(page)
fh.close()

# initialize arrays
pinids = []
boards = []
sources = []

count = re.compile(r'<strong>(.*?)</strong> Pins')
pincount = count.search(page).group(1)
npages = math.ceil(int(re.sub(r'[^\d-]+','',pincount))/50)
npages

start = time.localtime()
# test whether more than 0.5 second has passed
elapsed = time.localtime() - start
if elapsed > 0.5:
    time.sleep(0.5)
start = time.localtime()


soup = BeautifulSoup(page)
for pin in soup.find_all("a","PinImage ImgLink"):
    pinids.append(pin['href'])

for item in soup.find_all("div","pin"):   
    sourcenext = -1
    for child in item.descendants:
#        print "***" + str(child)
        if re.match('<a class="" href="/'+user,str(child)):
            boards.append(str(child))
        if sourcenext == 1:
            sources.append(str(child))
            sourcenext = 0
        if re.match(' from',str(child)):
            sourcenext = 1
    if sourcenext == -1:
        sources.append("None")

        
allpins = zip(pinids,boards,sources)
print allpins
#for page in npages:
    # extract the folder, pin id, and source
