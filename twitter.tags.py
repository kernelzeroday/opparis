#!/usr/bin/env python
#-*- coding: utf-8 -*-
# Extract Isis Twitter Accounts From Hash Tags - https://ghostbin.com/paste/vhdjs
#
# For #OpParis by PeterPunk 2015
#
# TWITTER NO-LOGIN with selenium, BeautifulSoup
#
# Accessing TWITTER IS hashtags (taken from text file  'HashTags.txt' originally 
# originaly taken from https://oasis.sandstorm.io/shared/fC311wGUaTUS-oFOAZHY9FncVDfD7Zj2TYB119LJbY7) 
# and get all persons with a specific frequency of contribution on this hashtags, 
# considering them as IS cadidates. Store them in a text file 'PossibleIS.txt' for additional examination.
#
# !!!!!!! Check the 'Initialize Vars Section' below for program variables  !!!!!!!!!!!!!
#

import time
from selenium.webdriver.common.proxy import *
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.proxy import *

# Initialize Vars Section ----------------------------------------------------------------------------
dictNames={}
inputFile = 'HashTags.txt' # A text file containning the IS Hashtags.
outputFile = 'PossibleIS.txt' # The output file that will contains the IS condidates for examination. 
iDeepLevelOfHashtag = 2 # How many times to automatically scroll down to twitter hashtag page to get more data.
iThreshold = 2 # Minimum number of posts a user has in order to be suspected an in IS candidate.
# -----------------------------------------------------------------------------------------------------


#Build the Proxy object using the locally running Privoxy
port = "8118" #The Privoxy (HTTP) port
myProxy = "127.0.0.1:"+port
proxy = Proxy({
    'proxyType': ProxyType.MANUAL,
    'httpProxy': myProxy,
    'ftpProxy': myProxy,
    'sslProxy': myProxy,
    'noProxy': ''
})

#Launch the Firefox window and visit the given URL
ff = webdriver.Firefox(proxy=proxy)
url_no = 0

with open(inputFile) as f:
	for hashtag in f:
		url_no = url_no + 1
		hashtag = hashtag.strip()
		url = "https://twitter.com/search?q=%s&src=tren" % hashtag
		print '[+] Trying #%d: %s'% (url_no, url)

		ff.get(url)
		time.sleep(5)

		for i in range(1,iDeepLevelOfHashtag):
			ff.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			time.sleep(4)

		# Get the content of the page into data var.
		data = ff.page_source.encode("utf-8")

		# Put Data into the... soup ;)
		soup = BeautifulSoup(data, 'html.parser')

		# Scan HTML page to get all the names involved.
		allRows = soup.findAll('a', {"class":"account-group js-account-group js-action-profile js-user-profile-link js-nav"})
		for row in allRows:
			name = row.find('b').text
			# If the name already exists in Dictionary increase occurance by 1, otherwise insert it with default value = 1.
			if name in dictNames.keys():
				dictNames[name] = dictNames[name] + 1
			else:	
				dictNames[name] = 1
			
#Close the browser
ff.close()

# Get all names with frequency >= iThreshold.
IScadidates = dict((k, v) for k, v in dictNames.items() if v >= iThreshold)

print 'Writting to %s...' % outputFile,

# Put them in a file and bye bye!
out = open(outputFile, "w")
for key, value in IScadidates.iteritems() :
	link = 'https://twitter.com/'+key
	out.write(link+"\n")

print 'ok!'


