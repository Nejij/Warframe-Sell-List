import urllib.request
import re
import os

#get html from page
def getHtml(url):
	with urllib.request.urlopen(url) as response:
		pageHTML = response.read()
	return pageHTML

#get mid price from html
def findMidPrice(table):
	result=re.search('column-3">(.*)</td><t', table)
	return result.group(1)
	
#list of urls to check
urls=['http://wftrading.net/sets/','http://wftrading.net/archwings-aw-weapons/','http://wftrading.net/void-trader-items/','http://wftrading.net/syndicate-weapons-mods','http://wftrading.net/prime-weapons/','http://wftrading.net/prime-warframes/','http://wftrading.net/warframe/','http://wftrading.net/rifle/','http://wftrading.net/shotgun/','http://wftrading.net/pistol/','http://wftrading.net/melee/','http://wftrading.net/sentinel/','http://wftrading.net/aura/','http://wftrading.net/most-wanted-rare/','http://wftrading.net/event-mods']
	
#delete old sell list
try:
	os.remove("sellList.txt")
except OSError:
	pass
#create and open new sell list
sellList=open("sellList.txt", "w+")
#get html from each url
for url in urls[:-1]:
	html=getHtml(url)
	#open local file
	myItems=open("myItems.txt", "rb+")
	#check if each line in the local file is in the html
	for line in myItems:
		#remove \r\n from the items
		item=line[:len(line)-2]
		#convert from byte array to string
		tmpItem=item.decode("utf-8")
		#remove "'" and "Blueprint"
		newTmpItem=tmpItem.replace("'","")
		del tmpItem
		endItem=newTmpItem.replace(" Blueprint","")
		#if the line is in the html
		if html.find(item)!=-1:
			itemPrice=repr(endItem).replace("'","") + " " + repr(findMidPrice(html[html.find(item):html.find(item)+200].decode())).replace("'","") + "|"
			sellList.write(itemPrice)
#close files
myItems.close()
sellList.close()