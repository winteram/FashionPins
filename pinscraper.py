import urllib
import re
from bs4 import BeautifulSoup
import math

user = "calistoddard"
pinurl = "http://pinterest.com"


firstpg = urllib.urlopen(pinurl + "/" + user + "/pins/")
page=firstpg.read()
page
count=re.compile(r'<strong>(.*?)</strong> Pins')
pincount=count.search(page).group(1)
npages=math.ceil(int(re.sub(r'[^\d-]+','',pincount))/50)
npages

soup = BeautifulSoup(firstpg)
repins=soup.find_all("div","pin")


#for page in npages:
    # extract the folder, pin id, and source

