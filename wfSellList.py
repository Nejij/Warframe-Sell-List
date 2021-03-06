import urllib.request
import re
import os
import operator

#######################################
#              FUNCTIONS
#######################################
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
	
#######################################
#                MAIN
#######################################
#delete old sell list
try:
	os.remove("sellList.txt")
except OSError:
	pass
#list of urls to check
urls=['http://wftrading.net/sets/','http://wftrading.net/archwings-aw-weapons/','http://wftrading.net/void-trader-items/','http://wftrading.net/syndicate-weapons-mods','http://wftrading.net/prime-weapons/','http://wftrading.net/prime-warframes/','http://wftrading.net/warframe/','http://wftrading.net/rifle/','http://wftrading.net/shotgun/','http://wftrading.net/pistol/','http://wftrading.net/melee/','http://wftrading.net/sentinel/','http://wftrading.net/aura/','http://wftrading.net/most-wanted-rare/','http://wftrading.net/event-mods']

#make dict
strDict={}

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
		#create item object and remove \r\n from the items
		item=line[:len(line)-2]
		#convert from byte array to string
		tempStrItem=toString(item)
		#remove "'" and "Blueprint"
		strItem=remSub(tempStrItem, {"'":"", " Blueprint":""})
		#if the line is in the html
		if html.find(item)!=-1:
			#get the html for that item
			itemHtmlStr=toString(html[html.find(item):html.find(item)+200])
			#get mid price of item
			tempItemPrice=findMidPrice(itemHtmlStr)
			#remove "'"
			itemPrice=remSub(tempItemPrice, {"'":""})
			#add item to dict
			strDict[strItem]=itemPrice

#convert dict values to int
intDict = dict((k,int(v)) for k,v in strDict.items())
#sort tuples
sortedIntList=sorted(intDict.items(), key=operator.itemgetter(1), reverse=True)
#make string for output
sellListStr="WTS|"
#add items to sellListStr 
for i in sortedIntList:
	if len(sellListStr) < 270:
		sellListStr+=i[0] + " {}|".format(i[1])
#create and open new sell list
sellList=open("sellList.txt", "w+")
#write string to file
sellList.write(sellListStr[:-1])	

#close files
myItems.close()
sellList.close()