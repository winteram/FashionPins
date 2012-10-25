import urllib
import re
from bs4 import BeautifulSoup
import math

user = "calistoddard"
pinurl = "http://pinterest.com"


firstpg = urllib.urlopen(pinurl + "/" + user + "/pins/")
page=firstpg.read()
count=re.compile(r'<strong>(.*?)</strong>  Pins')
pincount=count.search(page).group(1)
npages=math.ceil(int(re.sub(r'[^\d-]+','',pincount))/50)


soup = BeautifulSoup(firstpg)


#for page in npages:
    # extract the folder, pin id, and source

