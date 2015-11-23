#!/bin/python

# pastebin_hunter.py
#	Version 0.1
# 	Searches latest pastebin submissions for suspicious content
# 	Uses a wordlist to match content
# 	#OpParis
#
# Requirements
#   Beautiful Soup 4 library
#       $ pip install beautifulsoup4
#
#   Developed in Python 2.7.9 by mpac

from urllib2 import urlopen, URLError
from argparse import ArgumentParser
from bs4 import BeautifulSoup
import os.path
import sys
import time
import random
import argparse

linkListFilePath = "linklist"

def getwordlist(wordListFilePath):
	words = []
	if os.path.isfile(wordListFilePath):
		with open(wordListFilePath, 'r') as thefile:
			words = thefile.read().splitlines()
	else:
		print wordListFilePath,"file not found"
	return words

def getLastLinkList():
	lines = []
	if os.path.isfile(linkListFilePath):
		with open(linkListFilePath, 'r') as thefile:
			lines = thefile.read().splitlines()
	return lines

def scanFile(fileUrl,wordlist):
	try:
		resp = urlopen(fileUrl)
	except URLError as e:
		print 'An error occured fetching %s \n %s' % (url, e.reason)   
		return -1

	content = resp.read().splitlines()
	
	# matching with the wordlist	
	stop = False
	for line in content:
		if stop:
			break;
		line = line.decode('utf-8')
		for word in wordlist:
			wordEncoded = word.decode('utf-8')
			if not line.find(wordEncoded) == -1:
				print "Suspicious file detected:",fileUrl
				stop = True


	return 0

def main():

	parser = argparse.ArgumentParser()
	parser.add_argument("wordlist", help="path to a wordlist file")
	args = parser.parse_args()

	# Get word list
	wordlist = getwordlist(args.wordlist)
	if len(wordlist) == 0:
		print "[ERROR] Empty wordlist (-1)"
		return -1

	archiveUrl = "http://pastebin.com/"
	
	while(1):
		# Opening URL
		try:
			resp = urlopen(archiveUrl)
		except URLError as e:
			print 'An error occured fetching %s \n %s' % (url, e.reason)   
			continue
		html = resp.read()
		soup = BeautifulSoup(html, "html.parser")

		# Get table
		try:
			table = soup.find('div',attrs={"id":"menu_2"})
		except AttributeError as e:
			print '[ERROR] Table not found, moving on (-2)'
			continue

		if type(table) == type(None):
			print '[ERROR] Table not found, moving on (-3)'
			continue

		try:
			# Getting all the files in the table
			linklist = []
			for row in table.find_all("li"):
				linklist.append(row.a['href'])

			# Get last link list
			lastLinkList = getLastLinkList()

			# Go through all links in the current list
			for item in linklist:
				# Make sure it was not already scanned
				if not item in lastLinkList:
					print item
					# scan this paste
					scanFile("http://pastebin.com/raw.php?i=" + item[1:],wordlist)

				# Wait a bit before making next request (2 ± 1 secs)
				time.sleep(2 + random.randrange(-100,100)/100.0)

			# Save the link list
			with open(linkListFilePath, 'w') as thefile:
				for item in linklist:
					thefile.write("%s\n" % item.encode('utf-8'))

		except Exception as e:
			print '[ERROR] On main, exiting (-2)',e
			return -2

		# Wait for next cycle (3 ± 1 secs)
		time.sleep(3 + random.randrange(-100,100)/100.0)
	return 0

if __name__ == '__main__':
	status = main()
	sys.exit(status)

# Developed in Python 2.7.9 by mpac