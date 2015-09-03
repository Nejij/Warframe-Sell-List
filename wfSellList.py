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
	
#converts bytes to string
def toString(byteStr):
	charStr=byteStr.decode("utf-8")
	return charStr
	
#remove substring from string
def remSub(mainStr, subStrArr):
	for i, j in subStrArr.items():
		mainStr=mainStr.replace(i, j)
	return mainStr
	
#list of urls to check
urls=['http://wftrading.net/sets/','http://wftrading.net/archwings-aw-weapons/','http://wftrading.net/void-trader-items/','http://wftrading.net/syndicate-weapons-mods','http://wftrading.net/prime-weapons/','http://wftrading.net/prime-warframes/','http://wftrading.net/warframe/','http://wftrading.net/rifle/','http://wftrading.net/shotgun/','http://wftrading.net/pistol/','http://wftrading.net/melee/','http://wftrading.net/sentinel/','http://wftrading.net/aura/','http://wftrading.net/most-wanted-rare/','http://wftrading.net/event-mods']
	
#delete old sell list
try:
	os.remove("sellList.txt")
except OSError:
	pass
#create and open new sell list
sellList=open("sellList.txt", "w+")
#print WTS to file
sellList.write("WTS|")
#get html from each url
for url in urls[:-1]:
	html=getHtml(url)
	#open local file
	try:
		myItems=open("myItems.txt", "rb+")
	except OSError:
		pass
		print('Error: "myItems.txt" not found.')
	#check if each line in the local file is in the html
	for line in myItems:
		#remove \r\n from the items
		item=line[:len(line)-2] #type: bytes
		#convert from byte array to string
		tempStrItem=toString(item)
		#remove "'" and "Blueprint"
		strItem=remSub(tempStrItem, {"'":"", "Blueprint":""})
		#if the line is in the html
		if html.find(item)!=-1:
			itemPrice=strItem + " " + repr(findMidPrice(html[html.find(item):html.find(item)+200].decode())).replace("'","") + "|"
			sellList.write(itemPrice)
#close files
myItems.close()
sellList.close()